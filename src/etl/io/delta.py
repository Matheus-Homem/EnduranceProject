from deltalake import DeltaTable, write_deltalake

from src.etl.definitions import Layer
from src.etl.ports import IOHandler, PandasDF


class DeltaHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(layer)

    def read(self) -> PandasDF:
        return DeltaTable(self.path).to_pandas()

    def write(self, table: PandasDF) -> None:
        write_deltalake(self.path, table, mode="overwrite")
