from dataclasses import dataclass
from os import getenv
from typing import Any, Dict, Protocol

from dotenv import load_dotenv

load_dotenv()

PRD = getenv("USER")

class Credential(Protocol):

    def get_all_credentials(self) -> Dict[str, Any]: ...


@dataclass
class SshCredential(Credential):
    HOST: str = "ssh.pythonanywhere.com"
    PORT: int = 3306
    USERNAME: str = getenv("SSH_USERNAME")
    PASSWORD: str = getenv("SSH_PASSWORD")
    HOSTNAME: str = f"{USERNAME}.mysql.pythonanywhere-services.com"

    def get_all_credentials(self) -> Dict[str, Any]:
        return {
            "host": self.HOST,
            "port": self.PORT,
            "username": self.USERNAME,
            "password": self.PASSWORD,
            "hostname": self.HOSTNAME,
        }


@dataclass
class MySqlCredential(Credential):
    USERNAME: str = getenv("MYSQL_USERNAME")
    PASSWORD: str = getenv("MYSQL_PASSWORD")
    DATABASE_NAME: str = getenv("MYSQL_DATABASE")
    DB: str = f"{USERNAME}${DATABASE_NAME}"
    HOST: str = "127.0.0.1"
    HOSTNAME: str = f"{USERNAME}.mysql.pythonanywhere-services.com"

    def get_all_credentials(self) -> Dict[str, Any]:
        return {
            "host": self.HOST,
            "username": self.USERNAME,
            "password": self.PASSWORD,
            "database": self.DB,
            "hostname": self.HOSTNAME,
        }
