from src.shared.connections.connectors import SshConnector
from src.shared.connections.credentials import SshCredential

import unittest
from unittest.mock import patch, MagicMock


class TestSshConnection(unittest.TestCase):

    @patch('sshtunnel.SSHTunnelForwarder')
    def test_ssh_connector(self, mock_tunnel_forwarder):
        mock_tunnel = MagicMock()
        mock_tunnel.is_active = False
        mock_tunnel.start.side_effect = lambda: setattr(mock_tunnel, 'is_active', True)
        mock_tunnel.local_bind_port = 2624050664384
        mock_tunnel_forwarder.return_value = mock_tunnel

        mock_credential = MagicMock()
        ssh_connector = SshConnector(mock_credential)

        with ssh_connector as conn:
            self.assertIsInstance(conn, SshConnector)
            self.assertEqual(conn.credential, mock_credential)
            ssh_connector.start_tunnel()
            mock_tunnel.start.assert_called_once()
            self.assertTrue(mock_tunnel.is_active)
            self.assertEqual(ssh_connector.get_local_bind_port(), 2624050664384)

if __name__ == '__main__':
    unittest.main()