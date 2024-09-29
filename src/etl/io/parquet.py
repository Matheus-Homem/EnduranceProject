from src.etl.definitions import Layer
from src.etl.ports import IOHandler, PandasDF


class ParquetHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(layer)

    def read(self) -> PandasDF:
        return self.pd.read_parquet(self.path)

    def write(self, table: PandasDF) -> None:
        table.to_parquet(self.path, index=False)
