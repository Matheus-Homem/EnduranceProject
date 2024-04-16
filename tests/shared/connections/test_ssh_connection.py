from src.shared.connections.credentials import SshCredential
from src.shared.connections.connectors import SshConnector
from src.shared.connections.builder import Connector, ConnectionType

from unittest.mock import patch, MagicMock
import unittest

class TestSshConnection(unittest.TestCase):

    @patch('src.shared.connections.builder.build_connection')
    @patch('src.shared.connections.builder.sshtunnel.SSHTunnelForwarder', autospec=True)
    def setUp(self, mock_sshtunnel, mock_build_connection):
        self.mock_sshtunnel = mock_sshtunnel
        self.mock_build_connection = mock_build_connection
        self.mock_ssh_credential = SshCredential()
        self.mock_ssh_connector = SshConnector(self.mock_ssh_credential)
        # self.mock_build_connection.connection = self.mock_ssh_connector.build_connection(lib=self.mock_sshtunnel)
        self.connection = self.mock_ssh_connector.build_connection(lib=self.mock_sshtunnel)

    def test_connector_enum(self):
        assert Connector.SSH.value == ConnectionType("ssh")

    @patch('src.shared.connections.builder.CONNECTION_CLASSES')
    def test_CONNECTION_CLASSES_dict(self, mock_CONNECTION_CLASSES):
        mock_CONNECTION_CLASSES.get = (SshConnector, SshCredential, self.mock_sshtunnel)
        ssh_connector_class, ssh_credential_class, ssh_lib_class = mock_CONNECTION_CLASSES.get
        assert ssh_connector_class == SshConnector
        assert ssh_credential_class == SshCredential
        assert ssh_lib_class == self.mock_sshtunnel
    
    def test_ssh_build_connection(self):
        assert isinstance(self.connection, SshConnector)
        assert isinstance(self.connection.credential, SshCredential)
        assert isinstance(self.connection.tunnel, type(self.mock_sshtunnel()))
    
    def test_ssh_tunnel(self):
        self.connection.start_tunnel()
        self.mock_sshtunnel.start.assert_called_once()
        assert self.connection.tunnel.is_active == True
        self.connection.close_tunnel()
        self.mock_sshtunnel.close.assert_called_once()
        assert self.connection.tunnel.is_active == False

if __name__ == '__main__':
    unittest.main()