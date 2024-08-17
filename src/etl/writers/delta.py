from deltalake import write_deltalake
from polars import DataFrame

from src.etl.definitions import Path, Writer


class DeltaWriter(Writer):

    def __init__(self, path: Path) -> None:
        super().__init__(path=path)

    def write_dataframe(self, dataframe: DataFrame) -> None:
        self.logger.info(f"Starting writing process. FORMAT: Delta | PATH: {self.path}")
        write_deltalake(self.path, dataframe.to_pandas(), mode="overwrite")
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")
