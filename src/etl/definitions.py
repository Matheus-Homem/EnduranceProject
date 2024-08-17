import os
from abc import ABC, abstractmethod
from typing import NewType, Optional, Union

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
    name: str
    source: Source
    layer: str
    folder: str = "data"
    format: Optional[str] = None

    @property
    def path(self) -> Path:
        suffix = f".{self.format}" if self.format else ""
        return Path(os.path.join(self.folder, self.layer, self.name) + suffix)
