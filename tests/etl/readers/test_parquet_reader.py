import unittest
from pathlib import Path
from unittest.mock import patch

import polars as pl

from src.etl.readers.parquet import ParquetReader


class TestParquetReader(unittest.TestCase):

    @patch("src.etl.readers.parquet.read_parquet")
    def test_read_dataframe(self, mock_polars_read_parquet):
        mock_path = Path("test_path")
        mock_df = pl.DataFrame({"column1": ["value1", "value3"], "column2": ["value2", "value4"]})

        mock_polars_read_parquet.return_value = mock_df

        reader = ParquetReader()
        df = reader.read_dataframe(mock_path)

        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.shape[1], 2)
        self.assertEqual(df["column1"][0], "value1")
        self.assertEqual(df["column2"][1], "value4")


if __name__ == "__main__":
    unittest.main()
