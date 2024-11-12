import unittest

from src.etl.core.cleaning.schema.casting import (
    BoolCastingStrategy,
    CastingStrategyFactory,
    DateCastingStrategy,
    DoubleCastingStrategy,
    DurationHHMMCastingStrategy,
    DurationHHMMSSCastingStrategy,
    IntegerCastingStrategy,
    OrdinalCastingStrategy,
    StringCastingStrategy,
    TimestampCastingStrategy,
)
from src.etl.core.definitions import DataType


class TestCastingStrategyFactory(unittest.TestCase):

    def test_get_strategy(self):
        strategy_mapping = {
            DataType.DATE: DateCastingStrategy,
            DataType.BOOL: BoolCastingStrategy,
            DataType.DOUBLE: DoubleCastingStrategy,
            DataType.DURATION_HHMMSS: DurationHHMMSSCastingStrategy,
            DataType.DURATION_HHMM: DurationHHMMCastingStrategy,
            DataType.INTEGER: IntegerCastingStrategy,
            DataType.ORDINAL: OrdinalCastingStrategy,
            DataType.STRING: StringCastingStrategy,
            DataType.TIMESTAMP: TimestampCastingStrategy,
        }

        for column_type, expected_class in strategy_mapping.items():
            with self.subTest(column_type=column_type):
                strategy = CastingStrategyFactory.get_strategy(column_type)
                self.assertIsInstance(strategy, expected_class, f"Strategy for {column_type} should be {expected_class.__name__}")


if __name__ == "__main__":
    unittest.main()
