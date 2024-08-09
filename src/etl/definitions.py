from abc import ABC, abstractmethod

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


class ProccessingType:
    FULL = "full"
    INCREMENTAL = "incremental"
