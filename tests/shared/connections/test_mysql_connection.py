from src.shared.connections.credentials import MySqlCredential
from src.shared.connections.connectors import MySqlConnector
from src.shared.connections.builder import build_connection, Connector

from unittest.mock import patch, MagicMock
import unittest


class TestMySqlConnection(unittest.TestCase):
    
    @patch("sshtunnel.SSHTunnelForwarder")
    @patch("mysql.connector.connect")
    def setUp(self, mock_mysql_connect, mock_sshtunnel):
        self.mock_sshtunnel = mock_sshtunnel
        self.mock_sshtunnel.start_tunnel.return_value = MagicMock()
        self.mock_mysql_connect = mock_mysql_connect
        self.mysql_connection = MySqlConnector(MySqlCredential()).build_connection(lib=self.mock_mysql_connect, tunnel=self.mock_sshtunnel)

    def test_mysql_build_connection(self):
        connection = build_connection(Connector.MYSQL, tunnel=self.mock_sshtunnel)

        self.assertIsInstance(connection, MySqlConnector)
        self.assertIsInstance(connection.credential, MySqlCredential)
        self.assertEqual(connection.credential, self.mysql_connection.credential)
        #self.assertEqual(connection.tunnel, self.ssh_connection.tunnel)
        


if __name__ == '__main__':
    unittest.main()