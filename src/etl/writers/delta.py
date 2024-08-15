from polars import DataFrame
from deltalake import write_deltalake

from src.etl.definitions import Writer, Path


class DeltaWriter(Writer):

    def __init__(self, path: Path) -> None:
        super().__init__(path=path)

    def write_data(self, dataframe: DataFrame) -> None:
        self.logger.info(f"Starting writing process. FORMAT: Delta | PATH: {self.path}")
        write_deltalake(self.path, dataframe.to_pandas(), mode="overwrite")
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")
