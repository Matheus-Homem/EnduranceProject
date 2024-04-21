from src.shared.connections.connectors import ConnectorType
from src.shared.connections.builder import build_connection

from functools import wraps


def establish_mysql_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with build_connection(connection_type=ConnectorType.SSH) as ssh_connection:
            with build_connection(connection_type=ConnectorType.MYSQL, ssh_connection=ssh_connection) as mysql_connection:
                cursor = mysql_connection.get_cursor()
                return func(cursor, *args, **kwargs)
    return wrapper