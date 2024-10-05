from typing import Any, Dict, List, Union

from pandas import DataFrame

from src.etl.core.definitions import Layer

DatabaseDF = List[Dict[str, Any]]
PandasDF = DataFrame


class EntityDTO:

    def __init__(
        self,
        name: str,
        data: Union[DatabaseDF, PandasDF] = None,
    ):
        self.name = name
        self.format = format
        self.pipeline = pipeline
        self.path = path
        self.layer = layer
        self.data = data

    def set_name(self, name) -> None:
        self.name = name

    def set_format(self, format) -> None:
        self.format = format

    def set_pipeline(self, pipeline) -> None:
        self.pipeline = pipeline

    def set_path(self, path) -> None:
        self.path = path

    def set_layer(self, layer: Layer) -> None:
        self.layer = layer

    def set_data(self, data) -> None:
        self.data = data
