from typing import Any, Dict, List

from pandas import DataFrame

from src.etl.ports import Engine


class ExtractionEngine(Engine):

    def __init__(self):
        super().__init__()

    def process(self, table: List[Dict[str, Any]]) -> DataFrame:
        return self.pd.DataFrame(table)
