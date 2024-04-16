from src.shared.definition.exceptions import ConnectionNotEstablished
from src.shared.connections.credentials import Credential

from typing import Protocol


class Connector(Protocol):

    def __init__(self, credential: Credential):
        ...

    def build_connection(self, lib, **kwargs):
        ...


class SmtpConnector(Connector):

    def __init__(self, credential: Credential):
        self.credential = credential

    def get_credential(self):
        return self.credential

    def build_connection(self, lib):
        self.connection = lib(
            host=self.credential.get_server(),
            port=self.credential.get_port()
        )
        return self.connection

    def account_login(self):
        self.connection.starttls()
        return self.connection.login(
            self.credential.get_sender(),
            self.credential.get_password()
        )

    def address_message(self, message):
        message["From"] = self.credential.get_sender()
        message["To"] = self.credential.get_reciever()
        return message

    def send_email(self, message):
        return self.connection.sendmail(
            from_addr = self.credential.get_sender(),
            to_addrs = self.credential.get_reciever(),
            msg = message.as_bytes()
        )


class SshConnector(Connector):

    def __init__(self, credential: Credential):
        self.credential = credential

    def build_connection(self, lib):
        self.tunnel = lib(
            ssh_address_or_host=self.credential.get_host(),
            ssh_username=self.credential.get_username(),
            ssh_password=self.credential.get_password(),
            remote_bind_address=(
                self.credential.get_hostname(), 
                self.credential.get_port()
            )
        )
        return self.tunnel

    def start_tunnel(self):
        self.tunnel.start()

    def close_tunnel(self):
        self.tunnel.close()


class MySqlConnector(Connector):

    def __init__(self, credential: Credential):
        self.credential = credential
        self.connection = None
        self.cursor = None

    def build_connection(self, lib, tunnel):
        tunnel.start_tunnel()
        self.connection = lib(
            user=self.credential.get_host(),
            password=self.credential.get_password(),
            host=self.credential.get_username(),
            port=tunnel.local_bind_port,
            db=self.credential.get_database()
        )
        return self.connection

    def get_cursor(self):
        try:
            self.cursor = self.connection.cursor()
        except AttributeError:
            raise ConnectionNotEstablished("Call build_connection first.")
        return self.cursor

    def commit(self):
        try:
            self.connection.commit()
        except AttributeError:
            raise ConnectionNotEstablished("Call build_connection first.")

    def close(self, tunnel):
        try:
            if self.cursor is not None:
                self.cursor.close()
            self.connection.close()
            tunnel.close_tunnel()
        except AttributeError:
            raise ConnectionNotEstablished("Call build_connection first.")