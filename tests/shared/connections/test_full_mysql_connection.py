from src.shared.connections.credentials import MySqlCredential, SshCredential
from src.shared.connections.connectors import MySqlConnector, SshConnector
from src.shared.connections.builder import Connector, build_connection

import unittest
from unittest.mock import patch, MagicMock


class TestFullMySqlConnection(unittest.TestCase):

    @patch('src.shared.connections.builder.mysql.connector.connect')
    @patch('src.shared.connections.builder.sshtunnel.SSHTunnelForwarder')
    def test_build_connection(self, mock_tunnel, mock_mysql_connector):

        ssh_credential = SshCredential()
        
        ssh_connection = SshConnector(ssh_credential).build_connection(mock_tunnel)

        print("ssh_connection: ",ssh_connection)
        print(type(ssh_connection))
        
        print(type(Connector.SSH))
        print(type(build_connection(Connector.SSH)))
        assert ssh_connection == build_connection(Connector.SSH)

        ssh_connection.start_tunnel()
        ssh_connection.close_tunnel()
        
        mysql_credential = MySqlCredential()

        mysql_connection = MySqlConnector(mysql_credential).build_connection(mock_mysql_connector)

        assert mysql_connection == build_connection(Connector.MYSQL)


        ssh_connection.start_tunnel.assert_called_once()
        ssh_connection.close_tunnel.assert_called_once()
        
        #self.assertEqual(build_connection(Connector.SSH), SshConnector(SshCredential()).build_connection(sshtunnel.SSHTunnelForwarder)) 
        
        # # Arrange
        # mock_credential = MagicMock(spec=Credential)
        # mock_instance = MagicMock()
        # mock_tunnel = MagicMock()
        # mock_tunnel.start_tunnel = MagicMock()
        # mock_connector = MySqlConnector(mock_credential)

        # # Act
        # mock_connector.build_connection(mock_instance, mock_tunnel)

        # # Assert
        # mock_tunnel.start_tunnel.assert_called_once()
        # mock_instance.assert_called_once_with(
        #     user=mock_credential.get_host(),
        #     password=mock_credential.get_password(),
        #     host=mock_credential.get_username(),
        #     port=mock_tunnel.local_bind_port,
        #     db=mock_credential.get_database()
        # )

if __name__ == '__main__':
    unittest.main()