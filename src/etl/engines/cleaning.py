from src.etl.core.definitions import Engine, PandasDF


class CleaningEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__)

    def process(self, table: PandasDF) -> PandasDF:
        self.logger.info("Starting data cleaning process")
        return table
