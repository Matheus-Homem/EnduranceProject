from src.shared.connections.connectors import Connector, SmtpConnector, SshConnector, MySqlConnector
from src.shared.connections.credentials import Credential, SmtpCredential, SshCredential, MySqlCredential

from typing import NewType, Type, Tuple, Union, Dict
from enum import Enum
import mysql.connector
import sshtunnel
import smtplib

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

ConnectionType = NewType('ConnectionType', str)

CONNECTION_CLASSES: Dict[ConnectionType, Type[Tuple[Connector, Credential, Union[mysql.connector.connect, sshtunnel.SSHTunnelForwarder, smtplib.SMTP]]]] = {
    ConnectionType("smtp"): (SmtpConnector, SmtpCredential, smtplib.SMTP),
    ConnectionType("ssh"): (SshConnector, SshCredential, sshtunnel.SSHTunnelForwarder),
    ConnectionType("mysql"): (MySqlConnector, MySqlCredential, mysql.connector.connect),
}

class Connector(Enum):
    SMTP = ConnectionType("smtp")
    SSH = ConnectionType("ssh")
    MYSQL = ConnectionType("mysql")


def build_connection(connection_type: ConnectionType, **kwargs):
    """
    Builds a connection using the specified connection type.

    Args:
        connection_type (ConnectionType): The key for the connector and credential classes to use.
        **kwargs: Arbitrary keyword arguments to be passed to the connector's build method.

    Returns:
        The built connection object.

    Raises:
        AttributeError: If the connection_type is not recognized.
    """
    classes = CONNECTION_CLASSES.get(connection_type.value)

    if classes is None:
        raise AttributeError(f"Unrecognized connection_type '{connection_type}'")

    connector_class, credential_class, lib_class = classes
    credential = credential_class()
    connector = connector_class(credential)

    return connector.build_connection(lib=lib_class, **kwargs)