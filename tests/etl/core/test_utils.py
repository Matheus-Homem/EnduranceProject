import unittest

import pandas as pd

from src.etl.core.definitions import TableName
from src.etl.core.utils import PipelineUtils


class TestPipelineUtils(unittest.TestCase):
    def test_split_dataframe_multiple_subsets(self):
        # Preparation
        data = {"category": ["A", "B", "A", "C", "B", "C"], "value": [10, 20, 30, 40, 50, 60]}
        df = pd.DataFrame(data)
        expected_subsets = [df[df["category"] == "A"], df[df["category"] == "B"], df[df["category"] == "C"]]

        # Execution
        result = PipelineUtils.split_dataframe(dataframe=df, column_to_split="category")

        # Asserts
        self.assertEqual(len(result), 3)
        pd.testing.assert_frame_equal(result[0].reset_index(drop=True), expected_subsets[0].reset_index(drop=True))
        pd.testing.assert_frame_equal(result[1].reset_index(drop=True), expected_subsets[1].reset_index(drop=True))
        pd.testing.assert_frame_equal(result[2].reset_index(drop=True), expected_subsets[2].reset_index(drop=True))

    def test_split_dataframe_single_subset(self):
        # Preparation
        data = {"category": ["A", "A", "A"], "value": [10, 20, 30]}
        df = pd.DataFrame(data)
        expected_subsets = [df]

        # Execution
        result = PipelineUtils.split_dataframe(dataframe=df, column_to_split="category")

        # Asserts
        self.assertEqual(len(result), 1)
        pd.testing.assert_frame_equal(result[0].reset_index(drop=True), expected_subsets[0].reset_index(drop=True))

    def test_split_dataframe_unique_each_subset(self):
        # Preparation
        data = {"category": ["A", "B", "C"], "value": [10, 20, 30]}
        df = pd.DataFrame(data)
        expected_subsets = [df[df["category"] == "A"], df[df["category"] == "B"], df[df["category"] == "C"]]

        # Execution
        result = PipelineUtils.split_dataframe(dataframe=df, column_to_split="category")

        # Asserts
        self.assertEqual(len(result), 3)
        pd.testing.assert_frame_equal(result[0].reset_index(drop=True), expected_subsets[0].reset_index(drop=True))
        pd.testing.assert_frame_equal(result[1].reset_index(drop=True), expected_subsets[1].reset_index(drop=True))
        pd.testing.assert_frame_equal(result[2].reset_index(drop=True), expected_subsets[2].reset_index(drop=True))

    def test_split_dataframe_empty_dataframe(self):
        # Preparation
        df = pd.DataFrame(columns=["category", "value"])

        # Execution
        result = PipelineUtils.split_dataframe(dataframe=df, column_to_split="category")

        # Asserts
        self.assertEqual(len(result), 0)

    def test_split_dataframe_nonexistent_column(self):
        # Preparation
        data = {"category": ["A", "B", "A"], "value": [10, 20, 30]}
        df = pd.DataFrame(data)

        # Execution & Asserção
        with self.assertRaises(KeyError):
            PipelineUtils.split_dataframe(dataframe=df, column_to_split="nonexistent_column")

    def test_get_subset_table_name_regular_case(self):
        # Preparation
        data = {"subset_col": ["table1", "table2", "table1"], "value": [10, 20, 30]}
        df = pd.DataFrame(data)
        expected_table_name = TableName("table1")

        # Execution
        result = PipelineUtils.get_subset_table_name(dataframe=df, subset_col_id="subset_col")

        # Asserts
        self.assertEqual(result, expected_table_name)

    def test_get_subset_table_name_single_unique_value(self):
        # Preparation
        data = {"subset_col": ["table1", "table1", "table1"], "value": [10, 20, 30]}
        df = pd.DataFrame(data)
        expected_table_name = TableName("table1")

        # Execution
        result = PipelineUtils.get_subset_table_name(dataframe=df, subset_col_id="subset_col")

        # Asserts
        self.assertEqual(result, expected_table_name)

    def test_get_subset_table_name_empty_dataframe(self):
        # Preparation
        df = pd.DataFrame(columns=["subset_col", "value"])

        # Execution & Asserção
        with self.assertRaises(IndexError):
            PipelineUtils.get_subset_table_name(dataframe=df, subset_col_id="subset_col")

    def test_get_subset_table_name_nonexistent_column(self):
        # Preparation
        data = {"subset_col": ["table1", "table2"], "value": [10, 20]}
        df = pd.DataFrame(data)

        # Execution & Asserção
        with self.assertRaises(KeyError):
            PipelineUtils.get_subset_table_name(dataframe=df, subset_col_id="nonexistent_column")


if __name__ == "__main__":
    unittest.main()
