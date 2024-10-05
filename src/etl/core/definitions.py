import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, NewType, Union

import pandas

from os_local import get_absolute_path, join_paths
from src.database.tables import (
    DailyControl,
    ElementEntries,
    ElementSchemas,
    MySqlTable,
    Users,
)
from src.etl.core.entity import EntityDTO

DATA_FOLDER = get_absolute_path("data")

TableName = NewType("TableName", str)

DatabaseDF = List[Dict[str, Any]]
PandasDF = pandas.DataFrame
DataFrameType = Union[DatabaseDF, PandasDF]


class Layer(Enum):
    DATABASE = "database"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


class IOHandler(ABC):

    def __init__(self, class_name: str, supported_layers: List[Layer], layer: Layer):
        self.logger = logging.getLogger(class_name)
        self.pd = pandas
        self.layer = layer
        self.validate_layer(class_name, supported_layers)

    @abstractmethod
    def read(self, table_name: TableName) -> DataFrameType:
        pass

    @abstractmethod
    def write(self, dataframe: DataFrameType, table_name: TableName) -> None:
        pass

    def validate_layer(self, class_name: str, supported_layers: List[Layer]) -> None:
        if self.layer not in supported_layers:
            raise ValueError(f"Layer {self.layer} is not supported by {class_name}")

    def validate_table_name(self, table_name: str) -> None:
        if not isinstance(table_name, TableName):
            raise TypeError(f"Expected table_name to be of type TableName, got {type(table_name).__name__} instead")

    def generate_path(self, table_name: TableName) -> Union[str, MySqlTable]:
        self.validate_table_name(table_name)

        if self.layer == Layer.DATABASE:
            mysql_table_mapping = {
                TableName("element_entries"): ElementEntries,
                TableName("element_schemas"): ElementSchemas,
                TableName("users"): Users,
                TableName("daily_control"): DailyControl
            }
            try:
                return mysql_table_mapping[table_name]
            except KeyError:
                raise ValueError(f"Table '{table_name}' not found in database")
        elif self.layer == Layer.BRONZE:
            return join_paths(DATA_FOLDER, self.layer.value, f"{table_name}.parquet")
        elif self.layer in [Layer.SILVER, Layer.GOLD]:
            return join_paths(DATA_FOLDER, self.layer.value, table_name)
        else:
            raise ValueError(f"Unsupported layer: {self.layer}")


class Engine(ABC):

    def __init__(self, class_name: str):
        self.logger = logging.getLogger(class_name)
        self.pd = pandas

    @abstractmethod
    def process(self, entity: EntityDTO) -> EntityDTO:
        pass
