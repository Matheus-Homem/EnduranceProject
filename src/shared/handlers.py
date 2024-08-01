import sshtunnel
from pymysql import connect

from src.shared.logger import Logger
from src.shared.credentials import PRD, MySqlCredential, SshCredential

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


class StatmentType:
    RESULT = "result"
    COMMIT = "commit"


class MySqlHandler:

    def __init__(self, logger=Logger()):
        self.mysql_credentials = MySqlCredential().get_all_credentials()
        self.logger = logger.get_logger()

    def _is_prd_environment(self) -> bool:
        return True if PRD == "EnduranceProject" else False

    def _establish_remote_connection(self) -> "connect":
        connection = connect(
            user=self.mysql_credentials.get("username"),
            passwd=self.mysql_credentials.get("password"),
            host=self.mysql_credentials.get("hostname"),
            db=self.mysql_credentials.get("database"),
            connect_timeout=60,
        )
        print("Remote connection establish with success")
        return connection

    def _establish_local_connection(self) -> "connect":
        ssh_credentials = SshCredential().get_all_credentials()

        ssh_tunnel = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=ssh_credentials.get("host"),
            ssh_username=ssh_credentials.get("username"),
            ssh_password=ssh_credentials.get("password"),
            remote_bind_address=(
                ssh_credentials.get("hostname"),
                ssh_credentials.get("port"),
            ),
        )
        ssh_tunnel.start()
        connection = connect(
            user=self.mysql_credentials.get("username"),
            passwd=self.mysql_credentials.get("password"),
            host=self.mysql_credentials.get("host"),
            port=ssh_tunnel.local_bind_port,
            db=self.mysql_credentials.get("database"),
            connect_timeout=60,
        )
        print("Local connection establish with success")
        return connection

    def _close_connection(self, connection, cursor) -> None:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Connection closed")

    def _validate_statement(self, statement: str) -> None:
        available_statements = ["SELECT", "INSERT", "UPDATE", "DELETE"]
        command = statement.split(" ")[0].upper()
        if command not in available_statements:
            raise ValueError(
                "Statement has a command not supported. Please use one of the following: SELECT, INSERT, UPDATE, DELETE"
            )

    def _set_statement_type(self, statement: str) -> StatmentType:
        command = statement.split(" ")[0].upper()
        return StatmentType.RESULT if command == "SELECT" else StatmentType.COMMIT

    def execute(self, statement) -> None:
        """
        Examples:
        - 'INSERT INTO local_test (data) VALUES (\'{"key1": "value1", "key2": "value2"}\');'
        - 'UPDATE local_test SET data = \'{"key1": "new_value"}\' WHERE id = 1;'
        - 'DELETE FROM local_test WHERE id = 1;'
        - 'SELECT * FROM local_test;'
        - 'SELECT COUNT(*) FROM local_test;'
        """
        connection = (
            self._establish_remote_connection()
            if self._is_prd_environment()
            else self._establish_local_connection()
        )
        cursor = connection.cursor()
        self._validate_statement(statement)
        statement_type = self._set_statement_type(statement)
        if statement_type == StatmentType.RESULT:
            cursor.execute(statement)
            result = cursor.fetchall()
            self._close_connection(connection, cursor)
            return result
        elif statement_type == StatmentType.COMMIT:
            cursor.execute(statement)
            connection.commit()
            self._close_connection(connection, cursor)
