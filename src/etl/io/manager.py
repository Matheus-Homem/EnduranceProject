from src.etl.core.definitions import (
    DataFrameType,
    Format,
    IOHandler,
    Layer,
    TableName,
)
from src.etl.io.database import DatabaseHandler
from src.etl.io.delta import DeltaHandler
from src.etl.io.parquet import ParquetHandler


class IOHandlerFactory:

    @staticmethod
    def get_handler(layer: Layer, format: Format) -> IOHandler:

        if format == Format.JDBC:
            return DatabaseHandler(layer=layer)

        if format == Format.PARQUET:
            return ParquetHandler(layer=layer)

        if format == Format.DELTA:
            return DeltaHandler(layer=layer)

        else:
            raise ValueError(f"Unsupported format: {format}")


class IOManager:

    def __init__(
        self,
        layer: Layer,
        format: Format,
    ):
        self.handler = IOHandlerFactory.get_handler(layer, format)

    def read(self, table_name: TableName) -> DataFrameType:
        return self.handler.read(table_name=table_name)

    def write(self, dataframe: DataFrameType, table_name: TableName) -> None:
        self.handler.write(dataframe=dataframe, table_name=table_name)
