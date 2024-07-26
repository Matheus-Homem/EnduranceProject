import unittest
from unittest.mock import patch, MagicMock
from src.shared.handlers import MySqlHandler

class TestMySQLHandler(unittest.TestCase):

    @patch.dict('os.environ', {'USER': 'EnduranceProject'})
    def test_is_prd_environment_remote(self):
        connector = MySqlHandler()
        self.assertTrue(connector._is_prd_environment())

    @patch.dict('os.environ', {}, clear=True)
    def test_is_prd_environment_local(self):
        connector = MySqlHandler()
        self.assertFalse(connector._is_prd_environment())

    @patch("src.shared.decorators.pymysql.connect")
    def test_establish_remote_connection(self, pymysql_connect_mock):
        mysql_connector = MySqlHandler()
        self.remote_connection = mysql_connector._establish_remote_connection()

        pymysql_connect_mock.assert_called_once()

    @patch("src.shared.decorators.pymysql.connect")
    @patch("src.shared.decorators.sshtunnel.SSHTunnelForwarder")
    def test_establish_local_connection(self, sshtunnel_mock, pymysql_connect_mock):
        mysql_connector = MySqlHandler()
        self.local_connection = mysql_connector._establish_local_connection()

        sshtunnel_mock.assert_called_once()
        pymysql_connect_mock.assert_called_once()

    

if __name__ == '__main__':
    unittest.main()
