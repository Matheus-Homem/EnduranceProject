import unittest
from unittest.mock import MagicMock, patch

from src.etl.core.definitions import Layer, PandasDF
from src.etl.core.io.parquet import ParquetHandler


class TestParquetHandler(unittest.TestCase):

    @patch("src.etl.core.io.parquet.read_parquet")
    def test_read(self, mock_read_parquet):
        # Preparation
        layer = Layer.BRONZE
        handler = ParquetHandler(layer=layer)
        table_name = "test_table"
        expected_path = "/path/to/test_table.parquet"
        expected_df = MagicMock(spec=PandasDF)

        handler.generate_path = MagicMock(return_value=expected_path)
        mock_read_parquet.return_value = expected_df

        # Execution
        result = handler.read(table_name)

        # Asserts
        handler.generate_path.assert_called_once_with(table_name=table_name)
        mock_read_parquet.assert_called_once_with(expected_path)
        self.assertEqual(result, expected_df)

    @patch("src.etl.core.io.parquet.PandasDF.to_parquet")
    def test_write(self, mock_to_parquet):
        # Preparation
        layer = Layer.BRONZE
        handler = ParquetHandler(layer=layer)
        table_name = "test_table"
        dataframe = MagicMock(spec=PandasDF)
        expected_path = "/path/to/test_table.parquet"
        partition_cols = ["year", "month", "day"]

        handler.generate_path = MagicMock(return_value=expected_path)

        # Execution
        handler.write(dataframe=dataframe, table_name=table_name, partition_cols=partition_cols)

        # Asserts
        handler.generate_path.assert_called_once_with(table_name=table_name)
        dataframe.to_parquet.assert_called_once_with(expected_path, index=False, partition_cols=partition_cols)

    @patch("src.etl.core.io.parquet.PandasDF.to_parquet")
    def test_write_without_partition_cols(self, mock_to_parquet):
        # Preparation
        layer = Layer.BRONZE
        handler = ParquetHandler(layer=layer)
        table_name = "test_table"
        dataframe = MagicMock(spec=PandasDF)
        expected_path = "/path/to/test_table.parquet"

        handler.generate_path = MagicMock(return_value=expected_path)

        # Execution
        handler.write(dataframe=dataframe, table_name=table_name)

        # Asserts
        handler.generate_path.assert_called_once_with(table_name=table_name)
        dataframe.to_parquet.assert_called_once_with(expected_path, index=False, partition_cols=None)


if __name__ == "__main__":
    unittest.main()
