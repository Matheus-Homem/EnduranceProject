from typing import Protocol
from dataclasses import dataclass
import os

class Credential(Protocol):
    
    def get_password(self) -> str:
        ...

@dataclass
class SmtpCredential(Credential):
    _PORT: int = 587
    _SERVER: str = "smtp.gmail.com"
    _SENDER_EMAIL: str = os.getenv("SMTP_SENDER_EMAIL")
    _SENDER_PASSWORD: str = os.getenv("SMTP_SENDER_PASSWORD")
    _RECIEVER_EMAIL: str = os.getenv("SMTP_RECIEVER_EMAIL")

    def get_port(self) -> int:
        return self._PORT
    
    def get_server(self) -> str:
        return self._SERVER
    
    def get_sender(self) -> str:
        return self._SENDER_EMAIL
    
    def get_password(self) -> str:
        return self._SENDER_PASSWORD
    
    def get_reciever(self) -> str:
        return self._RECIEVER_EMAIL
    

@dataclass
class MySqlCredential(Credential):
    _HOST: str = "127.0.0.1"
    _USERNAME: str = os.getenv("MYSQL_USERNAME")
    _PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    _DATABASE: str = os.getenv("MYSQL_DATABASE")

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
    _HOST: str = "ssh.pythonanywhere.com"
    _PORT: int = 3306
    _USERNAME: str = os.getenv("SSH_USERNAME")
    _PASSWORD: str = os.getenv("SSH_PASSWORD")

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