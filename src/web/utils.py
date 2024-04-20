from src.shared.connections.connectors import ConnectorType
from src.shared.connections.builder import build_connection
from src.shared.definition.statements import DataManipulationLanguage


def establish_mysql_connection(func):
    def wrapper(*args, **kwargs):
        with build_connection(
            connection_type=ConnectorType.SSH
        ) as ssh_connection:
            mysql_connection = build_connection(
                connection_type=ConnectorType.MYSQL,
                ssh_connection=ssh_connection
            )
            cursor = mysql_connection.get_cursor()
            DML = DataManipulationLanguage(cursor=cursor)
            result = func(DML, *args, **kwargs)
            mysql_connection.close_connection()
            ssh_connection.close_tunnel()
        return result
    return wrapper