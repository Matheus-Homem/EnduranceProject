import unittest
from unittest.mock import MagicMock, patch

from src.etl.readers.database import DatabaseReader
from src.shared.database.tables import MySqlTable


class TestDatabaseReader(unittest.TestCase):

    def setUp(self):

        self.mock_table = MagicMock(spec=MySqlTable)
        self.mock_table.__tablename__ = "test_table"

        self.mock_executor = MagicMock()
        self.mock_executor.select.return_value = [{"column1": "value1", "column2": "value2"}, {"column1": "value3", "column2": "value4"}]

    @patch("src.etl.readers.database.DatabaseExecutorBuilder", return_value=MagicMock())
    def test_read_dataframe(self, MockDatabaseExecutorBuilder):

        MockDatabaseExecutorBuilder.return_value.__enter__.return_value = self.mock_executor

        reader = DatabaseReader()
        df = reader.read_dataframe(self.mock_table)

        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.shape[1], 2)
        self.assertEqual(df["column1"][0], "value1")
        self.assertEqual(df["column2"][1], "value4")


if __name__ == "__main__":
    unittest.main()
