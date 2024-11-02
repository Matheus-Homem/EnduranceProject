from src.etl.core.definitions import PandasDF, Transformer


class WeeklyDataFrameTransformer(Transformer):

    def apply(self, dataframe: PandasDF) -> PandasDF:
        return dataframe
