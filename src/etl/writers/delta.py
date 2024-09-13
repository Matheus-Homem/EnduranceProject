from deltalake import write_deltalake
from polars import DataFrame

from src.etl.definitions import Path, Writer


class DeltaWriter(Writer):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def write_dataframe(self, dataframe: DataFrame, path: Path) -> None:
        self.logger.info(f"Starting writing process. FORMAT: Delta | PATH: {path}")
        write_deltalake(path, dataframe.to_pandas(), mode="overwrite")
        self.logger.info(f"Data written successfully with {dataframe.shape[0]} records")
