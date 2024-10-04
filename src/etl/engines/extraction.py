from src.etl.ports import DatabaseDF, Engine, PandasDF


class ExtractionEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__)

    def process(self, table: DatabaseDF) -> PandasDF:
        self.logger.info("Starting data processing for extraction tables")
        return self.pd.DataFrame([table])
