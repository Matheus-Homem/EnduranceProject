from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import pandas

from os_local import get_absolute_path, join_paths
from src.etl.definitions import Layer

Dataset = Union[pandas.DataFrame, List[Dict[str, Any]]]
DATA_FOLDER = get_absolute_path("data")


class IOHandler(ABC):

    def __init__(self, layer: Layer):
        self.path = join_paths(DATA_FOLDER, layer.value)
        self.pd = pandas

    @abstractmethod
    def read(self, path: str) -> Dataset:
        pass

    @abstractmethod
    def write(self, table: Dataset) -> None:
        pass


class Engine(ABC):

    def __init__(self):
        self.pd = pandas

    @abstractmethod
    def process(self, table: Dataset) -> None: ...
