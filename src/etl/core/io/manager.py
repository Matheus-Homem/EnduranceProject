from src.etl.core.definitions import Format, IOHandler, Layer
from src.etl.core.io.database import DatabaseHandler
from src.etl.core.io.delta import DeltaHandler
from src.etl.core.io.parquet import ParquetHandler


class IOManager:

    def __init__(
        self,
        layer: Layer,
        format: Format,
    ):
        self.layer = layer
        self.format = format

    def get_handler(self) -> IOHandler:

        if self.format == Format.JDBC:
            return DatabaseHandler(layer=self.layer)

        if self.format == Format.PARQUET:
            return ParquetHandler(layer=self.layer)

        if self.format == Format.DELTA:
            return DeltaHandler(layer=self.layer)

        else:
            raise ValueError(f"Unsupported format: {self.format}")
