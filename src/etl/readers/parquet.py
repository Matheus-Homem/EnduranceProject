from polars import DataFrame, read_parquet

from src.etl.definitions import Path, Reader


class ParquetReader(Reader):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def read_dataframe(self, source: Path) -> DataFrame:
        self.logger.info(f"Reading data from {source} using Parquet format")
        df = read_parquet(source)
        return df
