import unittest
import pandas as pd
from datetime import datetime, date, time
from src.etl.engines.tools.casting import (
    DateCastingStrategy,
    BoolCastingStrategy,
    DoubleCastingStrategy,
    DurationHHMMSSCastingStrategy,
    DurationHHMMCastingStrategy,
    IntegerCastingStrategy,
    OrdinalCastingStrategy,
    StringCastingStrategy,
    TimestampCastingStrategy
)

class TestCastingStrategies(unittest.TestCase):

    def test_date_casting_strategy(self):
        strategy = DateCastingStrategy()
        df = pd.DataFrame({"date_col": ["2024-09-28", None, "2023-05-15"]})
        result = strategy.cast(df["date_col"])
        expected = pd.Series([date(2024, 9, 28), date(1900, 1, 1), date(2023, 5, 15)], name="date_col")
        pd.testing.assert_series_equal(result, expected)

    def test_bool_casting_strategy(self):
        strategy = BoolCastingStrategy()
        df = pd.DataFrame({"bool_col": ["True", "False", None]})
        result = strategy.cast(df["bool_col"])
        expected = pd.Series([True, False, False], name="bool_col")
        pd.testing.assert_series_equal(result, expected)

    def test_double_casting_strategy(self):
        strategy = DoubleCastingStrategy()
        df = pd.DataFrame({"double_col": ["1.1", None, "2.2"]})
        result = strategy.cast(df["double_col"])
        expected = pd.Series([1.1, 0.0, 2.2], name="double_col")
        pd.testing.assert_series_equal(result, expected)

    def test_duration_hhmmss_casting_strategy(self):
        strategy = DurationHHMMSSCastingStrategy()
        df = pd.DataFrame({"duration_col": ["12:34:56", None, "01:23:45"]})
        result = strategy.cast(df["duration_col"])
        expected = pd.Series([time(12, 34, 56), time(0, 0, 0), time(1, 23, 45)], name="duration_col")
        pd.testing.assert_series_equal(result, expected)

    def test_duration_hhmm_casting_strategy(self):
        strategy = DurationHHMMCastingStrategy()
        df = pd.DataFrame({"duration_col": ["12:34", None, "01:23"]})
        result = strategy.cast(df["duration_col"])
        expected = pd.Series([time(12, 34), time(0, 0), time(1, 23)], name="duration_col")
        pd.testing.assert_series_equal(result, expected)

    def test_integer_casting_strategy(self):
        strategy = IntegerCastingStrategy()
        df = pd.DataFrame({"int_col": ["1", None, "2"]})
        result = strategy.cast(df["int_col"])
        expected = pd.Series([1, 0, 2], name="int_col")
        pd.testing.assert_series_equal(result, expected)

    def test_ordinal_casting_strategy(self):
        strategy = OrdinalCastingStrategy()
        df = pd.DataFrame({"ordinal_col": ["a", "b", "c"]})
        result = strategy.cast(df["ordinal_col"])
        expected = pd.Series(["a", "b", "c"], dtype="category", name="ordinal_col")
        pd.testing.assert_series_equal(result, expected)

    def test_string_casting_strategy(self):
        strategy = StringCastingStrategy()
        df = pd.DataFrame({"string_col": ["a", None, "c"]})
        result = strategy.cast(df["string_col"])
        expected = pd.Series(["a", '', "c"], dtype="string", name="string_col")
        pd.testing.assert_series_equal(result, expected)

    def test_timestamp_casting_strategy(self):
        strategy = TimestampCastingStrategy()
        df = pd.DataFrame({"timestamp_col": ["2024-09-28 12:34:56", None, "2023-05-15 01:23:45"]})
        result = strategy.cast(df["timestamp_col"])
        expected = pd.Series([
            datetime(2024, 9, 28, 12, 34, 56),
            datetime(1900, 1, 1, 0, 0, 0),
            datetime(2023, 5, 15, 1, 23, 45)
        ], name="timestamp_col")
        pd.testing.assert_series_equal(result, expected)

if __name__ == "__main__":
    unittest.main()