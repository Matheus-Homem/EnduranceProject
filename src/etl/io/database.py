from src.database.connection.builder import DatabaseExecutorBuilder
from src.database.tables import ElementEntries
from src.etl.definitions import Layer
from src.etl.ports import DatabaseDF, IOHandler
from src.shared.credentials import PRD


class DatabaseHandler(IOHandler):

    def __init__(self, layer: Layer):
        super().__init__(layer=layer, class_name=__class__.__name__)

    def read(self) -> DatabaseDF:
        if self.layer != Layer.DATABASE:
            raise ValueError("Layer not supported: DatabaseHandler only supports Layer.DATABASE")
        self.logger.info(f"Reading data from database connection")
        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            entries = executor.select(ElementEntries)
        return entries

    def write(self, table):
        raise NotImplementedError("DatabaseReader does not support write operations")


# from contextlib import contextmanager
# from typing import Generator
# import logging

# @contextmanager
# def log_operation(logger: logging.Logger, message: str) -> Generator[None, None, None]:
#     logger.info(f"Starting: {message}")
#     try:
#         yield
#     finally:
#         logger.info(f"Finished: {message}")

# def read(self) -> DatabaseDF:
#     if self.layer != Layer.DATABASE:
#         raise ValueError("Layer not supported. DatabaseHandler only supports Layer.DATABASE")

#     self.logger.info(f"Reading data from {self.path}")

#     with log_operation(self.logger, f"Reading data from {self.path}"):
#         with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
#             entries = executor.select(ElementEntries)

#     return entries
