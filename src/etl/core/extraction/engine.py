from src.etl.core.definitions import DatabaseDF, Engine, EngineType, PandasDF


class ExtractionEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__, type=EngineType.EXTRACTION)

    def process(self, dataframe: DatabaseDF) -> PandasDF:
        self.logger.info("Starting data processing for extraction tables")
        return self._pd.DataFrame(dataframe)
