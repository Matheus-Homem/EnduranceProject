from polars import DataFrame

from src.etl.definitions import Path, Writer


class ParquetWriter(Writer):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def write_dataframe(self, dataframe: DataFrame, path: Path) -> None:
        self.logger.info(f"Starting writing process. FORMAT: Parquet | PATH: {path}")
        dataframe.write_parquet(f"{path}")
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")
