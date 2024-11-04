from unittest import TestCase
from unittest.mock import patch

from src.etl.core.definitions import Format, Layer
from src.etl.core.io import IOManager
from src.etl.core.refinement.summary.melter import SummaryDataFrameMelter


class TestSummaryDataFrameTransformer(TestCase):

    def setUp(self):
        self.melter = SummaryDataFrameMelter()
        delta_handler = IOManager(layer=Layer.SILVER, format=Format.DELTA).get_handler()

        self.df_navigator = delta_handler.read("navigator")
        self.df_diplomat = delta_handler.read("diplomat")
        self.df_alchemist = delta_handler.read("alchemist")

    def test_get_detail_columns(self):
        detail_cols = self.melter._get_detail_columns(self.df_navigator, detail_id="book")
        self.assertEqual(detail_cols, ["book_A", "book_B"])

    def test_filter_value_columns(self):
        value_cols = self.melter._filter_value_columns(
            dataframe=self.df_navigator,
            value_columns=["read_A", "listen_A", "notes_A", "read_B", "listen_B", "notes_B"],
            variant="_A",
        )
        self.assertEqual(value_cols, ["read_A", "listen_A", "notes_A"])

    def test_melt_without_detail_col(self):
        value_vars = ["animals", "family", "friends", "society", "contacts", "coworkers"]

        df_melted = self.melter._melt_without_detail_col(
            dataframe=self.df_diplomat,
            value_vars=value_vars,
        )

        self.assertEqual(len(df_melted), len(self.df_diplomat) * len(value_vars))
        self.assertIn("element_category", df_melted.columns)
        self.assertIn("element_name", df_melted.columns)
        self.assertIn("user_id", df_melted.columns)
        self.assertIn("date_input", df_melted.columns)
        self.assertNotIn("habit_detail", df_melted.columns)
        self.assertIn("habit_action", df_melted.columns)
        self.assertIn("value", df_melted.columns)

    def test_melt_with_detail_col(self):
        value_vars = ["read_A", "listen_A", "notes_A", "read_B", "listen_B", "notes_B"]
        detail_col_id = "book"

        number_of_value_columns = len([col for col in self.df_navigator.columns if col in value_vars and col.endswith("_A")])
        number_of_detail_columns = len([col for col in self.df_navigator.columns if col.startswith(detail_col_id)])

        df_melted = self.melter._melt_with_detail_col(
            dataframe=self.df_navigator,
            value_vars=value_vars,
            detail=detail_col_id,
        )

        self.assertEqual(len(df_melted), len(self.df_navigator) * number_of_value_columns * number_of_detail_columns)
        self.assertIn("element_category", df_melted.columns)
        self.assertIn("element_name", df_melted.columns)
        self.assertIn("user_id", df_melted.columns)
        self.assertIn("date_input", df_melted.columns)
        self.assertIn("habit_detail", df_melted.columns)
        self.assertIn("habit_action", df_melted.columns)
        self.assertIn("value", df_melted.columns)

    def test_apply(self):

        with patch.object(self.melter, "_melt_with_detail_col") as mock_melt_with_detail_col:
            _ = self.melter.apply(self.df_navigator, detail="book")
            mock_melt_with_detail_col.assert_called_once_with(dataframe=self.df_navigator, detail="book")

        with patch.object(self.melter, "_melt_without_detail_col") as mock_melt_without_detail_col:
            _ = self.melter.apply(self.df_alchemist)
            mock_melt_without_detail_col.assert_called_once_with(self.df_alchemist)
            expected_result = mock_melt_without_detail_col.return_value.copy()
            expected_result["habit_detail"] = None

        with patch.object(self.melter, "_melt_without_detail_col") as mock_melt_without_detail_col:
            _ = self.melter.apply(self.df_diplomat)
            mock_melt_without_detail_col.assert_called_once_with(self.df_diplomat)
            expected_result = mock_melt_without_detail_col.return_value.copy()
            expected_result["habit_detail"] = None
