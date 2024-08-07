from src.shared.credentials import MySqlCredential, SshCredential
from src.shared.database.connector import DatabaseConnector
from src.shared.database.executor import DatabaseExecutor


class DatabaseExecutorBuilder:
    def __init__(self) -> None:
        self.connector = DatabaseConnector()
        self.session = self.connector.get_session(
            mysql_credentials=MySqlCredential(), ssh_credentials=SshCredential()
        )
        self.executor = DatabaseExecutor(session=self.session)

    def __enter__(self) -> DatabaseExecutor:
        return self.executor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()
        return False
