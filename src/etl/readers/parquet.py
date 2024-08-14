from polars import DataFrame

from src.etl.definitions import Reader, Table


class ParquetReader(Reader):
    SOURCE: str = "Parquet"

    def __init__(self, source: Table) -> None:
        super().__init__(source=source)

    def read_data(self) -> DataFrame:
        # self.logger.info(
        #     f"Starting reading process. SOURCE: {self.SOURCE} | TABLE: {self.source.__tablename__}"
        # )
        # Read parquet file
        # self.logger.info(
        #     f"Data read successfully from {self.source.__tablename__} with {df.shape[0]} records"
        # )
        # return df
        pass
