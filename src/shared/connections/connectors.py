from src.shared.connections.credentials import Credential

from typing import Protocol, NewType, Tuple
from enum import Enum


ConnectionType = NewType('ConnectionType', str)

class ConnectorType(Enum):
    SMTP = ConnectionType("smtp")
    SSH = ConnectionType("ssh")
    MYSQL = ConnectionType("mysql")


class Connector(Protocol):
    """
    Represents a connector for establishing a connection to a data source.
    """

    def __init__(self, credential: Credential, **kwargs):
        """
        Initializes the connector with the given credential.
        """

    def __enter__(self):
        """
        Enters the context manager.
        """

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context manager.
        """

    @property
    def library(self):
        """
        Returns the library used by the connector.
        """


class SmtpConnector(Connector):

    def __init__(self, credential: Credential):
        self.credential = credential

    def __enter__(self):
        self.connection = self.library(
            host=self.credential.get_server(),
            port=self.credential.get_port()
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.quit()

    @property
    def library(self):
        import smtplib
        return smtplib.SMTP

    def get_credential(self):
        return self.credential

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

    def __enter__(self):
        self.tunnel = self.library(
            ssh_address_or_host=self.credential.get_host(),
            ssh_username=self.credential.get_username(),
            ssh_password=self.credential.get_password(),
            remote_bind_address=(
                self.credential.get_hostname(), 
                self.credential.get_port()
            )
        )
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.tunnel.close()
    
    @property
    def library(self):
        import sshtunnel
        sshtunnel.SSH_TIMEOUT = 5.0
        sshtunnel.TUNNEL_TIMEOUT = 5.0
        return sshtunnel.SSHTunnelForwarder

    def get_local_bind_port(self) -> Tuple:
        return self.tunnel.local_bind_port

    def start_tunnel(self):
        self.tunnel.start()

    def is_active(self) -> bool:
        return self.tunnel.is_active


class MySqlConnector(Connector):

    def __init__(self, credential: Credential, **kwargs):
        self.credential = credential
        self.ssh_connection = kwargs.get('ssh_connection')

    def __enter__(self):
        if not self.ssh_connection.is_active():
            self.ssh_connection.start_tunnel()
        self.connection = self.library(
            user=self.credential.get_username(),
            password=self.credential.get_password(),
            host=self.credential.get_host(),
            port=self.ssh_connection.get_local_bind_port(),
            db=self.credential.get_database()
        )
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
    
    @property
    def library(self):
        import pymysql
        return pymysql.connect

    def get_cursor(self):
        return self.cursor