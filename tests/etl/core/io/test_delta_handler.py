import unittest
from unittest.mock import MagicMock, call, patch

from src.etl.core.definitions import Layer, PandasDF
from src.etl.core.io.delta import DeltaHandler


class TestDeltaHandler(unittest.TestCase):

    @patch("src.etl.core.io.delta.DeltaTable")
    def test_read(self, mock_delta_table):
        # Preparation
        layer = Layer.SILVER
        handler = DeltaHandler(layer=layer)
        table_name = "test_table"
        expected_path = "/path/to/test_table.delta"
        expected_df = MagicMock(spec=PandasDF)

        handler.generate_path = MagicMock(return_value=expected_path)
        mock_instance = MagicMock()
        mock_instance.to_pandas.return_value = expected_df
        mock_delta_table.return_value = mock_instance

        # Execution
        result = handler.read(table_name)

        # Asserts
        handler.generate_path.assert_called_once_with(table_name=table_name)
        mock_delta_table.assert_called_once_with(expected_path)
        mock_instance.to_pandas.assert_called_once()
        self.assertEqual(result, expected_df)

    @patch("src.etl.core.io.delta.write_deltalake")
    def test_write(self, mock_write_deltalake):
        # Preparation
        layer = Layer.SILVER
        handler = DeltaHandler(layer=layer)
        table_name = "test_table"
        dataframe = MagicMock(spec=PandasDF)
        expected_path = "/path/to/test_table.delta"

        handler.generate_path = MagicMock(return_value=expected_path)

        # Execution
        handler.write(dataframe=dataframe, table_name=table_name)

        # Asserts
        handler.generate_path.assert_called_once_with(table_name=table_name)
        mock_write_deltalake.assert_called_once_with(expected_path, dataframe, mode="overwrite", schema_mode="overwrite")

    @patch("src.etl.core.io.delta.DeltaTable")
    def test_is_delta_table_true(self, mock_delta_table):
        # Preparation
        layer = Layer.GOLD
        handler = DeltaHandler(layer=layer)
        path = "/path/to/valid_table.delta"

        # Configurar o DeltaTable para não levantar exceção
        mock_delta_table.return_value = MagicMock()

        # Execution
        result = handler._is_delta_table(path)

        # Asserts
        mock_delta_table.assert_called_once_with(path)
        self.assertTrue(result)

    @patch("src.etl.core.io.delta.DeltaTable")
    def test_is_delta_table_false(self, mock_delta_table):
        # Preparation
        layer = Layer.GOLD
        handler = DeltaHandler(layer=layer)
        path = "/path/to/invalid_table.delta"

        # Configurar o DeltaTable para levantar exceção
        mock_delta_table.side_effect = Exception("Invalid Delta Table")

        # Execution
        result = handler._is_delta_table(path)

        # Asserts
        mock_delta_table.assert_called_once_with(path)
        self.assertFalse(result)

    @patch("src.etl.core.io.delta.explore_directory")
    @patch("src.etl.core.io.delta.extract_basename")
    @patch("src.etl.core.io.delta.DeltaHandler._is_delta_table")
    def test_list_delta_tables(self, mock_is_delta_table, mock_extract_basename, mock_explore_directory):
        # Preparation
        layer = Layer.SILVER
        handler = DeltaHandler(layer=layer)
        base_path = "/path/to/delta_tables/"
        mock_explore_directory.return_value = [
            ("/path/to/delta_tables/table1", ["_delta_log"], []),
            ("/path/to/delta_tables/table2", ["not_delta_log"], []),
            ("/path/to/delta_tables/table3", ["_delta_log"], []),
        ]
        mock_is_delta_table.side_effect = [True, False, True]
        mock_extract_basename.side_effect = ["table1", "table3"]

        handler.generate_path = MagicMock(return_value=base_path)

        # Execution
        result = handler.list_delta_tables()

        # Asserts
        handler.generate_path.assert_called_once_with(table_name="")
        mock_explore_directory.assert_called_once_with(base_path)
        expected_is_delta_calls = [call("/path/to/delta_tables/table1"), call("/path/to/delta_tables/table3")]
        mock_is_delta_table.assert_has_calls(expected_is_delta_calls, any_order=False)
        expected_extract_basename_calls = [
            call("/path/to/delta_tables/table1"),
        ]
        mock_extract_basename.assert_has_calls(expected_extract_basename_calls, any_order=False)
        self.assertEqual(result, ["table1"])


if __name__ == "__main__":
    unittest.main()
