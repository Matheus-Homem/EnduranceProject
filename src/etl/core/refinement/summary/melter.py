from typing import Any, Dict, List, Optional

from src.etl.core.definitions import PandasDF, Transformer

DEFAULT_COLUMNS = ["element_category", "element_name", "user_id", "date_input"]


class SummaryDataFrameMelter(Transformer):

    def __init__(self):
        super().__init__()
        self.value_name = "value"
        self.var_name = "habit_action"

    def _get_detail_columns(self, dataframe: PandasDF, detail_id: str) -> List[str]:
        return list(dataframe.columns[dataframe.columns.str.startswith(detail_id)])

    def _get_value_columns(
        self,
        dataframe: PandasDF,
        values: List[str],
        variant: str,
    ) -> List[str]:
        """
        Variants usually are identifications like '_A', '_B' or '_1', '_2'.
        """
        return [f"{value}{variant}" for value in values if f"{value}{variant}" in dataframe.columns]

    def _melt_without_detail_col(
        self,
        dataframe: PandasDF,
        value_vars: List[str],
        default_cols: List[str] = DEFAULT_COLUMNS,
    ) -> PandasDF:
        return dataframe.melt(
            id_vars=default_cols,
            value_vars=value_vars,
            var_name=self.var_name,
            value_name=self.value_name,
        )

    def _melt_with_detail_col(
        self,
        dataframe: PandasDF,
        value_vars: List[str],
        detail: str,
        default_cols: List[str] = DEFAULT_COLUMNS,
    ) -> PandasDF:
        dataframes_to_concatenate = []

        for col in self._get_detail_columns(dataframe, detail_id=detail):
            variant = col.replace(detail, "")

            df_melted = self._melt_without_detail_col(
                dataframe,
                value_vars=self._get_value_columns(dataframe, values=value_vars, variant=variant),
                default_cols=default_cols + [col],
            )
            df_renamed = df_melted.rename(columns={col: "habit_detail"})
            df_renamed["habit_action"] = df_renamed["habit_action"].str.replace(variant, "")
            dataframes_to_concatenate.append(df_renamed)
        
        return self.pd.concat(dataframes_to_concatenate).reset_index().drop(columns=["index"])

    def apply(
        self,
        dataframe: PandasDF,
        detail: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> PandasDF:
        if detail:
            df_melted = self._melt_with_detail_col(dataframe, detail, **kwargs)
        else:
            df_melted = self._melt_without_detail_col(dataframe, **kwargs)
            df_melted["habit_detail"] = None
        return df_melted
