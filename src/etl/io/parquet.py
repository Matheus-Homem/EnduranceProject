from src.etl.definitions import Layer
from src.etl.ports import IOHandler, PandasDF


class ParquetHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(class_name=__class__.__name__, layer=layer, format="parquet")

    def read(self) -> PandasDF:
        self.logger.info(f"Reading Parquet file from {self.path}")
        return self.pd.read_parquet(self.path)

    def write(self, table: PandasDF) -> None:
        self.logger.info(f"Writing Parquet file to {self.path}.parquet")
        parquet_path = self.path + ".parquet"
        table.to_parquet(parquet_path, index=False)
