from datetime import datetime
from src.etl.core.definitions import CastingStrategy, DataType, PandasDF


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
    def cast(self, col: PandasDF) -> PandasDF:
        col = col.fillna(value="1900-01-01")
        return col.apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date() if x else None)


class BoolCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        return col.apply(lambda x: True if x == "True" else False if x == "False" else False)


class DoubleCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        return col.apply(lambda x: float(x) if x else 0)


class DurationHHMMSSCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        col = col.fillna(value="00:00:00")
        return col.apply(lambda x: datetime.strptime(x, "%H:%M:%S").time() if x else None)


class DurationHHMMCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        col = col.fillna(value="00:00")
        return col.apply(lambda x: datetime.strptime(x, "%H:%M").time() if x else None)


class IntegerCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        return col.apply(lambda x: int(x) if x else 0)
    

class OrdinalCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        return col.astype('category')


class StringCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        col = col.fillna("")
        return col.astype("string")


class TimestampCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        col = col.fillna(value="1900-01-01 00:00:00")
        return col.apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S") if x else None)