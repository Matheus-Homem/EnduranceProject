import unittest
from unittest.mock import patch

import pandas as pd

from src.etl.core.cleaning.schema.transformer import SchemaTransformer


class TestSchemaTransformer(unittest.TestCase):

    # @patch("src.etl.core.cleaning.schema.transformer.DictUtils.deserialize_dict")
    # @patch("src.etl.core.cleaning.schema.transformer.CastingStrategyFactory.get_strategy")
    # @patch("pandas.read_parquet")
    # @patch("pandas.merge")
    # def test_apply(self, mock_merge, mock_read_parquet, mock_get_strategy, mock_deserialize_dict):
    #     # Preparation
    #     transformer = SchemaTransformer()

    #     schema_data = {
    #         "schema_encoded": ["schema1", "schema2"],
    #         "element_category": ["cat1", "cat2"],
    #         "element_name": ["elem1", "elem2"],
    #         "schema_dtypes": ['{"col1": "INTEGER", "col2": "STRING"}', '{"col3": "DATE"}'],
    #         "schema_fields": ["field1", "field2"],
    #     }
    #     df_schema = pd.DataFrame(schema_data)
    #     df_input_data = {
    #         "schema_encoded": ["schema1", "schema2"],
    #         "element_category": ["cat1", "cat2"],
    #         "element_name": ["elem1", "elem2"],
    #         "col1": ["1", "2"],
    #         "col2": ["a", "b"],
    #         "col3": ["2021-01-01", "2022-02-02"],
    #     }
    #     df_input = pd.DataFrame(df_input_data)
    #     df_merged = pd.merge(df_input, df_schema, on=["schema_encoded", "element_category", "element_name"], how="inner")

    #     mock_read_parquet.return_value = df_schema
    #     mock_merge.return_value = df_merged

    #     mock_deserialize_dict.side_effect = [{"col1": "INTEGER", "col2": "STRING"}, {"col3": "DATE"}]

    #     mock_integer_strategy = MagicMock(spec=IntegerCastingStrategy)
    #     mock_string_strategy = MagicMock(spec=StringCastingStrategy)
    #     mock_date_strategy = MagicMock(spec=DateCastingStrategy)
    #     mock_get_strategy.side_effect = [mock_integer_strategy, mock_string_strategy, mock_date_strategy]

    #     mock_integer_strategy.cast.side_effect = lambda x: x.astype(int)
    #     mock_string_strategy.cast.side_effect = lambda x: x.astype(str)
    #     mock_date_strategy.cast.side_effect = lambda x: pd.to_datetime(x)

    #     transformed_df1 = pd.Series([1, 2], dtype=int)
    #     transformed_df2 = pd.Series(["a", "b"], dtype=str)
    #     transformed_df3 = pd.to_datetime(pd.Series(["2021-01-01", "2022-02-02"]))

    #     mock_integer_strategy.cast.side_effect = lambda x: transformed_df1
    #     mock_string_strategy.cast.side_effect = lambda x: transformed_df2
    #     mock_date_strategy.cast.side_effect = lambda x: transformed_df3

    #     # Execution
    #     result = transformer.apply(dataframe=df_input)

    #     # Asserts
    #     mock_read_parquet.assert_called_once_with("data/bronze/schemas.parquet")
    #     mock_merge.assert_called_with(df_input, df_schema, on=["schema_encoded", "element_category", "element_name"], how="inner")
    #     mock_deserialize_dict.assert_has_calls([call(df_schema["schema_dtypes"].iloc[0]), call(df_schema["schema_dtypes"].iloc[1])])
    #     mock_get_strategy.assert_has_calls([call("INTEGER"), call("STRING"), call("DATE")])

    #     mock_integer_strategy.cast.assert_called_once_with(df_merged["col1"].replace("", None))
    #     mock_string_strategy.cast.assert_called_once_with(df_merged["col2"].replace("", None))
    #     mock_date_strategy.cast.assert_called_once_with(df_merged["col3"].replace("", None))

    #     expected_df = df_merged.copy()
    #     expected_df["col1"] = transformed_df1
    #     expected_df["col2"] = transformed_df2
    #     expected_df["col3"] = transformed_df3

    #     pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

    @patch("pandas.read_parquet")
    def test_read_schema_dataframe(self, mock_read_parquet):
        # Preparation
        transformer = SchemaTransformer()
        schema_path = "path/to/schema.parquet"
        df_mock = pd.DataFrame(
            {
                "schema_encoded": ["schema1"],
                "element_category": ["cat1"],
                "element_name": ["elem1"],
                "schema_dtypes": ['{"col1": "INTEGER"}'],
                "schema_fields": ["field1"],
            }
        )
        mock_read_parquet.return_value = df_mock

        # Execution
        result = transformer._read_schema_dataframe(schema_path)

        # Asserts
        mock_read_parquet.assert_called_once_with(schema_path)
        expected_df = df_mock[["schema_encoded", "element_category", "element_name", "schema_dtypes", "schema_fields"]]
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

    @patch("src.etl.core.cleaning.schema.transformer.DictUtils.deserialize_dict")
    def test_get_dtype_dict_success(self, mock_deserialize_dict):
        # Preparation
        transformer = SchemaTransformer()
        df_schema = pd.DataFrame(
            {
                "schema_encoded": ["schema1"],
                "element_category": ["cat1"],
                "element_name": ["elem1"],
                "schema_dtypes": ['{"col1": "INTEGER", "col2": "STRING"}'],
                "schema_fields": ["field1"],
            }
        )
        schema_encoded = "schema1"
        mock_deserialize_dict.return_value = {"col1": "INTEGER", "col2": "STRING"}

        # Execution
        result = transformer._get_dtype_dict(df_schema, schema_encoded)

        # Asserts
        mock_deserialize_dict.assert_called_once_with('{"col1": "INTEGER", "col2": "STRING"}')
        expected_dict = {"col1": "INTEGER", "col2": "STRING"}
        self.assertEqual(result, expected_dict)

    @patch("src.etl.core.cleaning.schema.transformer.DictUtils.deserialize_dict")
    def test_get_dtype_dict_failure(self, mock_deserialize_dict):
        # Preparation
        transformer = SchemaTransformer()
        df_schema = pd.DataFrame(
            {
                "schema_encoded": ["schema1"],
                "element_category": ["cat1"],
                "element_name": ["elem1"],
                "schema_dtypes": ["invalid_json"],
                "schema_fields": ["field1"],
            }
        )
        schema_encoded = "schema1"
        mock_deserialize_dict.side_effect = ValueError("Invalid JSON")

        # Execution & Asserção
        with self.assertRaises(Exception) as context:
            transformer._get_dtype_dict(df_schema, schema_encoded)
        self.assertIn("Error while getting schema dtype dictionary", str(context.exception))
        mock_deserialize_dict.assert_called_once_with("invalid_json")


if __name__ == "__main__":
    unittest.main()
