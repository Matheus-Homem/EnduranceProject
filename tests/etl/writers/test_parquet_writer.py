import unittest
from unittest.mock import patch

from polars import DataFrame

from src.etl.definitions import Path
from src.etl.writers.parquet import ParquetWriter


class TestParquetWriter(unittest.TestCase):

    @patch("src.etl.writers.parquet.DataFrame.write_parquet")
    def test_write_dataframe(self, mock_write_parquet):

        mock_df = DataFrame({"column1": ["value1", "value2"], "column2": ["value3", "value4"]})
        mock_path = Path("test_path")

        writer = ParquetWriter()
        writer.write_dataframe(mock_df, mock_path)

        mock_write_parquet.assert_called_once_with("test_path")


if __name__ == "__main__":
    unittest.main()
