from typing import Protocol
from dataclasses import dataclass
import os

class Credential(Protocol):
    pass

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
    
    def get_username(self) -> str:
        return self._SENDER_EMAIL
    
    def get_password(self) -> str:
        return self._SENDER_PASSWORD
    
    def get_reciever(self) -> str:
        return self._RECIEVER_EMAIL
    

@dataclass
class MySqlCredential(Credential):
    _HOST: str = "localhost"
    _PORT: int = 3306


@dataclass
class SshCredential(Credential):
    _HOST: str = "localhost"
    _PORT: int = 22