from typing import List

from src.etl.core.definitions import Engine, EngineType, PandasDF, Splitter, Tool
from src.etl.engines.tools.schema import SchemaTool
from src.etl.engines.tools.splitter import CleaningSplitter
from src.shared.utils import DictUtils


class CleaningEngine(Engine):

    def __init__(
        self,
        tool: Tool = SchemaTool(),
        splitter: Splitter = CleaningSplitter(),
    ):
        super().__init__(class_name=__class__.__name__, type=EngineType.CLEANING, tool=tool, splitter=splitter)

    def _explode_json_column(self, dataframe: PandasDF, field_name: str) -> PandasDF:
        base_dataframe = dataframe.drop([field_name], axis=1)
        exploded_json_columns = dataframe[field_name].apply(DictUtils.deserialize_dict).apply(self.pd.Series)
        return self.pd.concat([base_dataframe, exploded_json_columns], axis=1)

    def _reorder_columns(self, dataframe: PandasDF, start_cols: List[str], end_cols: List[str]) -> PandasDF:
        variable_columns = [col for col in dataframe.columns if col not in start_cols + end_cols]
        new_column_order = start_cols + variable_columns + end_cols
        return dataframe[new_column_order]

    def _drop_columns(self, dataframe: PandasDF, columns: List[str]) -> PandasDF:
        return dataframe.drop(columns, axis=1)

    def process(self, dataframe: PandasDF) -> PandasDF:
        self.logger.info("Starting data cleaning process")
        return (
            dataframe.pipe(self._explode_json_column, field_name="element_string")
            .pipe(
                self._reorder_columns,
                start_cols=["date_input", "element_category", "element_name"],
                end_cols=["user_id", "schema_encoded", "created_at", "updated_at"],
            )
            .pipe(self.tool.apply)
            .pipe(self._drop_columns, columns=["id", "entry_date", "op", "schema_dtypes", "schema_fields"])
        )
