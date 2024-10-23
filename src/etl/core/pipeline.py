import logging

from src.etl.core.definitions import Engine, EngineType, TableName
from src.etl.io.manager import IOManager


class Pipeline:

    def __init__(
        self,
        reader: IOManager,
        engine: Engine,
        writer: IOManager,
    ):
        self.logger = logging.getLogger(__class__.__name__)
        self.reader = reader.get_handler()
        self.engine = engine
        self.writer = writer.get_handler()

    def execute(self, table_to_read: TableName = None, table_to_write: TableName = None) -> None:
        self.logger.info(f"Starting pipeline execution for {self.engine.type.value.upper()} process")

        if self.engine.type == EngineType.EXTRACTION:
            df = self.reader.read(table_name=table_to_read)
            df = self.engine.process(df)
            self.writer.write(dataframe=df, table_name=table_to_write)

        if self.engine.type == EngineType.CLEANING:
            df = self.reader.read(table_name=table_to_read)
            data_subsets = self.engine.splitter.split(dataframe=df)
            for subset in data_subsets:
                table_to_write = self.engine.splitter.get_table_name(subset)
                processed_table = self.engine.process(subset)
                self.writer.write(dataframe=processed_table, table_name=table_to_write)

        if self.engine.type == EngineType.REFINEMENT:
            pass

        self.logger.info(f"Pipeline execution for {self.engine.type.value.upper()} process finished")
