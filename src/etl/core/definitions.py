import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, NewType, Optional, Union

import pandas

from os_local import get_absolute_path, join_paths
from src.database.tables import (
    DailyControl,
    ElementEntries,
    ElementSchemas,
    MySqlTable,
    Users,
)

DATA_FOLDER = get_absolute_path("data")

TableName = NewType("TableName", str)

DatabaseDF = List[Dict[str, Any]]
PandasDF = pandas.DataFrame
DataFrameType = Union[DatabaseDF, PandasDF]


class DataType(Enum):
    BOOL = "bool"
    DATE = "date"
    DOUBLE = "double"
    DURATION_HHMMSS = "hhmmss"
    DURATION_HHMM = "hhmm"
    INTEGER = "int"
    ORDINAL = "ordinal"
    STRING = "string"
    TIMESTAMP = "timestamp"


class Layer(Enum):
    DATABASE = "database"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


class Format(Enum):
    JDBC = "jdbc"
    PARQUET = "parquet"
    DELTA = "delta"


class IOHandlerInterface(ABC):

    def __init__(
        self,
        class_name: str,
        layer: Layer,
        supported_layers: List[Layer],
    ):
        self.logger = logging.getLogger(class_name)
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

    def generate_path(self, table_name: TableName) -> Union[str, MySqlTable]:
        if self.layer == Layer.DATABASE:
            mysql_table_mapping = {
                TableName("element_entries"): ElementEntries,
                TableName("element_schemas"): ElementSchemas,
                TableName("users"): Users,
                TableName("daily_control"): DailyControl,
            }
            try:
                return mysql_table_mapping[table_name]
            except KeyError:
                raise ValueError(f"Table '{table_name}' is not a MySQL Database valid table")
        elif self.layer == Layer.BRONZE:
            return join_paths(DATA_FOLDER, self.layer.value, f"{table_name}.parquet")
        elif self.layer in [Layer.SILVER, Layer.GOLD]:
            return join_paths(DATA_FOLDER, self.layer.value, table_name)
        else:
            raise ValueError(f"Unsupported layer: {self.layer}")


class CastingStrategy(ABC):
    @abstractmethod
    def cast(self, col: PandasDF, pandas: pandas = None) -> PandasDF:
        pass


class Splitter(ABC):

    def __init__(
        self,
        class_name: str,
        column_to_split: str,
    ):
        self.logger = logging.getLogger(class_name)
        self.column_to_split = column_to_split

    @abstractmethod
    def split(self, dataframe: DataFrameType) -> List[DataFrameType]:
        pass

    @abstractmethod
    def get_table_name(self, dataframe: DataFrameType) -> TableName:
        pass


class Tool(ABC):

    def __init__(self) -> None:
        self.pd = pandas

    @abstractmethod
    def apply(self, dataframe: DataFrameType) -> DataFrameType:
        pass


class Engine(ABC):

    def __init__(
        self,
        class_name: str,
        tool: Optional[Tool] = None,
        splitter: Optional[Splitter] = None,
    ):
        self.logger = logging.getLogger(class_name)
        self.pd = pandas
        self.tool = tool
        self.splitter = splitter

        self._need_split = True if splitter else False

    def should_split_data(self) -> bool:
        return self._need_split

    @abstractmethod
    def process(self, dataframe: DataFrameType) -> DataFrameType:
        pass
