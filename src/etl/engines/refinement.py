from typing import List, Optional

from src.etl.core.definitions import Engine, EngineType, PandasDF


class RefinementEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__, type=EngineType.REFINEMENT)

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
