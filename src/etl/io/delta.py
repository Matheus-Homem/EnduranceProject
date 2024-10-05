from deltalake import DeltaTable, write_deltalake

from src.etl.core.definitions import IOHandler, Layer, PandasDF, TableName


class DeltaHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(class_name=__class__.__name__, supported_layers=[Layer.SILVER, Layer.GOLD], layer=layer)

    def read(self, table_name: TableName) -> PandasDF:
        path = self.generate_path(table_name=table_name)
        self.logger.info(f"Reading Delta Lake file from {path}")
        return DeltaTable(path).to_pandas()

    def write(self, table: PandasDF, table_name: TableName) -> None:
        path = self.generate_path(table_name=table_name)
        self.logger.info(f"Writing Delta Lake file to {path}")
        write_deltalake(path, table, mode="overwrite", schema_mode="overwrite")
