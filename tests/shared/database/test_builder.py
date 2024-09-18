import unittest
from unittest.mock import MagicMock, patch

from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.executor import DatabaseExecutor


class TestDatabaseExecutorBuilder(unittest.TestCase):
    @patch("src.shared.database.builder.DatabaseConnector")
    @patch("src.shared.database.builder.MySqlCredential")
    @patch("src.shared.database.builder.SshCredential")
    def test_database_executor_builder(self, MockSshCredential, MockMySqlCredential, MockDatabaseConnector):
        mock_connector = MockDatabaseConnector.return_value
        mock_session = MagicMock()
        mock_connector.get_session.return_value = mock_session

        builder = DatabaseExecutorBuilder(use_production_db=False)

        MockDatabaseConnector.assert_called_once()
        mock_connector.get_session.assert_called_once_with(
            mysql_credentials=MockMySqlCredential.return_value,
            ssh_credentials=MockSshCredential.return_value,
        )
        self.assertEqual(builder.session, mock_session)

        self.assertIsInstance(builder.executor, DatabaseExecutor)
        self.assertEqual(builder.executor.session, mock_session)

        with builder as executor:
            self.assertEqual(executor, builder.executor)
        mock_connector.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
