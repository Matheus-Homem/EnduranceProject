import unittest

import pandas as pd

from src.etl.core.extraction import ExtractionEngine


class TestExtractionEngine(unittest.TestCase):

    def test_set_date_column(self):
        extraction_engine = ExtractionEngine()
        extraction_column_to_partition = "entry_date"
        extraction_engine.set_date_column(date_column_to_partition=extraction_column_to_partition)
        self.assertEqual(extraction_engine.column_to_partition, extraction_column_to_partition)

    def test_convert_to_dataframe(self):
        extraction_engine = ExtractionEngine()

        data = [
            {
                "id": 1,
                "entry_date": pd.Timestamp("2021-01-01"),
                "user_id": "0",
                "element_category": "test_category",
                "element_name": "test_name",
                "element_string": "{'nao':'nao'}",
                "schema_encoded": "1",
                "op": "u",
                "created_at": pd.Timestamp("2024-09-20 06:14:57"),
                "updated_at": pd.Timestamp("2024-09-20 06:24:51"),
            }
        ]

        dataframe = extraction_engine._convert_to_dataframe(input_data=data)

        self.assertEqual(
            list(dataframe.columns),
            [
                "id",
                "entry_date",
                "user_id",
                "element_category",
                "element_name",
                "element_string",
                "schema_encoded",
                "op",
                "created_at",
                "updated_at",
            ],
        )
        self.assertIsInstance(dataframe, pd.DataFrame)

    def test_add_partition_columns(self):
        extraction_engine = ExtractionEngine()
        extraction_engine.set_date_column("entry_date")

        test_df = pd.DataFrame(
            [
                {"entry_date": "2024-01-01"},
                {"entry_date": "2024-01-02"},
                {"entry_date": "2024-01-03"},
            ]
        )

        test_df_to_assert = extraction_engine._add_partition_columns(dataframe=test_df)

        self.assertIsInstance(test_df_to_assert, pd.DataFrame)
        self.assertEqual(list(test_df_to_assert.columns), ["entry_date", "year", "month", "day"])
        self.assertEqual(test_df_to_assert.shape[0], 3)

    def test_process(self):
        extraction_engine = ExtractionEngine()
        extraction_engine.set_date_column("entry_date")

        data = [
            {
                "id": 1,
                "entry_date": pd.Timestamp("2021-01-01"),
                "user_id": "0",
                "element_category": "test_category",
                "element_name": "test_name",
                "element_string": "{'nao':'nao'}",
                "schema_encoded": "1",
                "op": "u",
                "created_at": pd.Timestamp("2024-09-20 06:14:57"),
                "updated_at": pd.Timestamp("2024-09-20 06:24:51"),
            },
            {
                "id": 2,
                "entry_date": pd.Timestamp("2021-02-15"),
                "user_id": "1",
                "element_category": "test_category_2",
                "element_name": "test_name_2",
                "element_string": "{'sim':'sim'}",
                "schema_encoded": "2",
                "op": "i",
                "created_at": pd.Timestamp("2024-09-21 07:14:57"),
                "updated_at": pd.Timestamp("2024-09-21 07:24:51"),
            },
            {
                "id": 3,
                "entry_date": pd.Timestamp("2021-03-20"),
                "user_id": "2",
                "element_category": "test_category_3",
                "element_name": "test_name_3",
                "element_string": "{'talvez':'talvez'}",
                "schema_encoded": "3",
                "op": "d",
                "created_at": pd.Timestamp("2024-09-22 08:14:57"),
                "updated_at": pd.Timestamp("2024-09-22 08:24:51"),
            },
        ]

        result_df = extraction_engine.process(data)

        expected_columns = [
            "id",
            "entry_date",
            "user_id",
            "element_category",
            "element_name",
            "element_string",
            "schema_encoded",
            "op",
            "created_at",
            "updated_at",
            "year",
            "month",
            "day",
        ]

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(list(result_df.columns), expected_columns)
        self.assertEqual(result_df.shape[0], 3)


if __name__ == "__main__":
    unittest.main()
