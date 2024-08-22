import unittest
from pathlib import Path
from unittest.mock import patch

import polars as pl

from src.etl.readers.delta import DeltaReader


class TestDeltaReader(unittest.TestCase):

    @patch("src.etl.readers.delta.DeltaTable")
    def test_read_dataframe(self, MockDeltaTable):
        mock_path = Path("test_path")
        mock_df = pl.DataFrame({"column1": ["value1", "value3"], "column2": ["value2", "value4"]})

        MockDeltaTable.return_value.to_pandas.return_value = mock_df

        reader = DeltaReader()
        df = reader.read_dataframe(mock_path)

        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.shape[1], 2)
        self.assertEqual(df["column1"][0], "value1")
        self.assertEqual(df["column2"][1], "value4")


if __name__ == "__main__":
    unittest.main()
