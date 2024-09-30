from src.etl.ports import Engine, PandasDF


class CleaningEngine(Engine):

    def __init__(self):
        super().__init__()

    def process(self, table: PandasDF) -> PandasDF:
        pass
