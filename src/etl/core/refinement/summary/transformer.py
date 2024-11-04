from typing import Dict, List, Optional

from src.etl.core.definitions import PandasDF, Transformer
from src.etl.core.refinement.summary.aggregator import SummaryDataFrameAggregator
from src.etl.core.refinement.summary.melter import SummaryDataFrameMelter


class SummaryDataFrameTransformer(Transformer):

    def __init__(
        self,
        melter: SummaryDataFrameMelter = SummaryDataFrameMelter(),
    ):
        super().__init__()
        self.melter = melter
        self.habit_detail_dict = {
            "navigator": "book",
        }
        self.default_columns = ["element_category", "element_name", "user_id", "date_input", "schema_encoded", "created_at", "updated_at"]
        self.ordened_columns = [
            "element_category",
            "element_name",
            "user_id",
            "habit_group",
            "habit_action",
            "habit_detail",
            "total",
            "first_date",
            "last_date",
            "days_since_last",
            "longest_streak",
            "longest_gap",
        ]

        self.dtype_dict = {
            "element_category": "string",
            "element_name": "string",
            "user_id": "string",
            "habit_group": "string",
            "habit_action": "string",
            "habit_detail": "string",
            "total": "Int64",
            "first_date": "datetime64[ns]",
            "last_date": "datetime64[ns]",
            "days_since_last": "Int64",
            "longest_streak": "Int64",
            "longest_gap": "Int64",
        }

        self.columns_to_sort = [
            "element_category",
            "element_name",
            "user_id",
            "habit_group",
            "habit_action",
            "habit_detail",
        ]

    def _get_habit_detail_col(
        self,
        dataframe: PandasDF,
    ) -> Optional[str]:
        return self.habit_detail_dict.get(dataframe["element_name"].unique()[0])

    def _get_value_columns(self, dataframe: PandasDF) -> List[str]:
        return [col for col in dataframe.columns if col not in self.default_columns and dataframe[col].dtype == "bool"]

    def _set_habit_group(self, dataframe: PandasDF) -> PandasDF:
        element_name = dataframe["element_name"].unique()[0]
        habit_group_dict = {
            "navigator": "book",
            "diplomat": "relate",
            "alchemist": "emotion",
        }

        dataframe["habit_group"] = habit_group_dict.get(element_name)
        return dataframe

    def _calculate_summary_fields(
        self,
        dataframe: PandasDF,
        group_columns: List[str] = ["user_id", "element_category", "element_name", "habit_detail", "habit_action", "habit_group"],
    ) -> PandasDF:
        valid_group_columns = [col for col in group_columns if not dataframe[col].isnull().all()]
        df_grouped = (
            dataframe.groupby(valid_group_columns)
            .agg(
                total=("date_input", lambda x: SummaryDataFrameAggregator.calculate_date_aggregation(x[dataframe["value"] > 0], "count")),
                first_date=("date_input", lambda x: SummaryDataFrameAggregator.calculate_date_aggregation(x[dataframe["value"] > 0], "min")),
                last_date=("date_input", lambda x: SummaryDataFrameAggregator.calculate_date_aggregation(x[dataframe["value"] > 0], "max")),
                longest_streak=("date_input", lambda x: SummaryDataFrameAggregator.calculate_longest_streak(x[dataframe["value"] > 0])),
                longest_gap=("date_input", lambda x: SummaryDataFrameAggregator.calculate_longest_gap(x[dataframe["value"] > 0])),
            )
            .reset_index()
        )
        if "habit_detail" not in df_grouped.columns:
            df_grouped["habit_detail"] = None
        return df_grouped

    def _add_fields(self, dataframe: PandasDF) -> PandasDF:
        dataframe["days_since_last"] = (
            (self.pd.to_datetime("today") - dataframe["last_date"]).dt.days if not dataframe["last_date"].isnull().all() else None
        )
        return dataframe

    def _order_columns(self, dataframe: PandasDF, column_sequence: List[str]) -> PandasDF:
        return dataframe[column_sequence]

    def _cast_columns(self, dataframe: PandasDF, dtypes: Dict[str, str]) -> PandasDF:
        return dataframe.astype(dtypes)

    def _sort_columns(self, dataframe: PandasDF, sort_keys: List[str]) -> PandasDF:
        return dataframe.sort_values(by=sort_keys)

    def apply(self, dataframe: PandasDF) -> PandasDF:
        detail_column = self._get_habit_detail_col(dataframe)
        value_columns = self._get_value_columns(dataframe)

        return (
            dataframe.pipe(self.melter.apply, detail=detail_column, value_vars=value_columns)
            .pipe(self._set_habit_group)
            .pipe(self._calculate_summary_fields)
            .pipe(self._add_fields)
            .pipe(self._order_columns, column_sequence=self.ordened_columns)
            .pipe(self._cast_columns, dtypes=self.dtype_dict)
            .pipe(self._sort_columns, sort_keys=self.columns_to_sort)
        )
