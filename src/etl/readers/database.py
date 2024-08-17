from polars import DataFrame

from src.etl.definitions import Reader
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import MySqlTable


class DatabaseReader(Reader):

    def __init__(self) -> None:
        super().__init__()

    def read_dataframe(self, source: MySqlTable) -> DataFrame:
        self.logger.info(f"Starting reading process. SOURCE: Database | TABLE: {source.__tablename__}")
        with DatabaseExecutorBuilder() as executor:
            database_table_data = executor.select(source)
        df = DataFrame(database_table_data)
        self.logger.info(f"Data read successfully from {source.__tablename__} with {df.shape[0]} records")
        return df
