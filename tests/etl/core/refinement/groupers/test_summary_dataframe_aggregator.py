from unittest import TestCase

import pandas as pd

from src.etl.core.refinement.summary.aggregator import SummaryDataFrameAggregator


class TestSummaryDataFrameAggregator(TestCase):

    def test_calculate_date_aggregation(self):
        dates = pd.Series([pd.Timestamp("2022-02-10"), pd.Timestamp("2022-02-11")])
        result = SummaryDataFrameAggregator.calculate_date_aggregation(dates, "count")
        self.assertEqual(result, 2)

        result = SummaryDataFrameAggregator.calculate_date_aggregation(dates, "min")
        self.assertEqual(result, pd.Timestamp("2022-02-10"))

        result = SummaryDataFrameAggregator.calculate_date_aggregation(dates, "max")
        self.assertEqual(result, pd.Timestamp("2022-02-11"))

    def test_calculate_longest_streak(self):
        dates = pd.Series([pd.Timestamp("2022-02-10"), pd.Timestamp("2022-02-11")])
        result = SummaryDataFrameAggregator.calculate_longest_streak(dates)
        self.assertEqual(result, 2)

    def test_calculate_longest_gap(self):
        dates = pd.Series([pd.Timestamp("2022-02-10"), pd.Timestamp("2022-02-11")])
        result = SummaryDataFrameAggregator.calculate_longest_gap(dates)
        self.assertEqual(result, 1)
