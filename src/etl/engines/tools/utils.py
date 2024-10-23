from typing import List

from src.etl.core.definitions import PandasDF, TableName


def split_dataframe(
    dataframe: PandasDF, 
    column_to_split: str
) -> List[PandasDF]:
    subsets = dataframe[column_to_split].unique()
    return [dataframe[dataframe[column_to_split] == subset] for subset in subsets]


def get_subset_table_name(
    dataframe: PandasDF, 
    subset_col_id: str
) -> TableName:
    table_name = dataframe[subset_col_id].unique()[0]
    return TableName(table_name)
