from polars import DataFrame

from src.etl.definitions import Reader
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import MySqlTable


class DatabaseReader(Reader):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def read_dataframe(self, source: MySqlTable) -> DataFrame:
        self.logger.info(f"Reading table {source.__tablename__} from Database")
        with DatabaseExecutorBuilder() as executor:
            database_table_data = executor.select(source)
        df = DataFrame(database_table_data)
        return df
