from src.etl.definitions import Writer, Table


class ParquetWriter(Writer):
    TARGET: str = "RAW"

    def __init__(self, table: Table) -> None:
        super().__init__()
        self.logger_manager.set_class_name(__class__.__name__)
        self.logger = self.logger_manager.get_logger()
        self.table = table

    def write_data(self):
        print("Writing to Parquet table")
