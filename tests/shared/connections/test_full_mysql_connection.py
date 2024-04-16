from src.shared.connections.credentials import SshCredential
from src.shared.connections.connectors import SshConnector
from src.shared.connections.builder import Connector, ConnectionType, CONNECTION_CLASSES, build_connection

import unittest
import sshtunnel

class TestSshConnection(unittest.TestCase):
    # TODO: implement Mock/patch

    def setUp(self) -> None:
        self.connection = build_connection(Connector.SSH)

    def test_connector_enum(self):
        assert Connector.SSH.value == ConnectionType("ssh")

    def test_CONNECTION_CLASSES_dict(self):
        ssh_connector_class, ssh_credential_class, ssh_lib_class = CONNECTION_CLASSES.get(Connector.SSH.value)
        assert ssh_connector_class == SshConnector
        assert ssh_credential_class == SshCredential
        assert ssh_lib_class == sshtunnel.SSHTunnelForwarder
    
    def test_ssh_build_connection(self):
        assert isinstance(self.connection, SshConnector)
        assert isinstance(self.connection.credential, SshCredential)
        assert isinstance(self.connection.tunnel, sshtunnel.SSHTunnelForwarder)
    
    def test_ssh_tunnel(self):
        self.connection.tunnel.start()
        assert self.connection.tunnel.is_active == True
        self.connection.tunnel.close()
        assert self.connection.tunnel.is_active == False

if __name__ == '__main__':
    unittest.main()