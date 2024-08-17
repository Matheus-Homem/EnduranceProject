from polars import DataFrame, read_parquet

from src.etl.definitions import Path, Reader


class ParquetReader(Reader):

    def __init__(self, source: Path) -> None:
        super().__init__(source=source)

    def read_dataframe(self) -> DataFrame:
        self.logger.info(
            f"Starting reading process. FORMAT: Parquet | TARGET: {self.source}"
        )
        df = read_parquet(self.source)
        self.logger.info(
            f"Data read successfully from {self.source} with {df.shape[0]} records"
        )
        return df
