import unittest
from unittest.mock import patch, MagicMock
from src.shared.handlers import MySqlHandler, StatmentType

class TestMySqlHandler(unittest.TestCase):

    @patch('src.shared.handlers.PRD', "EnduranceProject")
    def test_is_prd_environment_true(self):
        connector = MySqlHandler()
        is_prd = connector._is_prd_environment()
        self.assertTrue(is_prd)

    @patch('src.shared.handlers.PRD', "")
    def test_is_prd_environment_false(self):
        connector = MySqlHandler()
        is_prd = connector._is_prd_environment()
        self.assertFalse(is_prd)

    def test_can_establish_remote_connection(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            connection = connector._establish_remote_connection()
            self.assertEqual(connection, connection)

    def test_can_establish_local_connection(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            with patch('src.shared.handlers.sshtunnel.SSHTunnelForwarder'):
                connection = connector._establish_local_connection()
                self.assertEqual(connection, connection)

    def test_can_close_connection(self):
        connection = MagicMock()
        cursor = MagicMock()
        connector = MySqlHandler()
        connector._close_connection(connection, cursor)
        connection.close.assert_called_once()
        cursor.close.assert_called_once()

    def test_can_validate_statement(self):
        connector = MySqlHandler()
        valid_statements = ["SELECT * FROM table", "INSERT INTO table", "UPDATE table", "DELETE FROM table"]
        for statement in valid_statements:
            connector._validate_statement(statement)

        invalid_statements = ["DROP table", "CREATE table", "ALTER table", "TRUNCATE table", "SHOW table", "DESCRIBE table"]
        for statement in invalid_statements:
            self.assertRaises(ValueError, connector._validate_statement, statement)

    def test_can_set_statement_type(self):
        select_statements = ["SELECT * FROM table", "select * from table", "Select count(*) from table"]
        for statement in select_statements:
            self.assertEqual(MySqlHandler()._set_statement_type(statement), StatmentType.RESULT)

        commit_statements = ["INSERT INTO table", "UPDATE table", "DELETE FROM table"]
        for statement in commit_statements:
            self.assertEqual(MySqlHandler()._set_statement_type(statement), StatmentType.COMMIT)

    def test_execute(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            with patch('src.shared.handlers.sshtunnel.SSHTunnelForwarder'):
                connector.execute("SELECT * FROM table")
                cursor.execute.assert_called_once()

        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            with patch('src.shared.handlers.sshtunnel.SSHTunnelForwarder'):
                connector.execute("INSERT INTO table")
                cursor.execute.assert_called_once()

        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            with patch('src.shared.handlers.sshtunnel.SSHTunnelForwarder'):
                connector.execute("UPDATE table")
                cursor.execute.assert_called_once()

        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            with patch('src.shared.handlers.sshtunnel.SSHTunnelForwarder'):
                connector.execute("DELETE FROM table")
                cursor.execute.assert_called_once()

        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connector = MySqlHandler()
        with patch('src.shared.handlers.connect', return_value=connection):
            with patch('src.shared.handlers.sshtunnel.SSHTunnelForwarder'):
                self.assertRaises(ValueError, connector.execute, "DROP table")

if __name__ == '__main__':
    unittest.main()