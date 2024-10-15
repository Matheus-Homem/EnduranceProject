from datetime import datetime, timedelta

from pandas import Series, to_datetime

from src.etl.core.definitions import CastingStrategy, DataType


class CastingStrategyFactory:
    @staticmethod
    def get_strategy(column_type: str) -> CastingStrategy:
        dtype = DataType(column_type)

        if dtype == DataType.DATE:
            return DateCastingStrategy()
        if dtype == DataType.BOOL:
            return BoolCastingStrategy()
        if dtype == DataType.DOUBLE:
            return DoubleCastingStrategy()
        if dtype == DataType.DURATION_HHMMSS:
            return DurationHHMMSSCastingStrategy()
        if dtype == DataType.DURATION_HHMM:
            return DurationHHMMCastingStrategy()
        if dtype == DataType.INTEGER:
            return IntegerCastingStrategy()
        if dtype == DataType.ORDINAL:
            return OrdinalCastingStrategy()
        if dtype == DataType.STRING:
            return StringCastingStrategy()
        if dtype == DataType.TIMESTAMP:
            return TimestampCastingStrategy()
        return None


class DateCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return to_datetime(col, format="%Y-%m-%d", errors="coerce").dt.date.astype("datetime64[ns]")


class BoolCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.apply(lambda x: True if x == "True" else False if x == "False" else None).astype("bool")


class DoubleCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.astype("float64") / 100


class DurationHHMMSSCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.apply(
            lambda x: int(timedelta(hours=int(x[:-4]), minutes=int(x[-4:-2]), seconds=int(x[-2:])).total_seconds()) if x else None
        ).astype("Int64")


class DurationHHMMCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.apply(lambda x: int(timedelta(hours=int(x[-4:-2]), minutes=int(x[-2:])).total_seconds()) if x else None).astype("Int64")


class IntegerCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.astype("Int64")


class OrdinalCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.astype("category")


class StringCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.astype("string")


class TimestampCastingStrategy(CastingStrategy):
    def cast(self, col: Series) -> Series:
        return col.apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S") if x else None).astype("datetime64[ns]")
