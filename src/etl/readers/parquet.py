from polars import DataFrame, read_parquet

from src.etl.definitions import Path, Reader


class ParquetReader(Reader):

    def __init__(self) -> None:
        super().__init__()

    def read_dataframe(self, source: Path) -> DataFrame:
        self.logger.info(f"Starting reading process. FORMAT: Parquet | TARGET: {source}")
        df = read_parquet(source)
        self.logger.info(f"Data read successfully from {source} with {df.shape[0]} records")
        return df
