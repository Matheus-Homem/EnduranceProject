from src.database.connection.builder import DatabaseExecutorBuilder
from src.database.tables import ElementEntries
from src.etl.definitions import Layer
from src.etl.ports import DatabaseDF, IOHandler
from src.shared.credentials import PRD


class DatabaseReader(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(layer)

    def read(self) -> DatabaseDF:
        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            entries = executor.select(ElementEntries)
        return entries

    def write(self, table):
        raise NotImplementedError("DatabaseReader does not support write operations")
