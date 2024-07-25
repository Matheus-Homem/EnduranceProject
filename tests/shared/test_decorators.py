import unittest
from unittest.mock import patch, MagicMock
from src.shared.decorators import establish_mysql_connection

class TestEstablishMySQLConnection(unittest.TestCase):

    def setUp(self):
        self.func = MagicMock(return_value="result")

    
    
    @patch('src.env.helpers.is_prd_environment', return_value=True)
    @patch('src.shared.credentials.MySqlCredential')
    @patch('pymysql.connect')
    def test_prd_environment(self, mock_connect , MockMySqlCredential):
        print(mock_connect)
        MockMySqlCredential().get_all_credentials.return_value = {
            "username": "user",
            "password": "pass",
            "hostname": "host",
            "database": "db"
        }
        
        from src.shared.credentials import MySqlCredential, SshCredential
        print(MySqlCredential.get_all_credentials())
        # mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # mock_connection.cursor.return_value = mock_cursor

        decorated_func = establish_mysql_connection(self.func)
        result = decorated_func()

        mock_connect.assert_called_once_with(
            user="user",
            passwd="pass",
            host="host",
            db="db"
        )
        # mock_cursor.execute.assert_called_once()
        # mock_connection.commit.assert_called_once()
        # self.func.assert_called_once_with(mock_cursor)
        self.assertEqual(result, "result")
        print("test_prd_environment passed")

    # @patch('src.shared.decorators.is_prd_environment', return_value=False)
    # @patch('src.shared.decorators.MySqlCredential')
    # @patch('src.shared.decorators.SshCredential')
    # @patch('src.shared.decorators.sshtunnel.SSHTunnelForwarder')
    # @patch('src.shared.decorators.pymysql.connect')
    # def test_non_prd_environment(self, mock_connect, MockSSHTunnelForwarder, MockSshCredential, MockMySqlCredential, mock_is_prd_environment):
    #     mock_cursor = MagicMock()
    #     mock_connection = MagicMock()
    #     mock_tunnel = MagicMock()
    #     mock_connect.return_value = mock_connection
    #     mock_connection.cursor.return_value = mock_cursor
    #     MockSSHTunnelForwarder.return_value.__enter__.return_value = mock_tunnel
    #     mock_tunnel.local_bind_port = 3306
    #     MockMySqlCredential().get_all_credentials.return_value = {
    #         "username": "user",
    #         "password": "pass",
    #         "host": "localhost",
    #         "database": "db"
    #     }
    #     MockSshCredential().get_all_credentials.return_value = {
    #         "host": "ssh_host",
    #         "username": "ssh_user",
    #         "password": "ssh_pass",
    #         "hostname": "remote_host",
    #         "port": 22
    #     }

    #     decorated_func = establish_mysql_connection(self.func)
    #     result = decorated_func()

    #     MockSSHTunnelForwarder.assert_called_once_with(
    #         ssh_address_or_host="ssh_host",
    #         ssh_username="ssh_user",
    #         ssh_password="ssh_pass",
    #         remote_bind_address=("remote_host", 22)
    #     )
    #     mock_connect.assert_called_once_with(
    #         user="user",
    #         passwd="pass",
    #         host="localhost",
    #         port=3306,
    #         db="db"
    #     )
    #     mock_cursor.execute.assert_called_once()
    #     mock_connection.commit.assert_called_once()
    #     self.func.assert_called_once_with(mock_cursor)
    #     self.assertEqual(result, "result")
    #     print("test_non_prd_environment passed")

if __name__ == '__main__':
    unittest.main()
