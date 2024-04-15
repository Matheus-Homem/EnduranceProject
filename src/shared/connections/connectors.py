from src.shared.connections.credentials import Credential
from typing import Protocol

class Connector(Protocol):

    def __init__(self, credential: Credential):
        ...

    def build_connection(self):
        ...

class SmtpConnector(Connector):

    def __init__(self, credential: Credential):
        self.credential = credential

    def get_credential(self):
        return self.credential

    def build_connection(self, instance):
        self.instance = instance
        return self.instance(
            host=self.credential.get_server(),
            port=self.credential.get_port()
        )
    
    def account_login(self):
        self.instance.starttls()
        return self.instance.login(
            self.credential.get_username(),
            self.credential.get_password()
        )
    
    def address_message(self, message):
        message["From"] = self.credential.get_username()
        message["To"] = self.credential.get_reciever()
        return message
    
    def send_email(self, message):
        return self.instance.sendmail(
            from_addr = self.credential.get_username(),
            to_addrs = self.credential.get_reciever(),
            msg = message.as_bytes()
        )

class MySqlConnector(Connector):
    def build_connection(self, credential: Credential):
        return super().build(credential)
    
class SshConnector(Connector):
    def build_connection(self, credential: Credential):
        return super().build(credential)