from src.etl.definitions import Writer, Table
from polars import DataFrame


class ParquetWriter(Writer):

    def __init__(self, target: Table) -> None:
        super().__init__(target=target)

    def write_data(self, dataframe: DataFrame) -> None:
        self.logger.info(f"Starting writing process. PATH: {self.target}")
        dataframe.write_parquet(self.target)
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")

        
