from src.shared.connections.credentials import SshCredential
from src.shared.connections.connectors import SshConnector
# from src.shared.connections.builder import Connector, ConnectionType

from unittest.mock import patch
import unittest

class TestSshConnection(unittest.TestCase):

    @patch('sshtunnel.SSHTunnelForwarder')
    def setUp(self, mock_sshtunnel):
        self.mock_sshtunnel = mock_sshtunnel
        self.mock_sshtunnel.return_value.start.side_effect = self._activate_tunnel
        self.mock_sshtunnel.return_value.close.side_effect = self._deactivate_tunnel
        self.ssh_connection = SshConnector(SshCredential()).build_connection(lib=self.mock_sshtunnel)

    def _activate_tunnel(self):
        self.mock_sshtunnel.return_value.is_active = True

    def _deactivate_tunnel(self):
        self.mock_sshtunnel.return_value.is_active = False        

    # def test_connection_classes_dict(self):
    #     mock_connection_classes_dict = {
    #         ConnectionType("ssh"): (SshConnector, SshCredential, self.mock_sshtunnel)
    #     }
    #     ssh_connector_class, ssh_credential_class, ssh_lib_class = mock_connection_classes_dict.get(Connector.SSH.value)
    #     # self.assertEqual(Connector.SSH.value, ConnectionType("ssh"))
    #     self.assertEqual(ssh_connector_class, SshConnector)
    #     self.assertEqual(ssh_credential_class, SshCredential)
    #     self.assertEqual(ssh_lib_class, self.mock_sshtunnel)
    
    def test_ssh_build_connection(self):
        ssh_credential = SshCredential()
        ssh_connector = SshConnector(ssh_credential)
        connection = ssh_connector.build_connection(lib=self.mock_sshtunnel)
        
        self.assertIsInstance(connection, SshConnector)
        self.assertIsInstance(connection.credential, SshCredential)
        self.assertEqual(connection.credential, self.ssh_connection.credential)
        self.assertEqual(connection.tunnel, self.mock_sshtunnel.return_value)

    def test_tunnel_activation(self):
        self.mock_sshtunnel.return_value.is_active = False
        self.ssh_connection.start_tunnel()
        self.ssh_connection.tunnel.start.assert_called_once()
        self.assertTrue(self.mock_sshtunnel.return_value.is_active)
    
    def test_tunnel_deactivation(self):
        self.mock_sshtunnel.return_value.is_active = True
        self.ssh_connection.close_tunnel()
        self.ssh_connection.tunnel.close.assert_called_once()
        self.assertFalse(self.mock_sshtunnel.return_value.is_active)

if __name__ == '__main__':
    unittest.main()