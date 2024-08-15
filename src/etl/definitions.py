import os
from abc import ABC, abstractmethod
from typing import Union, NewType

from src.shared.database.tables import MySqlTable
from src.shared.logger import LoggingManager

Path = NewType('Path', str)

class Reader(ABC):
    def __init__(
        self,
        source: Union[Path, MySqlTable],
        logger_manager=LoggingManager(),
    ) -> None:
        self.source = source
        self.logger_manager = logger_manager
        self.logger_manager.set_class_name(self.__class__.__name__)
        self.logger = self.logger_manager.get_logger()

    @abstractmethod
    def read_data(self):
        pass


class Writer(ABC):

    def __init__(
        self,
        path: Path,
        logger_manager=LoggingManager(),
    ) -> None:
        self.path = path
        self.logger_manager = logger_manager
        self.logger_manager.set_class_name(self.__class__.__name__)
        self.logger = self.logger_manager.get_logger()

    @abstractmethod
    def write_data(self, dataframe):
        pass


class PipelineDefinition:

    def __init__(
        self,
        reader: Reader,
        writer: Writer,
    ) -> None:
        self.reader = reader
        self.writer = writer

    def get_reader(self) -> Reader:
        return self.reader

    def get_writer(self) -> Writer:
        return self.writer

    def print(self):
        print(
            f"""
        Pipeline Definition:
        Reader: {type(self.reader).__name__}
        Writer: {type(self.writer).__name__}
        Source: {str(self.reader.source).split('.')[-1][:-2]}
        Target: {self.writer.path}
        """
        )


class Table(ABC):
    FOLDER: str = "data"
    LAYER: str
    TARGET: str
    FORMAT: str
    SOURCE: Union["Table", MySqlTable]
    READER: Reader
    WRITER: Writer

    def __init__(self):
        self.pipeline_properties = self.generate_pipeline_properties()

    @abstractmethod
    def generate_pipeline_properties(self) -> PipelineDefinition:
        pass

    def get_path(self) -> Path:
        suffix = f".{self.FORMAT}" if self.FORMAT else ""
        return Path(os.path.join(self.FOLDER, self.LAYER, self.TARGET) + suffix)