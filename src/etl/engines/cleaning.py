from typing import List

from src.etl.core.definitions import Engine, PandasDF, TableName


class CleaningEngine(Engine):

    def __init__(self, column_to_split: str = "element_name"):
        super().__init__(class_name=__class__.__name__)
        self.column_to_split = column_to_split

    def need_split(self) -> bool:
        return True

    def process(self, dataframe: PandasDF) -> PandasDF:
        self.logger.info("Starting data cleaning process")
        return dataframe

    def split(self, dataframe: PandasDF) -> List[PandasDF]:
        self.logger.info("Starting data split process")
        subsets = dataframe[self.column_to_split].unique()
        return [dataframe[dataframe[self.column_to_split] == subset] for subset in subsets]

    def get_table_name(self, dataframe: PandasDF) -> TableName:
        table_name = dataframe[self.column_to_split].unique()[0]
        return TableName(table_name)
