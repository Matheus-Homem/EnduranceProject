from typing import List, Literal, Optional, Union

from pandas import Series, Timedelta, Timestamp, to_datetime

from src.etl.core.definitions import PandasDF, Transformer


class SummaryDataFrameTransformer(Transformer):

    @staticmethod
    def _calculate_date_aggregation(
        dates: Series,
        aggregate_by: Literal["count", "min", "max"],
    ) -> Union[int, Timestamp, None]:
        if not (dates != Timestamp(0)).any():
            return None
        elif aggregate_by == "count":
            return dates.count()
        elif aggregate_by == "min":
            return dates.min()
        elif aggregate_by == "max":
            return dates.max()

    @staticmethod
    def _calculate_longest_streak(dates: Series) -> int:
        if dates.empty:
            return 0
        dates = dates.sort_values()
        streaks = (dates.diff() != Timedelta(days=1)).cumsum()
        return streaks.value_counts().max()

    @staticmethod
    def _calculate_longest_gap(dates: Series) -> int:
        if dates.empty:
            return 0
        dates = dates.sort_values()
        gaps = dates.diff().dt.days[1:]
        return gaps.max() if not gaps.empty else 0

    def _diplomat(
        self,
        cleaned_dataframe: PandasDF,
        id_vars: List[str] = ["element_category", "element_name", "user_id", "date_input"],
        value_vars: List[str] = ["animals", "family", "friends", "society", "contacts", "coworkers"],
        var_name: str = "habit_action",
        habit_detail_col: Optional[str] = None,
    ) -> PandasDF:
        df_right = cleaned_dataframe.melt(
            id_vars=[id_vars, habit_detail_col],
            value_vars=value_vars,
            var_name=var_name,
            value_name="value",
        )

        df_right["habit_action"] = df_right["habit_action"].str.replace("_0", "")
        df_right["habit_group"] = "relate"

        df_right = (
            df_right.groupby(["user_id", "element_category", "element_name", "habit_action", "habit_group"])
            .agg(
                total=("date_input", lambda x: SummaryDataFrameTransformer._calculate_date_aggregation(x[df_right["value"] > 0], "count")),
                first_date=("date_input", lambda x: SummaryDataFrameTransformer._calculate_date_aggregation(x[df_right["value"] > 0], "min")),
                last_date=("date_input", lambda x: SummaryDataFrameTransformer._calculate_date_aggregation(x[df_right["value"] > 0], "max")),
                longest_streak=("date_input", lambda x: SummaryDataFrameTransformer._calculate_longest_streak(x[df_right["value"] > 0])),
                longest_gap=("date_input", lambda x: SummaryDataFrameTransformer._calculate_longest_gap(x[df_right["value"] > 0])),
            )
            .reset_index()
        )

        df_final = df_right
        df_final["days_since_last"] = (to_datetime("today") - df_final["last_date"]).dt.days
        df_final["habit_detail"] = None
        df_final = df_final[
            [
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
        ]
        df_final = df_final.sort_values(by=["element_category", "element_name", "user_id", "habit_group", "habit_action", "habit_detail"])

        return df_final

    def _navigator(self):

        df_right = df_navigator.melt(
            id_vars=["element_category", "element_name", "user_id", "book_0", "date_input"],
            value_vars=["read_0", "listen_0", "notes_0"],
            var_name="habit_action",
            value_name="value",
        )

        df_right["habit_action"] = df_right["habit_action"].str.replace("_0", "")
        df_right["habit_group"] = "book"

        def count_with_none(series):
            if not series.any():
                return 0
            else:
                return series.count()

        def min_with_none(series):
            if not series.any():
                return None
            else:
                return series.min()

        def max_with_none(series):
            if not series.any():
                return None
            else:
                return series.max()

        def calculate_longest_streak(dates):
            if dates.empty:
                return 0
            dates = dates.sort_values()
            streaks = (dates.diff() != pd.Timedelta(days=1)).cumsum()
            return streaks.value_counts().max()

        def calculate_longest_gap(dates):
            if dates.empty:
                return 0
            dates = dates.sort_values()
            gaps = dates.diff().dt.days[1:]
            return gaps.max() if not gaps.empty else 0

        df_right = (
            df_right.groupby(["user_id", "element_category", "element_name", "book_0", "habit_action", "habit_group"])
            .agg(
                total=("date_input", lambda x: count_with_none(x[df_right["value"] > 0])),
                first_date=("date_input", lambda x: min_with_none(x[df_right["value"] > 0])),
                last_date=("date_input", lambda x: max_with_none(x[df_right["value"] > 0])),
                longest_streak=("date_input", lambda x: calculate_longest_streak(x[df_right["value"] > 0])),
                longest_gap=("date_input", lambda x: calculate_longest_gap(x[df_right["value"] > 0])),
            )
            .reset_index()
        )

        df_final = df_right.rename(columns={"book_0": "habit_detail"})
        df_final["days_since_last"] = (pd.to_datetime("today") - df_final["last_date"]).dt.days
        df_final = df_final[
            [
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
        ]
        df_final = df_final.sort_values(by=["element_category", "element_name", "user_id", "habit_group", "habit_action", "habit_detail"])

        return df_final

    def _get_habit_detail_col(self, dataframe: PandasDF) -> Optional[str]:
        pass

    def _melt_dataframe(
        self,
        dataframe: PandasDF,
        value_vars: List[str],
        id_vars: List[str] = ["element_category", "element_name", "user_id", "date_input"],
        habit_detail_col: Optional[str] = None,
    ) -> PandasDF:
        return dataframe.melt(
            id_vars=[id_vars, habit_detail_col],
            value_vars=value_vars,
            var_name="habit_action",
            value_name="value",
        )

    def _set_habit_group(self, dataframe: PandasDF) -> PandasDF:
        pass

    def _group_dataframe(self, dataframe: PandasDF) -> PandasDF:
        pass

    def _add_fields(self, dataframe: PandasDF) -> PandasDF:
        pass

    def _set_habit_detail(self, dataframe: PandasDF) -> PandasDF:
        pass

    def _reshape_dataframe(self, dataframe: PandasDF) -> PandasDF:
        return dataframe[
            [
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
        ].sort_values(
            by=[
                "element_category",
                "element_name",
                "user_id",
                "habit_group",
                "habit_action",
                "habit_detail",
            ]
        )

    def apply(self, dataframe: PandasDF) -> PandasDF:
        habit_detail_col = self._get_habit_detail_col(dataframe)
        return (
            dataframe.pipe(self._melt_dataframe, habit_detail_col=habit_detail_col)
            .pipe(self._set_habit_group)
            .pipe(self._group_dataframe)
            .pipe(self._add_fields)
            .pipe(self._set_habit_detail)
            .pipe(self._reshape_dataframe)
        )
