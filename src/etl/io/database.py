from src.database.connection.builder import DatabaseExecutorBuilder
from src.etl.core.definitions import DatabaseDF, IOHandlerInterface, Layer, TableName
from src.shared.credentials import PRD


class DatabaseHandler(IOHandlerInterface):

    def __init__(self, layer: Layer):
        super().__init__(class_name=__class__.__name__, supported_layers=[Layer.DATABASE], layer=layer)

    def read(self, table_name: TableName) -> DatabaseDF:
        self.logger.info(f"Reading data from database connection")
        mysql_table = self.generate_path(table_name)
        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            return executor.select(mysql_table)

    def write(self, table):
        raise NotImplementedError("DatabaseReader does not support write operations")
