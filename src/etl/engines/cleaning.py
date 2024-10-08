from json import loads as json_loads
from typing import List

from src.etl.core.definitions import Engine, PandasDF, Splitter, Tool
from src.etl.engines.tools.casting import CastingTool
from src.etl.engines.tools.splitter import CleaningSplitter


class CleaningEngine(Engine):

    def __init__(
        self,
        tool: Tool = CastingTool(),
        splitter: Splitter = CleaningSplitter(),
    ):
        super().__init__(class_name=__class__.__name__, tool=tool, splitter=splitter)

    def _reorder_columns(self, dataframe: PandasDF, start_columns: List[str], end_columns: List[str]) -> PandasDF:
        variable_columns = [col for col in dataframe.columns if col not in start_columns + end_columns]
        new_column_order = start_columns + variable_columns + end_columns
        return dataframe[new_column_order]

    def _cast_columns(self, dataframe: PandasDF) -> PandasDF:
        return self.tool.apply(dataframe)

    def _drop_columns(self, dataframe: PandasDF) -> PandasDF:
        return dataframe.drop(["id", "entry_date", "op"], axis=1)

    def _explode_json_column(self, dataframe: PandasDF, field_name: str) -> PandasDF:
        df1 = dataframe.drop([field_name], axis=1)
        df2 = dataframe[field_name].apply(json_loads).apply(self.pd.Series)
        return self.pd.concat([df1, df2], axis=1)

    def process(self, dataframe: PandasDF) -> PandasDF:
        self.logger.info("Starting data cleaning process")
        df_exploded = self._explode_json_column(dataframe, field_name="element_string")
        df_ordered = self._reorder_columns(
            df_exploded,
            start_columns=["date_input", "element_category", "element_name"],
            end_columns=["user_id", "schema_encoded", "created_at", "updated_at"],
        )
        df_casted = self._cast_columns(df_ordered)
        df_cleaned = self._drop_columns(df_casted)
        return df_cleaned
