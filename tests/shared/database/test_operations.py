import unittest
from unittest.mock import MagicMock, patch


class TestDatabaseOperations(unittest.TestCase):

    @patch("src.shared.decorators.establish_mysql_connection", lambda func: func)
    def test_execute_command(self):
        cursor_mock = MagicMock()
        command = 'INSERT INTO local_test (data) VALUES (\'{"key1": "value1", "key2": "value2"}\');'
        from src.shared.database.operations import DatabaseOperations

        DatabaseOperations.execute_command(cursor_mock, command)

        cursor_mock.execute.assert_called_once_with(command)
        print("test_execute_command passed")

    @patch("src.shared.decorators.establish_mysql_connection", lambda func: func)
    def test_select_data(self):
        cursor_mock = MagicMock()
        command = "SELECT * FROM local_test;"
        expected_result = [("row1",), ("row2",)]
        cursor_mock.fetchall.return_value = expected_result
        from src.shared.database.operations import DatabaseOperations

        result = DatabaseOperations.select_data(cursor_mock, command)

        cursor_mock.execute.assert_called_once_with(command)
        cursor_mock.fetchall.assert_called_once()
        self.assertEqual(result, expected_result)
        print("test_select_data passed")

    @patch("src.shared.decorators.establish_mysql_connection", lambda func: func)
    def test_count_rows(self):
        cursor_mock = MagicMock()
        table = "local_test"
        expected_result = (5,)
        cursor_mock.fetchone.return_value = expected_result
        from src.shared.database.operations import DatabaseOperations

        result = DatabaseOperations.count_rows(cursor_mock, table)

        cursor_mock.execute.assert_called_once_with(f"SELECT COUNT(*) FROM {table}")
        cursor_mock.fetchone.assert_called_once()
        self.assertEqual(result, expected_result[0])
        print("test_count_rows passed")


if __name__ == "__main__":
    unittest.main()
