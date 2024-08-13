from abc import ABC, abstractmethod

from src.shared.logger import LoggingManager


class Reader(ABC):
    def __init__(self, logger_manager=LoggingManager()) -> None:
        self.logger_manager = logger_manager

    @abstractmethod
    def read_data(self):
        pass


class Writer(ABC):
    def __init__(self, logger_manager=LoggingManager()) -> None:
        self.logger_manager = logger_manager

    @abstractmethod
    def write_data(self):
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

class Table(ABC):
    READER: Reader
    WRITER: Writer

    def __init__(self):
        self.pipeline_properties = self.generate_pipeline_properties()

    @abstractmethod
    def generate_pipeline_properties(self) -> PipelineDefinition:
        pass

    def update(self):
        pass
        # execute_pipeline(pipeline_properties=self.pipeline_properties)


class SilverTable(Table):
    LAYER: str = "SILVER"


class GoldTable(Table):
    LAYER: str = "GOLD"