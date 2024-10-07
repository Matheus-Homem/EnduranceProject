from src.etl.core.definitions import DatabaseDF, Engine, PandasDF, TableName


class ExtractionEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__, need_split=False)

    def process(self, dataframe: DatabaseDF) -> PandasDF:
        self.logger.info("Starting data processing for extraction tables")
        return self.pd.DataFrame(dataframe)

    def split(self, dataframe: PandasDF) -> PandasDF:
        NotImplementedError("ExtractionEngine does not support split operations")

    def get_table_name(self, dataframe: PandasDF) -> TableName:
        NotImplementedError("ExtractionEngine does not support get_table_name operations")
