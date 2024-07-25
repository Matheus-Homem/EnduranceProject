import unittest
from unittest.mock import MagicMock, patch
from src.shared.database.operations import DatabaseOperations


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        self.cursor_mock = MagicMock()

    @patch("src.shared.database.operations.establish_mysql_connection", lambda func: func)
    def test_execute_command(self):
        command = 'INSERT INTO local_test (data) VALUES (\'{"key1": "value1", "key2": "value2"}\');'

        @canc
        DatabaseOperations.execute_command(self.cursor_mock, command)

        self.cursor_mock.execute.assert_called_once_with(command)

    @patch("src.shared.database.operations.establish_mysql_connection", lambda func: func)
    def test_select_data(self):
        command = "SELECT * FROM local_test;"
        expected_result = [("row1",), ("row2",)]
        self.cursor_mock.fetchall.return_value = expected_result

        result = DatabaseOperations.select_data(self.cursor_mock, command)

        self.cursor_mock.execute.assert_called_once_with(command)
        self.cursor_mock.fetchall.assert_called_once()
        self.assertEqual(result, expected_result)

    @patch("src.shared.database.operations.establish_mysql_connection", lambda func: func)
    def test_count_rows(self):
        table = "local_test"
        expected_result = (5,)
        self.cursor_mock.fetchone.return_value = expected_result

        result = DatabaseOperations.count_rows(self.cursor_mock, table)

        self.cursor_mock.execute.assert_called_once_with(f"SELECT COUNT(*) FROM {table}")
        self.cursor_mock.fetchone.assert_called_once()
        self.assertEqual(result, expected_result[0])


if __name__ == "__main__":
    unittest.main()
