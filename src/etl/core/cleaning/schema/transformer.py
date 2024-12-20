from typing import Dict

from os_local import join_paths
from src.etl.core.cleaning.schema.casting import CastingStrategyFactory
from src.etl.core.definitions import PandasDF, Transformer
from src.shared.utils import DictUtils

SCHEMAS_PATH = join_paths("data", "bronze", "schemas")


class SchemaTransformer(Transformer):

    def _read_schema_dataframe(self, schema_path: str) -> PandasDF:
        df_schema = self._pd.read_parquet(schema_path)
        df_schema_filtered = df_schema[["schema_encoded", "element_category", "element_name", "schema_dtypes", "schema_fields"]]
        return df_schema_filtered

    def _get_dtype_dict(self, df_schema: PandasDF, schema_encoded: str) -> Dict[str, str]:
        try:
            schema = df_schema[(df_schema["schema_encoded"] == schema_encoded)]
            return DictUtils.deserialize_dict(schema["schema_dtypes"].iloc[0])
        except Exception as e:
            raise Exception(f"Error while getting schema dtype dictionary: {e}")

    def apply(self, dataframe: PandasDF) -> PandasDF:
        self.schema = self._read_schema_dataframe(SCHEMAS_PATH)
        df_merged = self._pd.merge(dataframe, self.schema, on=["schema_encoded", "element_category", "element_name"], how="inner")

        for schema_code in df_merged["schema_encoded"].unique():
            schema = self._get_dtype_dict(df_merged, schema_code)
            for column, column_type in schema.items():
                strategy = CastingStrategyFactory.get_strategy(column_type)
                df_merged[column] = df_merged[column].replace("", None)
                df_merged[column] = strategy.cast(df_merged[column])

        return df_merged
