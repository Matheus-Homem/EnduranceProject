from polars import DataFrame

from src.etl.definitions import Writer, Path


class ParquetWriter(Writer):

    def __init__(self, path: Path) -> None:
        super().__init__(path=path)

    def write_data(self, dataframe: DataFrame) -> None:
        self.logger.info(f"Starting writing process. FORMAT: Parquet | PATH: {self.path}")
        dataframe.write_parquet(f"{self.path}")
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")
