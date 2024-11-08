from typing import List

from src.etl.core.definitions import Engine, EngineType, PandasDF, RefinementType
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
        self.refinement_type = None

    def set_refinement_type(self, type: RefinementType) -> None:
        self.logger.info(f"Setting refinement type to {type.value.upper()}")
        self.refinement_type = type

    def union_dataframes(self, dataframes: List[PandasDF]) -> PandasDF:
        return self._pd.concat(dataframes, ignore_index=True).reset_index(drop=True)

    def process(self, table: PandasDF) -> PandasDF:

        if self.refinement_type is None:
            raise ValueError("Refinement type not set")
        if self.refinement_type == RefinementType.SUMMARY:
            return self.summary_transformer.apply(dataframe=table)
        if self.refinement_type == RefinementType.MONTHLY:
            return self.monthly_transformer.apply(dataframe=table)
        if self.refinement_type == RefinementType.WEEKLY:
            return self.weekly_transformer.apply(dataframe=table)
