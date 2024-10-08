from typing import List

from src.etl.core.definitions import PandasDF, Splitter, TableName


class CleaningSplitter(Splitter):

    def __init__(self):
        super().__init__(class_name=__class__.__name__, column_to_split="element_name")

    def split(self, dataframe: PandasDF) -> List[PandasDF]:
        self.logger.info("Starting data split process for cleaning")
        subsets = dataframe[self.column_to_split].unique()
        return [dataframe[dataframe[self.column_to_split] == subset] for subset in subsets]

    def get_table_name(self, dataframe: PandasDF) -> TableName:
        table_name = dataframe[self.column_to_split].unique()[0]
        return TableName(table_name)
