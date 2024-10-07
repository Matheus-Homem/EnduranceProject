from src.etl.core.definitions import IOHandler, Layer, PandasDF, TableName


class ParquetHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(class_name=__class__.__name__, supported_layers=[Layer.BRONZE], layer=layer)

    def read(self, table_name: TableName = TableName("entries")) -> PandasDF:
        path = self.generate_path(table_name=table_name)
        self.logger.info(f"Reading Parquet file from {repr(path)}")
        return self.pd.read_parquet(path)

    def write(self, dataframe: PandasDF, table_name: TableName = TableName("entries")) -> None:
        path = self.generate_path(table_name=table_name)
        self.logger.info(f"Writing Parquet file to {repr(path)}")
        dataframe.to_parquet(path, index=False)
