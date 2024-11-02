from typing import List

from src.etl.core.definitions import Engine, EngineType, PandasDF
from src.etl.core.refinement.monthly.transformer import MonthlyDataFrameTransformer
from src.etl.core.refinement.summary.transformer import SummaryDataFrameTransformer
from src.etl.core.refinement.weekly.transformer import WeeklyDataFrameTransformer


class RefinementEngine(Engine):

    def __init__(
        self,
        summary_transformer: SummaryDataFrameTransformer = SummaryDataFrameTransformer(),
        monthly_transformer: MonthlyDataFrameTransformer = MonthlyDataFrameTransformer(),
        weekly_transformer: WeeklyDataFrameTransformer = WeeklyDataFrameTransformer(),
    ):
        super().__init__(class_name=__class__.__name__, type=EngineType.REFINEMENT)
        self.summary_transformer = summary_transformer
        self.monthly_transformer = monthly_transformer
        self.weekly_transformer = weekly_transformer

    def process(self, table: PandasDF) -> List[PandasDF]:
        self.logger.info("Starting data refinement process")
        df_summary = self.summary_transformer.apply(dataframe=table)
        df_monthly = self.monthly_transformer.apply(dataframe=table)
        df_weekly = self.weekly_transformer.apply(dataframe=table)
        return [df for df in [df_summary, df_monthly, df_weekly] if df is not None]
