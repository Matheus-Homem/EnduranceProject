import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import pandas

from os_local import get_absolute_path, join_paths
from src.etl.definitions import Layer

DATA_FOLDER = get_absolute_path("data")
DatabaseDF = List[Dict[str, Any]]
PandasDF = pandas.DataFrame


class IOHandler(ABC):

    def __init__(self, class_name: str, layer: Layer, format: str = None):
        self.logger = logging.getLogger(class_name)
        self.path = join_paths(DATA_FOLDER, layer.value) + f".{format}" if format else join_paths(DATA_FOLDER, layer.value)
        self.layer = layer
        self.pd = pandas

    @abstractmethod
    def read(self, path: str) -> Union[DatabaseDF, PandasDF]:
        pass

    @abstractmethod
    def write(self, table: PandasDF) -> None:
        pass


class Engine(ABC):

    def __init__(self, class_name: str):
        self.logger = logging.getLogger(class_name)
        self.pd = pandas

    @abstractmethod
    def process(self, table: Union[DatabaseDF, PandasDF]) -> PandasDF:
        pass
