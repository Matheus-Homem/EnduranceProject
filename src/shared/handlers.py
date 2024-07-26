import pymysql
import sshtunnel

from src.shared.credentials import PRD, MySqlCredential, SshCredential

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


class MySqlHandler:

    def __init__(self):
        self.mysql_credentials = MySqlCredential().get_all_credentials()

    def _is_prd_environment(self) -> bool:
        return True if PRD == "EnduranceProject" else False

    def _establish_remote_connection(self):
        connection = pymysql.connect(
            user=self.mysql_credentials.get("username"),
            passwd=self.mysql_credentials.get("password"),
            host=self.mysql_credentials.get("host"),
            db=self.mysql_credentials.get("database"),
            connect_timeout=60,
        )
        print("Remote connection establish with success")
        return connection

    def _establish_local_connection(self):
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
        connection = pymysql.connect(
            user=self.mysql_credentials.get("username"),
            passwd=self.mysql_credentials.get("password"),
            host=self.mysql_credentials.get("host"),
            port=ssh_tunnel.local_bind_port,
            db=self.mysql_credentials.get("database"),
            connect_timeout=60,
        )
        print("Local connection establish with success")
        return connection

    def _close_connection(self, connection, cursor):
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Connection closed")

    def get_statement(self, statement: str):
        """
        Examples:
        - 'INSERT INTO local_test (data) VALUES (\'{"key1": "value1", "key2": "value2"}\');'
        - 'UPDATE local_test SET data = \'{"key1": "new_value"}\' WHERE id = 1;'
        - 'DELETE FROM local_test WHERE id = 1;'
        - 'SELECT * FROM local_test;'
        - 'SELECT COUNT(*) FROM local_test;'
        """
        available_statements = ["SELECT", "INSERT", "UPDATE", "DELETE"]
        command = statement.split(" ")[0].upper()
        if command not in available_statements:
            raise ValueError("Invalid statement")
        if command == "SELECT":
            self.result_statement = statement
        else:
            self.statement = statement

    def execute(self):
        if self._is_prd_environment():
            connection = self._establish_remote_connection()
        else:
            connection = self._establish_local_connection()

        cursor = connection.cursor()
        if self.result_statement:
            cursor.execute(self.result_statement)
            result = cursor.fetchall()
            self._close_connection(connection, cursor)
            return result
        elif self.statement:
            cursor.execute(self.statement)
            connection.commit()
            self._close_connection(connection, cursor)
        else:
            raise ValueError("No valid statement provided")
