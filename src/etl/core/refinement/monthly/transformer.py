from src.etl.core.definitions import PandasDF, Transformer


class MonthlyDataFrameTransformer(Transformer):

    def apply(self, dataframe: PandasDF) -> PandasDF:
        return dataframe
