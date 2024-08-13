import polars as pl

from src.etl.definitions import Reader
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import MySqlTable

class DatabaseReader(Reader):
    SOURCE: str = "DATABASE"

    def __init__(self, table: MySqlTable) -> None:
        super().__init__()
        self.logger_manager.set_class_name(__class__.__name__)
        self.logger = self.logger_manager.get_logger()
        self.table = table

    def read_data(self) -> pl.DataFrame:
        self.logger.info(f"Starting reading process. Source: {self.SOURCE} | Table: {self.table.__tablename__}")
        with DatabaseExecutorBuilder() as executor:
            database_table_data = executor.select(self.table)
        df = pl.DataFrame(database_table_data)
        self.logger.info(f"Data read successfully from {self.table.__tablename__} with {df.shape[0]} records")
        return df
