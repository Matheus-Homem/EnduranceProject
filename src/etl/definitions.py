from abc import ABC, abstractmethod

from src.etl.pipeline.execute import execute_pipeline
from src.etl.pipeline.properties import PipelineProperties
from src.shared.logger import LoggingManager


class Reader(ABC):
    def __init__(self, logger_manager=LoggingManager()) -> None:
        self.logger_manager = logger_manager

    @abstractmethod
    def read(self):
        pass


class Writer(ABC):
    def __init__(self, logger_manager=LoggingManager()) -> None:
        self.logger_manager = logger_manager

    @abstractmethod
    def write(self):
        pass


class Table(ABC):
    READER: Reader
    WRITER: Writer

    def __init__(self):
        self.pipeline_properties = self.generate_pipeline_properties()

    @abstractmethod
    def generate_pipeline_properties(self) -> PipelineProperties:
        pass

    def update(self):
        execute_pipeline(pipeline_properties=self.pipeline_properties)


class SilverTable(Table):
    LAYER: str = "SILVER"


class GoldTable(Table):
    LAYER: str = "GOLD"


class ProccessingType:
    FULL = "full"
    INCREMENTAL = "incremental"
