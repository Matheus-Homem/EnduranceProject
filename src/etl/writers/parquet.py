from polars import DataFrame

from src.etl.definitions import Writer


class ParquetWriter(Writer):
    FORMAT: str = "parquet"

    def __init__(self, target: str) -> None:
        super().__init__(target=target)
        self.path = f"{target}.{self.FORMAT}"

    def write_data(self, dataframe: DataFrame) -> None:
        self.logger.info(f"Starting writing process. PATH: {self.path}")
        dataframe.write_parquet(f"{self.path}")
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")
