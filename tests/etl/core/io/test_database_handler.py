import unittest
from unittest.mock import MagicMock, patch

from src.database.tables import MySqlTable
from src.etl.core.definitions import DatabaseDF, Layer
from src.etl.core.io.database import DatabaseHandler
from src.shared.credentials import PRD


class TestDatabaseHandler(unittest.TestCase):

    @patch("src.etl.core.io.database.DatabaseExecutorBuilder")
    def test_read(self, mock_executor_builder):
        # Preparation
        layer = Layer.DATABASE
        handler = DatabaseHandler(layer=layer)
        table_name = MagicMock(spec=MySqlTable)
        expected_mysql_table = "path_to_test_table"
        handler.generate_path = MagicMock(return_value=expected_mysql_table)

        mock_executor = MagicMock()
        mock_executor.select.return_value = MagicMock(spec=DatabaseDF)
        mock_executor_builder.return_value.__enter__.return_value = mock_executor

        # Execution
        result = handler.read(table_name)

        # Asserts
        handler.generate_path.assert_called_once_with(table_name)
        mock_executor_builder.assert_called_once_with(use_production_db=PRD)
        mock_executor.select.assert_called_once_with(expected_mysql_table)

    def test_write_not_implemented(self):
        # Preparation
        layer = Layer.DATABASE
        handler = DatabaseHandler(layer=layer)
        table = MagicMock()

        # Execution and Asserts
        with self.assertRaises(NotImplementedError) as context:
            handler.write(table)
        self.assertEqual(str(context.exception), "DatabaseReader does not support write operations")


if __name__ == "__main__":
    unittest.main()
