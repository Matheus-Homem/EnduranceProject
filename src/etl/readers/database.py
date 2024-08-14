from polars import DataFrame

from src.etl.definitions import Reader
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import MySqlTable

class DatabaseReader(Reader):
    SOURCE: str = "Database"

    def __init__(self, source:MySqlTable) -> None:
        super().__init__(source=source)

    def read_data(self) -> DataFrame:
        self.logger.info(f"Starting reading process. SOURCE: {self.SOURCE} | TABLE: {self.source.__tablename__}")
        with DatabaseExecutorBuilder() as executor:
            database_table_data = executor.select(self.source)
        df = DataFrame(database_table_data)
        self.logger.info(f"Data read successfully from {self.source.__tablename__} with {df.shape[0]} records")
        return df
