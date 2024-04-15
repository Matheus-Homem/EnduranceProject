from typing import NewType, Type, Tuple, Dict
from src.shared.connections.connectors import Connector, SmtpConnector, SshConnector, MySqlConnector
from src.shared.connections.credentials import Credential, SmtpCredential, SshCredential, MySqlCredential

# Define a new type for the connection keys
ConnectionType = NewType('ConnectionType', str)

# Mapping of ConnectionType keys to Connector and Credential classes
CONNECTION_CLASSES: Dict[ConnectionType, Type[Tuple[Connector, Credential]]] = {
    ConnectionType("smtp"): (SmtpConnector, SmtpCredential),
    ConnectionType("ssh"): (SshConnector, SshCredential),
    ConnectionType("mysql"): (MySqlConnector, MySqlCredential),
}

def build_connection(connection_type: ConnectionType, **kwargs):
    """
    Builds a connection using the specified connection type.

    Args:
        connection_type (ConnectionType): The key for the connector and credential classes to use.
        **kwargs: Arbitrary keyword arguments to be passed to the connector's build method.

    Returns:
        The built connection object.

    Raises:
        ValueError: If the connection_type is not recognized.
    """
    classes = CONNECTION_CLASSES.get(connection_type)

    if classes is None:
        raise ValueError(f"Unrecognized connection_type '{connection_type}'")

    connector_class, credential_class = classes
    credential = credential_class()
    connector = connector_class(credential)

    return connector.build_connection(**kwargs)