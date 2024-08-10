import polars as pl

from src.etl.definitions import Reader
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import MySqlTable


class DatabaseReader(Reader):

    def __init__(self, table: MySqlTable) -> None:
        super().__init__()
        self.logger_manager.set_class_name(__class__.__name__)
        self.logger = self.logger_manager.get_logger()
        self.table = table

    def read(self) -> pl.DataFrame:
        with DatabaseExecutorBuilder() as executor:
            database_table_data = executor.select(self.table)
        df = pl.DataFrame(database_table_data)
        self.logger.info("Data read successfully")
        return df
