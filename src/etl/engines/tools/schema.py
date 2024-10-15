from json import loads as json_loads
from typing import Dict

from src.etl.core.definitions import PandasDF, Tool
from src.etl.engines.tools.casting import CastingStrategyFactory


class SchemaTool(Tool):
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
            for column, column_type in schema.items():
                strategy = CastingStrategyFactory.get_strategy(column_type)
                df_merged[column] = df_merged[column].replace("", None)
                df_merged[column] = strategy.cast(df_merged[column])

        return df_merged
