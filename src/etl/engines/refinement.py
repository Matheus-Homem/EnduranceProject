from typing import List, Optional

from src.etl.core.definitions import Engine, EngineType, PandasDF


class RefinementEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__, type=EngineType.REFINEMENT)

    # def _melt_dataframe(
    #     self,
    #     table: PandasDF,
    #     bool_cols: List[str],
    #     id_cols: List[str] = ['element_category', 'element_name', 'user_id', 'date_input'],
    #     activity_content_col: str = None,
    # ) -> PandasDF:
    #     return table.melt(
    #         id_vars=id_cols + activity_content_col,
    #         value_vars=bool_cols,
    #         var_name="column_name",
    #         value_name="column_value"
    #     )

    def _build_summary_statistics(self, cleaned_table: PandasDF) -> Optional[PandasDF]:
        pass

    def _build_monthly_statistics(self, cleaned_table: PandasDF) -> Optional[PandasDF]:
        pass

    def _build_weekly_statistics(self, cleaned_table: PandasDF) -> Optional[PandasDF]:
        pass

    def process(self, table: PandasDF) -> List[PandasDF]:
        self.logger.info("Starting data refinement process")
        df_summary = self._build_summary_statistics(cleaned_table=table)
        df_monthly = self._build_monthly_statistics(cleaned_table=table)
        df_weekly = self._build_weekly_statistics(cleaned_table=table)
        return [df for df in [df_summary, df_monthly, df_weekly] if df is not None]
