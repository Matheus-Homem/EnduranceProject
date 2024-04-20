from src.shared.connections.connectors import Connector, SmtpConnector, SshConnector, MySqlConnector, ConnectionType
from src.shared.connections.credentials import Credential, SmtpCredential, SshCredential, MySqlCredential

from typing import Type, Tuple, Dict


CONNECTION_CLASSES: Dict[ConnectionType, Type[Tuple[Connector, Credential]]] = {
    ConnectionType("smtp"): (SmtpConnector, SmtpCredential),
    ConnectionType("ssh"): (SshConnector, SshCredential),
    ConnectionType("mysql"): (MySqlConnector, MySqlCredential),
}

def build_connection(connection_type: ConnectionType, **kwargs) -> Connector:
    
    try:
        classes = CONNECTION_CLASSES.get(connection_type.value)
    except AttributeError:
        raise AttributeError(f"Unrecognized connection_type '{connection_type.value}'")
    else:
        classes = CONNECTION_CLASSES.get(connection_type.value)
        connector_class, credential_class = classes
        credential = credential_class()
        conn_instance = connector_class(credential, **kwargs)
        return conn_instance