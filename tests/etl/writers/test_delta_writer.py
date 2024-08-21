import unittest
from unittest.mock import patch

from polars import DataFrame

from src.etl.definitions import Path
from src.etl.writers.delta import DeltaWriter


class TestDeltaWriter(unittest.TestCase):

    @patch("src.etl.writers.delta.write_deltalake")
    def test_write_dataframe(self, mock_write_deltalake):

        mock_df = DataFrame({"column1": ["value1", "value2"], "column2": ["value3", "value4"]})
        mock_path = Path("test_path")

        writer = DeltaWriter()
        writer.write_dataframe(mock_df, mock_path)

        called_args, called_kwargs = mock_write_deltalake.call_args
        mock_write_deltalake.assert_called_once()

        self.assertEqual(called_args[0], Path("test_path"))
        self.assertEqual(called_args[1]["column1"][0], mock_df.to_pandas()["column1"][0])
        self.assertEqual(called_args[1]["column2"][1], mock_df.to_pandas()["column2"][1])
        self.assertEqual(called_kwargs["mode"], "overwrite")


if __name__ == "__main__":
    unittest.main()
