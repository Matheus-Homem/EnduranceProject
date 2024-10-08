from json import loads as json_loads
from typing import Dict

from src.etl.core.definitions import CastingStrategy, PandasDF, Tool


class CastingTool(Tool):
    def _read_schema_dataframe(self, schema_path: str) -> PandasDF:
        df_schema = self.pd.read_parquet(schema_path)
        df_schema_filtered = df_schema[["schema_encoded", "element_category", "element_name", "schema_dtypes", "schema_fields"]]
        return df_schema_filtered

    def _get_dtype_dict(self, df_schema: PandasDF, schema_encoded: str) -> Dict[str, str]:
        try:
            schema = df_schema[(df_schema["schema_encoded"] == schema_encoded)]
            return json_loads(schema["schema_dtypes"].iloc[0])
        except Exception as e:
            raise Exception(f"Error while getting schema dtype dictionary: {e}")

    def apply(self, dataframe: PandasDF) -> PandasDF:
        self.schema = self._read_schema_dataframe("data/bronze/schemas.parquet")
        df_merged = self.pd.merge(dataframe, self.schema, on=["schema_encoded", "element_category", "element_name"], how="inner")

        for schema_code in df_merged["schema_encoded"].unique():
            schema = self._get_dtype_dict(df_merged, schema_code)
            for column, dtype in schema.items():
                strategy = CastingStrategyFactory.get_strategy(dtype)
                strategy.cast(df_merged[column], pandas=self.pd)

        return df_merged


class CastingStrategyFactory:
    @staticmethod
    def get_strategy(dtype: str) -> CastingStrategy:
        if dtype == "date":
            return DateCastingStrategy()
        elif dtype == "bool":
            return BoolCastingStrategy()
        return None


class DateCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF, pandas) -> PandasDF:
        return col.apply(lambda x: pandas.to_datetime(x).date() if pandas.notnull(x) else None)


class BoolCastingStrategy(CastingStrategy):
    def cast(self, col: PandasDF) -> PandasDF:
        return col.apply(lambda x: True if x == "True" else False if x == "False" else None)
