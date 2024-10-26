import unittest
from datetime import date, datetime

import pandas as pd

from src.etl.engines.transformers.casting import (
    BoolCastingStrategy,
    DateCastingStrategy,
    DoubleCastingStrategy,
    DurationHHMMCastingStrategy,
    DurationHHMMSSCastingStrategy,
    IntegerCastingStrategy,
    OrdinalCastingStrategy,
    StringCastingStrategy,
    TimestampCastingStrategy,
)


class TestCastingStrategies(unittest.TestCase):

    def test_date_casting_strategy(self):
        strategy = DateCastingStrategy()
        df = pd.DataFrame({"date_col": ["2024-09-28", None, "2023-05-15"]})
        result = strategy.cast(df["date_col"])
        expected = pd.Series(
            [date(2024, 9, 28), None, date(2023, 5, 15)],
            name="date_col",
            dtype="datetime64[ns]",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_bool_casting_strategy(self):
        strategy = BoolCastingStrategy()
        df = pd.DataFrame({"bool_col": ["True", "False", None]})
        result = strategy.cast(df["bool_col"])
        expected = pd.Series(
            [True, False, None],
            name="bool_col",
            dtype="bool",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_double_casting_strategy(self):
        strategy = DoubleCastingStrategy()
        df = pd.DataFrame({"double_col": ["101", None, "220", "0330", "0010"]})
        result = strategy.cast(df["double_col"])
        expected = pd.Series(
            [1.01, None, 2.20, 3.30, 0.10],
            name="double_col",
            dtype="float64",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_duration_hhmmss_casting_strategy(self):
        strategy = DurationHHMMSSCastingStrategy()
        df = pd.DataFrame({"duration_col": ["235900", None, "000001", "10000"]})
        result = strategy.cast(df["duration_col"])
        expected = pd.Series(
            [86340, None, 1, 3600],
            name="duration_col",
            dtype="Int64",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_duration_hhmm_casting_strategy(self):
        strategy = DurationHHMMCastingStrategy()
        df = pd.DataFrame({"duration_col": ["2359", None, "0100"]})
        result = strategy.cast(df["duration_col"])
        expected = pd.Series(
            [86340, None, 3600],
            name="duration_col",
            dtype="Int64",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_integer_casting_strategy(self):
        strategy = IntegerCastingStrategy()
        df = pd.DataFrame({"int_col": ["1", None, "0001", "2"]})
        result = strategy.cast(df["int_col"])
        expected = pd.Series(
            [1, None, 1, 2],
            name="int_col",
            dtype="Int64",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_ordinal_casting_strategy(self):
        strategy = OrdinalCastingStrategy()
        df = pd.DataFrame({"ordinal_col": ["a", "b", "c", None]})
        result = strategy.cast(df["ordinal_col"])
        expected = pd.Series(
            ["a", "b", "c", None],
            name="ordinal_col",
            dtype="category",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_string_casting_strategy(self):
        strategy = StringCastingStrategy()
        df = pd.DataFrame({"col_to_string": ["a", None, "c"]})
        result = strategy.cast(df["col_to_string"])
        expected = pd.Series(
            ["a", None, "c"],
            name="col_to_string",
            dtype="string",
        )
        pd.testing.assert_series_equal(result, expected)

    def test_timestamp_casting_strategy(self):
        strategy = TimestampCastingStrategy()
        df = pd.DataFrame({"timestamp_col": ["2024-09-28 12:34:56", None, "2023-05-15 01:23:45", "2024-10-14T20:43"]})
        result = strategy.cast(df["timestamp_col"])
        expected = pd.Series(
            [datetime(2024, 9, 28, 12, 34, 56), None, datetime(2023, 5, 15, 1, 23, 45), datetime(2024, 10, 14, 20, 43)],
            name="timestamp_col",
            dtype="datetime64[ns]",
        )
        pd.testing.assert_series_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
