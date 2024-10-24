from typing import List

from deltalake import DeltaTable, write_deltalake

from os_local import list_directory_contents, extract_basename
from src.etl.core.definitions import IOHandler, Layer, PandasDF, TableName


class DeltaHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(class_name=__class__.__name__, supported_layers=[Layer.SILVER, Layer.GOLD], layer=layer)

    def read(self, table_name: TableName) -> PandasDF:
        path = self.generate_path(table_name=table_name)
        return DeltaTable(path).to_pandas()

    def write(self, dataframe: PandasDF, table_name: TableName) -> None:
        path = self.generate_path(table_name=table_name)
        self.logger.info(f"Writing Delta Lake file to {repr(path)}")
        write_deltalake(path, dataframe, mode="overwrite", schema_mode="overwrite")

    def _is_delta_table(self, path: str) -> bool:
        try:
            DeltaTable(path)
            return True
        except:
            return False

    def list_delta_tables(self) -> List[str]:
        base_path = self.generate_path(table_name="")
        delta_tables = [
            extract_basename(root) for root, dirs, files in list_directory_contents(base_path) if "_delta_log" in dirs and self._is_delta_table(root)
        ]
        return delta_tables
