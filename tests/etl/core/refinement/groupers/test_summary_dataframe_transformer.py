from unittest import TestCase

import pandas as pd

from src.etl.core.definitions import Format, Layer
from src.etl.core.io import IOManager
from src.etl.core.refinement.summary.transformer import SummaryDataFrameTransformer


class TestSummaryDataFrameTransformer(TestCase):

    def setUp(self):
        self.transformer = SummaryDataFrameTransformer()
        delta_handler = IOManager(layer=Layer.SILVER, format=Format.DELTA).get_handler()

        self.df_navigator = delta_handler.read("navigator")
        self.df_alchemist = delta_handler.read("alchemist")
        self.df_diplomat = delta_handler.read("diplomat")

        self.df1 = self.transformer.melter.apply(
            self.df_navigator, detail="book", value_vars=["read_A", "listen_A", "notes_A", "read_B", "listen_B", "notes_B"]
        )

        self.df2 = self.df1.copy()
        self.df2["habit_group"] = "book"

        self.df3 = (
            self.df2.groupby(["user_id", "element_category", "element_name", "habit_detail", "habit_action", "habit_group"])
            .agg(
                total=("date_input", lambda x: 42),
                first_date=("date_input", lambda x: pd.to_datetime("2022-02-10")),
                last_date=("date_input", lambda x: pd.to_datetime("2022-02-10")),
                longest_streak=("date_input", lambda x: 1),
                longest_gap=("date_input", lambda x: 2),
            )
            .reset_index()
        )

        self.df4 = self.df3.copy()
        self.df4["days_since_last"] = (self.df4["last_date"] - self.df4["first_date"]).dt.days

    def test_get_habit_detail_col(self):
        habit_detail = self.transformer._get_habit_detail_col(self.df_navigator)
        self.assertEqual(habit_detail, "book")

    def test_get_value_columns(self):
        value_vars = self.transformer._get_value_columns(self.df_navigator)
        expected_value_vars = ["read_A", "listen_A", "notes_A", "read_B", "listen_B", "notes_B"]
        self.assertEqual(value_vars, expected_value_vars)

    def test_set_habit_group(self):
        df = self.transformer._set_habit_group(self.df_navigator)
        habit_group = df["habit_group"].unique()[0]
        self.assertEqual(habit_group, "book")

        df = self.transformer._set_habit_group(self.df_diplomat)
        habit_group = df["habit_group"].unique()[0]
        self.assertEqual(habit_group, "relate")

    def test_calculate_summary_fields(self):
        df_grouped = self.transformer._calculate_summary_fields(self.df2)

        expected_row_number = len([_ for _ in self.df2["habit_detail"].unique() if _ is not None]) * len(self.df2["habit_action"].unique())

        self.assertEqual(len(df_grouped), expected_row_number)
        self.assertIn("element_category", df_grouped.columns)
        self.assertIn("element_name", df_grouped.columns)
        self.assertIn("user_id", df_grouped.columns)
        self.assertIn("habit_detail", df_grouped.columns)
        self.assertIn("habit_action", df_grouped.columns)
        self.assertIn("habit_group", df_grouped.columns)
        self.assertIn("total", df_grouped.columns)
        self.assertIn("first_date", df_grouped.columns)
        self.assertIn("last_date", df_grouped.columns)
        self.assertIn("longest_streak", df_grouped.columns)
        self.assertIn("longest_gap", df_grouped.columns)

    def test_add_fields(self):
        df = self.transformer._add_fields(self.df3)
        self.assertIn("days_since_last", df.columns)

    def test_reshape_dataframe(self):
        df = self.transformer._reshape_dataframe(self.df4)

        expected_columns_sequence = [
            "element_category",
            "element_name",
            "user_id",
            "habit_group",
            "habit_action",
            "habit_detail",
            "total",
            "first_date",
            "last_date",
            "days_since_last",
            "longest_streak",
            "longest_gap",
        ]

        self.assertEqual(list(df.columns), expected_columns_sequence)

    def test_apply(self):
        expected_columns = [
            "element_category",
            "element_name",
            "user_id",
            "habit_group",
            "habit_action",
            "habit_detail",
            "total",
            "first_date",
            "last_date",
            "days_since_last",
            "longest_streak",
            "longest_gap",
        ]

        for df in [self.df_navigator, self.df_diplomat, self.df_alchemist]: #TODO: fix types
            df_result = self.transformer.apply(df)
            self.assertEqual(df_result.columns.tolist(), expected_columns)
            self.assertEqual(df_result["element_category"].dtype, "object")
            self.assertEqual(df_result["element_name"].dtype, "object")
            self.assertEqual(df_result["user_id"].dtype, "object")
            self.assertEqual(df_result["habit_group"].dtype, "object")
            self.assertEqual(df_result["habit_action"].dtype, "object")
            self.assertEqual(df_result["habit_detail"].dtype, "object")
            self.assertEqual(df_result["total"].dtype, "float64") 
            self.assertEqual(df_result["first_date"].dtype, "<M8[ns]")
            self.assertEqual(df_result["last_date"].dtype, "<M8[ns]")
            self.assertEqual(df_result["days_since_last"].dtype, "float64")
            self.assertEqual(df_result["longest_streak"].dtype, "int64")
            self.assertEqual(df_result["longest_gap"].dtype, "float64")
