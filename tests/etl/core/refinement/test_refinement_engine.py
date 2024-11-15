import unittest
from unittest.mock import MagicMock, patch

from src.etl.core.definitions import PandasDF, RefinementType
from src.etl.core.refinement.engine import RefinementEngine
from src.etl.core.refinement.monthly.transformer import MonthlyDataFrameTransformer
from src.etl.core.refinement.summary.transformer import SummaryDataFrameTransformer
from src.etl.core.refinement.weekly.transformer import WeeklyDataFrameTransformer


class TestRefinementEngine(unittest.TestCase):

    def setUp(self):
        self.summary_transformer = MagicMock(spec=SummaryDataFrameTransformer)
        self.monthly_transformer = MagicMock(spec=MonthlyDataFrameTransformer)
        self.weekly_transformer = MagicMock(spec=WeeklyDataFrameTransformer)
        self.engine = RefinementEngine(
            summary_transformer=self.summary_transformer, monthly_transformer=self.monthly_transformer, weekly_transformer=self.weekly_transformer
        )
        self.engine.logger = MagicMock()

    @patch("pandas.concat")
    def test_union_dataframes(self, mock_concat):
        # Preparation
        df1 = MagicMock(spec=PandasDF)
        df2 = MagicMock(spec=PandasDF)
        mock_concat.return_value.reset_index.return_value = MagicMock(spec=PandasDF)

        # Execution
        result = self.engine.union_dataframes([df1, df2])

        # Asserts
        mock_concat.assert_called_once_with([df1, df2], ignore_index=True)
        mock_concat.return_value.reset_index.assert_called_once_with(drop=True)
        self.assertIsNotNone(result)

    def test_set_refinement_type_summary(self):
        # Execution
        self.engine.set_refinement_type(RefinementType.SUMMARY)

        # Asserts
        self.engine.logger.info.assert_called_once_with("Setting refinement type to SUMMARY")
        self.assertEqual(self.engine.refinement_type, RefinementType.SUMMARY)

    def test_set_refinement_type_monthly(self):
        # Execution
        self.engine.set_refinement_type(RefinementType.MONTHLY)

        # Asserts
        self.engine.logger.info.assert_called_once_with("Setting refinement type to MONTHLY")
        self.assertEqual(self.engine.refinement_type, RefinementType.MONTHLY)

    def test_set_refinement_type_weekly(self):
        # Execution
        self.engine.set_refinement_type(RefinementType.WEEKLY)

        # Asserts
        self.engine.logger.info.assert_called_once_with("Setting refinement type to WEEKLY")
        self.assertEqual(self.engine.refinement_type, RefinementType.WEEKLY)

    def test_process_without_refinement_type(self):
        # Execution & Asserção
        with self.assertRaises(ValueError) as context:
            self.engine.process(MagicMock(spec=PandasDF))
        self.assertEqual(str(context.exception), "Refinement type not set")

    def test_process_summary(self):
        # Preparation
        self.engine.set_refinement_type(RefinementType.SUMMARY)
        df = MagicMock(spec=PandasDF)
        transformed_df = MagicMock(spec=PandasDF)
        self.summary_transformer.apply.return_value = transformed_df

        # Execution
        result = self.engine.process(df)

        # Asserts
        self.summary_transformer.apply.assert_called_once_with(dataframe=df)
        self.assertEqual(result, transformed_df)

    def test_process_monthly(self):
        # Preparation
        self.engine.set_refinement_type(RefinementType.MONTHLY)
        df = MagicMock(spec=PandasDF)
        transformed_df = MagicMock(spec=PandasDF)
        self.monthly_transformer.apply.return_value = transformed_df

        # Execution
        result = self.engine.process(df)

        # Asserts
        self.monthly_transformer.apply.assert_called_once_with(dataframe=df)
        self.assertEqual(result, transformed_df)

    def test_process_weekly(self):
        # Preparation
        self.engine.set_refinement_type(RefinementType.WEEKLY)
        df = MagicMock(spec=PandasDF)
        transformed_df = MagicMock(spec=PandasDF)
        self.weekly_transformer.apply.return_value = transformed_df

        # Execution
        result = self.engine.process(df)

        # Asserts
        self.weekly_transformer.apply.assert_called_once_with(dataframe=df)
        self.assertEqual(result, transformed_df)


if __name__ == "__main__":
    unittest.main()
