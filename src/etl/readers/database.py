from polars import DataFrame

from src.database.connection.builder import DatabaseExecutorBuilder
from src.database.tables import MySqlTable
from src.etl.definitions import Reader


class DatabaseReader(Reader):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def read_dataframe(self, source: MySqlTable) -> DataFrame:
        self.logger.info(f"Reading table {source.__tablename__} from Database")
        with DatabaseExecutorBuilder() as executor:
            database_table_data = executor.select(source)
        df = DataFrame(database_table_data)
        return df
