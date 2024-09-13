from deltalake import DeltaTable
from polars import DataFrame

from src.etl.definitions import Path, Reader


class DeltaReader(Reader):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def read_dataframe(self, source: Path) -> DataFrame:
        self.logger.info(f"Starting reading process. FORMAT: Delta | TARGET: {source}")
        delta_table = DeltaTable(source)
        df = DataFrame(delta_table.to_pandas())
        self.logger.info(f"Data read successfully from {source} with {df.shape[0]} records")
        return df
