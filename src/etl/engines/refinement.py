from src.etl.ports import Engine, PandasDF


class RefinementEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__)

    def process(self, table: PandasDF) -> PandasDF:
        self.logger.info("Starting data refinement process")
        return table
