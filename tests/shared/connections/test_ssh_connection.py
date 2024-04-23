from src.shared.connections.connectors import SshConnector

import sshtunnel
import unittest
from unittest.mock import patch, MagicMock

class TestSshConnection(unittest.TestCase):

    
    @patch('sshtunnel.SSHTunnelForwarder')
    def setUp(self, mock_get_library):
        self.tunnel = MagicMock()
        mock_credential = MagicMock()
        self.mock_get_library = mock_get_library
        self.mock_get_library.return_value = self.tunnel
        mock_credential.get_host.return_value = 'mock_host'
        mock_credential.get_username.return_value = 'mock_username'
        mock_credential.get_password.return_value = 'mock_password'
        mock_credential.get_hostname.return_value = 'mock_hostname'
        mock_credential.get_port.return_value = 666
        self.connector = SshConnector(mock_credential)
        self.connector.build_connection()

    @patch('src.shared.connections.credentials.SshCredential')
    def test_get_library(self, mock_ssh_credential):
        self.mock_ssh_credential = mock_ssh_credential
        ssh_connector = SshConnector(self.mock_ssh_credential.return_value)
        ssh_library = ssh_connector.get_library()
        self.assertEqual(ssh_library, sshtunnel.SSHTunnelForwarder)
        self.assertEqual(sshtunnel.SSH_TIMEOUT, 5.0)
        self.assertEqual(sshtunnel.TUNNEL_TIMEOUT, 5.0)

    def test_build_connection(self):
        result = self.connector.build_connection()
        self.mock_get_library.assert_called_once()
        self.assertIsInstance(result, SshConnector)
        self.assertEqual(result, self.connector)
        self.assertEqual(vars(self.connector.tunnel).get('ssh_host'), 'mock_host')
        self.assertEqual(vars(self.connector.tunnel).get('ssh_username'), 'mock_username')
        self.assertEqual(vars(self.connector.tunnel).get('ssh_password'), 'mock_password')
        self.assertEqual(vars(self.connector.tunnel).get('_remote_binds'), [('mock_hostname', 666)])

    def test_start_tunnel(self):
        def start_side_effect():
            self.tunnel.is_active = True
        self.tunnel.is_active = False
        self.tunnel.start.side_effect = start_side_effect
        self.connector.start_tunnel()
        self.tunnel.start.assert_called_once()
        self.assertTrue(self.tunnel.is_active)

    def test_close_tunnel(self):
        def close_side_effect():
            self.tunnel.is_active = False
        self.tunnel.is_active = True
        self.tunnel.close.side_effect = close_side_effect
        self.connector.close_tunnel()
        self.tunnel.close.assert_called_once()
        self.assertFalse(self.tunnel.is_active)

if __name__ == '__main__':
    unittest.main()