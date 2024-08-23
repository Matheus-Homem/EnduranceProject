from src.etl.definitions import Engine
from polars import DataFrame


class CleanerEngine(Engine):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def process(dataframe: DataFrame) -> DataFrame:
        return dataframe