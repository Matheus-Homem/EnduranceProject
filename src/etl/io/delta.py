from deltalake import DeltaTable, write_deltalake

from src.etl.definitions import Layer
from src.etl.ports import IOHandler, PandasDF


class DeltaHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(layer=layer, class_name=__class__.__name__)

    def read(self) -> PandasDF:
        self.logger.info(f"Reading Delta Lake file from {self.path}")
        return DeltaTable(self.path).to_pandas()

    def write(self, table: PandasDF) -> None:
        self.logger.info(f"Writing Delta Lake file to {self.path}")
        write_deltalake(self.path, table, mode="overwrite", schema_mode="overwrite")
