from typing import List

from src.etl.ports import DatabaseDF, Engine, PandasDF


class ExtractionEngine(Engine):

    def __init__(self):
        super().__init__()

    def process(self, table: DatabaseDF) -> PandasDF:
        return self.pd.DataFrame(table)
