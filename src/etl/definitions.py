import os
from abc import ABC, abstractmethod
from typing import Literal, NewType, Optional, Union

from polars import DataFrame

from src.shared.database.tables import MySqlTable
from src.shared.logging.printer import LoggingPrinter

Path = NewType("Path", str)


class Reader(ABC, LoggingPrinter):

    @abstractmethod
    def read_dataframe(self, source: Union[MySqlTable, "Table"]) -> DataFrame: ...


class Writer(ABC, LoggingPrinter):

    @abstractmethod
    def write_dataframe(self, dataframe: DataFrame, path: Path) -> None: ...


class Table:

    def __init__(
        self,
        name: str,
        source: Union[MySqlTable, "Table"],
        layer: Literal["bronze", "silver", "gold"],
        folder: str = "data",
        format: Optional[str] = None,
    ) -> None:
        self.name = name
        self.source = source
        self.layer = layer
        self.folder = folder
        self.format = format

    def get_path(self) -> Path:
        suffix = f".{self.format}" if self.format else ""
        return Path(os.path.join(self.folder, self.layer, self.name) + suffix)


class BronzeTable(Table):

    def __init__(
        self,
        name: str,
        source: MySqlTable,
        layer: str = "bronze",
        format: str = "parquet",
    ) -> None:
        super().__init__(name, source, layer, format=format)


class SilverTable(Table):

    def __init__(
        self,
        name: str,
        source: BronzeTable,
        layer: str = "silver",
        format: str = "parquet",
    ) -> None:
        super().__init__(name, source, layer, format=format)


class GoldTable(Table):

    def __init__(
        self,
        name: str,
        source: SilverTable,
        layer: str = "gold",
    ) -> None:
        super().__init__(name, source, layer)


class Pipeline(ABC, LoggingPrinter):

    @abstractmethod
    def execute(table: Table, reader: Reader, writer: Writer) -> None: ...


class Engine(ABC, LoggingPrinter):

    def __init__(self, class_name: str) -> None:
        super().__init__(class_name=class_name)