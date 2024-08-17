import os
from abc import ABC, abstractmethod
from typing import Literal, NewType, Optional, Union

from polars import DataFrame

from src.shared.database.tables import MySqlTable
from src.shared.logger import LoggingManager

Path = NewType("Path", str)

Source = Union[Path, MySqlTable]


class Reader(ABC):

    def __init__(
        self,
        logger_manager=LoggingManager(),
    ) -> None:
        self.logger_manager = logger_manager
        self.logger_manager.set_class_name(self.__class__.__name__)
        self.logger = self.logger_manager.get_logger()

    @abstractmethod
    def read_dataframe(self, source: Source) -> DataFrame:
        pass


class Writer(ABC):

    def __init__(
        self,
        logger_manager=LoggingManager(),
    ) -> None:
        self.logger_manager = logger_manager
        self.logger_manager.set_class_name(self.__class__.__name__)
        self.logger = self.logger_manager.get_logger()

    @abstractmethod
    def write_dataframe(self, dataframe: DataFrame, path: Path) -> None:
        pass


class Table:

    def __init__(
        self,
        name: str,
        source: Source,
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
        source: Path,
        layer: str = "silver",
    ) -> None:
        super().__init__(name, source, layer)


class GoldTable(Table):

    def __init__(
        self,
        name: str,
        source: Path,
        layer: str = "gold",
    ) -> None:
        super().__init__(name, source, layer)
