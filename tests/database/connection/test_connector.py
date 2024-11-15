import unittest
from unittest.mock import MagicMock, patch

from src.database.connection.connector import DatabaseConnector


class TestDatabaseConnector(unittest.TestCase):

    def setUp(self):
        self.database_connector = DatabaseConnector(use_production_db=True)
        self.database_connector.logger = MagicMock()

        self.mock_mysql_keys = {
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "database": "test_db",
        }

        self.mock_ssh_keys = {
            "host": "ssh_host",
            "username": "ssh_user",
            "password": "ssh_password",
            "hostname": "remote_host",
            "port": 22,
        }

    @patch("src.database.connection.connector.PRD", "EnduranceProject")
    def test_is_prd_environment(self):
        assert self.database_connector._is_prd_environment() == True

    @patch("src.database.connection.connector.PRD", "")
    def test_is_local_environment(self):
        assert self.database_connector._is_prd_environment() == False

    @patch("src.database.connection.connector.PRD", "EnduranceProject")
    @patch("src.database.connection.connector.create_engine")
    @patch("src.database.connection.connector.scoped_session")
    def test_can_create_remote_engine_with_sucess(self, mock_scoped_session, mock_create_engine):
        mock_mysql_credentials = MagicMock()
        mock_ssh_credentials = MagicMock()

        self.database_connector._create_engine(mock_mysql_credentials, mock_ssh_credentials)
        mock_scoped_session.assert_called_once()
        mock_create_engine.assert_called_once()

    @patch("src.database.connection.connector.PRD", "")
    @patch("src.database.connection.connector.DatabaseConnector._get_local_engine_url")
    def test_exception_when_create_local_engine(self, mock_get_local_engine_url):
        mock_mysql_credentials = MagicMock()
        mock_ssh_credentials = MagicMock()
        mock_get_local_engine_url.side_effect = Exception("Test exception")

        with self.assertRaises(Exception) as context:
            self.database_connector._create_engine(mock_mysql_credentials, mock_ssh_credentials)

        self.assertEqual(str(context.exception), "Test exception")

    @patch("src.database.connection.connector.sshtunnel.SSHTunnelForwarder")
    def test_can_get_local_engine_url(self, mock_SSHTunnelForwarder):
        mock_tunnel = MagicMock()
        mock_tunnel.local_bind_port = 12345
        mock_SSHTunnelForwarder.return_value = mock_tunnel

        result = self.database_connector._get_local_engine_url(self.mock_mysql_keys, self.mock_ssh_keys)

        mock_SSHTunnelForwarder.assert_called_once_with(
            ssh_address_or_host=self.mock_ssh_keys.get("host"),
            ssh_username=self.mock_ssh_keys.get("username"),
            ssh_password=self.mock_ssh_keys.get("password"),
            remote_bind_address=(
                self.mock_ssh_keys.get("hostname"),
                self.mock_ssh_keys.get("port"),
            ),
        )
        mock_tunnel.start.assert_called_once()
        self.assertEqual(
            result,
            self.database_connector._construct_engine_url(self.mock_mysql_keys, "localhost:12345"),
        )

    @patch("src.database.connection.connector.sshtunnel.SSHTunnelForwarder")
    def test_exception_when_get_local_engine_url(self, mock_SSHTunnelForwarder):
        mock_mysql_keys = MagicMock()
        mock_ssh_keys = MagicMock()

        mock_SSHTunnelForwarder.side_effect = Exception("Test exception")

        with self.assertRaises(Exception) as context:
            self.database_connector._get_local_engine_url(mock_mysql_keys, mock_ssh_keys)

        self.assertEqual(str(context.exception), "Test exception")
        self.database_connector.logger.error.assert_called_once_with("Failed to start SSH tunnel: Test exception")

    @patch("src.database.connection.connector.DatabaseConnector._create_engine")
    def test_can_get_new_session(self, mock_create_engine):
        mock_mysql_keys = MagicMock()
        mock_ssh_keys = MagicMock()

        session = self.database_connector.get_session(mock_mysql_keys, mock_ssh_keys)

        mock_create_engine.assert_called_once_with(mock_mysql_keys, mock_ssh_keys)

    @patch("src.database.connection.connector.DatabaseConnector._create_engine")
    def test_can_get_existing_session(self, mock_create_engine):
        self.database_connector.Session = MagicMock()

        session = self.database_connector.get_session(None, None)

        mock_create_engine.assert_not_called()
        self.database_connector.logger.info.assert_not_called()

    def test_can_close_connection(self):
        self.database_connector.Session = MagicMock()
        self.database_connector.engine = MagicMock()
        self.database_connector.ssh_tunnel = MagicMock()

        self.database_connector.close()

        self.database_connector.Session.remove.assert_called_once()
        self.database_connector.logger.info.assert_any_call("Session closed successfully")

        self.database_connector.engine.dispose.assert_called_once()

        self.database_connector.ssh_tunnel.stop.assert_called_once()
        self.database_connector.logger.info.assert_any_call("SSH tunnel stopped successfully")
