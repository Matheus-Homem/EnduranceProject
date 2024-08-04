import sshtunnel
from pymysql import connect

from src.shared.credentials import PRD, MySqlCredential, SshCredential
from src.shared.logger import LoggingManager

sshtunnel.SSH_TIMEOUT = 20.0
sshtunnel.TUNNEL_TIMEOUT = 20.0


class StatmentType:
    RESULT = "result"
    COMMIT = "commit"


class MySqlHandler:

    def __init__(self, logging_manager: LoggingManager):
        self.mysql_credentials = MySqlCredential().get_all_credentials()
        logging_manager.set_class_name(__class__.__name__)
        self.logger = logging_manager.get_logger()

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
        return connection

    def _close_connection(self, connection, cursor) -> None:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    def _validate_statement(self, statement: str) -> None:
        try:
            command = statement.split(" ")[0].upper()
            if command not in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
                raise ValueError("Statement has a command not supported. Please use one of the following: SELECT, INSERT, UPDATE, DELETE")
        except Exception as e:
            self.logger.error(f"Failed to create engine: {e}")
            raise e

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
        if self._is_prd_environment():
            self.logger.info("Establishing remote connection")
            connection = self._establish_remote_connection()
            self.logger.info("Remote connection successfully established")
        else:
            self.logger.info("Establishing local connection")
            connection = self._establish_local_connection()
            self.logger.info("Local connection successfully established")
        cursor = connection.cursor()
        self._validate_statement(statement)
        statement_type = self._set_statement_type(statement)
        self.logger.info("Executing statement")
        if statement_type == StatmentType.RESULT:
            cursor.execute(statement)
            result = cursor.fetchall()
            self._close_connection(connection, cursor)
            self.logger.info("Connection closed")
            return result
        elif statement_type == StatmentType.COMMIT:
            cursor.execute(statement)
            connection.commit()
            self._close_connection(connection, cursor)
            self.logger.info("Connection closed")
