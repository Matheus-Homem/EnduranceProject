from typing import Protocol
from dataclasses import dataclass
import os

class Credential(Protocol):
    
    def get_password(self) -> str:
        ...


class SmtpCredential(Credential):

    def __init__(self, getenv=os.getenv):
        self._PORT: int = 587
        self._SERVER: str = "smtp.gmail.com"
        self._SENDER: str = getenv("SMTP_SENDER_EMAIL")
        self._PASSWORD: str = getenv("SMTP_SENDER_PASSWORD")
        self._RECEIVER: str = getenv("SMTP_RECEIVER_EMAIL")

    def get_port(self) -> int:
        return self._PORT
    
    def get_server(self) -> str:
        return self._SERVER
    
    def get_sender(self) -> str:
        return self._SENDER
    
    def get_password(self) -> str:
        return self._PASSWORD
    
    def get_receiver(self) -> str:
        return self._RECEIVER


class MySqlCredential(Credential):
    

    def __init__(self, getenv=os.getenv):
        self._HOST: str = "127.0.0.1"
        self._USERNAME: str = getenv("MYSQL_USERNAME")
        self._PASSWORD: str = getenv("MYSQL_PASSWORD")
        self._DATABASE: str = getenv("MYSQL_DATABASE")

    def get_host(self) -> str:
        return self._HOST

    def get_username(self) -> str:
        return self._USERNAME

    def get_password(self) -> str:
        return self._PASSWORD

    def get_database(self) -> str:
        return f"{self._USERNAME}${self._DATABASE}"


@dataclass
class SshCredential(Credential):

    def __init__(self, getenv=os.getenv):
        self._HOST: str = "ssh.pythonanywhere.com"
        self._PORT: int = 3306
        self._USERNAME: str = getenv("SSH_USERNAME")
        self._PASSWORD: str = getenv("SSH_PASSWORD")

    def get_host(self) -> str:
        return self._HOST

    def get_port(self) -> int:
        return self._PORT

    def get_username(self) -> str:
        return self._USERNAME

    def get_password(self) -> str:
        return self._PASSWORD

    def get_hostname(self) -> str:
        return f"{self._USERNAME}.mysql.pythonanywhere-services.com"
