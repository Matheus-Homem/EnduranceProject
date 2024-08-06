from src.shared.credentials import MySqlCredential, SshCredential
from src.shared.database.connector import DatabaseConnector
from src.shared.database.executor import DatabaseExecutor


def initialize_database_setup() -> tuple[DatabaseExecutor, DatabaseConnector]:
    connector = DatabaseConnector()
    session = connector.get_session(
        mysql_credentials=MySqlCredential(), ssh_credentials=SshCredential()
    )
    return DatabaseExecutor(session=session), connector
