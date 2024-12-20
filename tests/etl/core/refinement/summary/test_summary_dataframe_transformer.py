import pandas as pd

from src.etl.core.refinement.summary.transformer import SummaryDataFrameTransformer
from tests.etl.core.refinement.base import GoldDataframeTestCase


class TestSummaryDataFrameTransformer(GoldDataframeTestCase):

    def setUp(self):
        self.transformer = SummaryDataFrameTransformer()

        self.df_cleaned_mocked = self.generate_mock_dataframe(cleaned_table="navigator")

        self.df_test = pd.DataFrame(
            {
                "a": [3, 2, 1],
                "b": [4, 5, 6],
                "c": [7, 8, 9],
            }
        )

        self.df1 = self.transformer.melter.apply(
            self.df_cleaned_mocked, detail="book", value_vars=["read_A", "listen_A", "notes_A", "read_B", "listen_B", "notes_B"]
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

    def test_get_value_columns(self):
        value_vars = self.transformer._get_value_columns(self.df_cleaned_mocked)
        expected_value_vars = ["read_A", "listen_A", "notes_A", "read_B", "listen_B", "notes_B"]
        self.assertEqual(value_vars, expected_value_vars)

    def test_set_habit_group_for_atharva(self):
        df_cleaned = pd.DataFrame(
            {
                "element_name": ["atharva_bindu", "atharva_bindu", "atharva_bindu", "atharva_bindu"],
                "habit_action": ["action1Reset", "action2", "action2Reset", "action1"],
                "user_id": [1, 2, 3, 4],
                "date_input": pd.to_datetime(["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"]),
                "value": [1, 1, 1, 1],
            }
        )

        df_refined = self.transformer._set_habit_group(df_cleaned, {"navigator": "book", "diplomat": "relate"})

        self.assertIn("habit_group", df_refined.columns)
        self.assertEqual(df_refined["habit_group"].tolist(), ["reset", "outlook", "reset", "outlook"])

    def test_set_habit_group(self):
        df_cleaned = pd.DataFrame(
            {
                "element_name": ["element", "element", "element", "element"],
                "habit_action": ["action1", "action2", "action3", "action4"],
                "user_id": [1, 2, 3, 4],
                "date_input": pd.to_datetime(["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"]),
                "value": [1, 1, 1, 1],
            }
        )

        df_refined = self.transformer._set_habit_group(df_cleaned, {"element": "group", "element2": "group2"})

        self.assertIn("habit_group", df_refined.columns)
        self.assertEqual(df_refined["habit_group"].unique().tolist(), ["group"])

    def test_calculate_summary_fields(self):
        df_grouped = self.transformer._calculate_summary_fields(self.df2)

        # expected_row_number = len([_ for _ in self.df2["habit_detail"].unique() if _ is not None]) * len(self.df2["habit_action"].unique())

        # self.assertEqual(len(df_grouped), expected_row_number)
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
        column_sequence = ["c", "a", "b"]
        dtypes = {"a": "float64", "b": "Int64", "c": "string"}
        sort_keys = ["a"]
        expected_df = self.df_test[column_sequence].astype(dtypes).sort_values(by=sort_keys)
        result_df = self.transformer._reshape_dataframe(self.df_test, column_sequence=column_sequence, dtypes=dtypes, sort_keys=sort_keys)
        pd.testing.assert_frame_equal(result_df, expected_df)

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

        df_refined = self.transformer.apply(self.df_cleaned_mocked)
        self.assertEqual(df_refined.columns.tolist(), expected_columns)
        self.assertEqual(df_refined["element_category"].dtype, "string")
        self.assertEqual(df_refined["element_name"].dtype, "string")
        self.assertEqual(df_refined["user_id"].dtype, "string")
        self.assertEqual(df_refined["habit_group"].dtype, "string")
        self.assertEqual(df_refined["habit_action"].dtype, "string")
        self.assertEqual(df_refined["habit_detail"].dtype, "string")
        self.assertEqual(df_refined["total"].dtype, pd.Int64Dtype())
        self.assertEqual(df_refined["first_date"].dtype, "<M8[ns]")
        self.assertEqual(df_refined["last_date"].dtype, "<M8[ns]")
        self.assertEqual(df_refined["days_since_last"].dtype, pd.Int64Dtype())
        self.assertEqual(df_refined["longest_streak"].dtype, pd.Int64Dtype())
        self.assertEqual(df_refined["longest_gap"].dtype, pd.Int64Dtype())
