from typing import Literal, Union

from pandas import Series, Timedelta, Timestamp


class SummaryDataFrameAggregator:

    @staticmethod
    def calculate_date_aggregation(
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
    def calculate_longest_streak(dates: Series) -> int:
        if dates.empty:
            return 0
        dates = dates.sort_values()
        streaks = (dates.diff() != Timedelta(days=1)).cumsum()
        return streaks.value_counts().max()

    @staticmethod
    def calculate_longest_gap(dates: Series) -> int:
        if dates.empty:
            return 0
        dates = dates.sort_values()
        gaps = dates.diff().dt.days[1:]
        return gaps.max() if not gaps.empty else 0
