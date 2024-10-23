import logging

from src.etl.core.definitions import Engine, EngineType, TableName
from src.etl.engines.tools.utils import get_subset_table_name, split_dataframe
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
        self.column_separator = "element_name"

    def __extract(self, table_to_read: TableName, table_to_write: TableName) -> None:
        df = self.reader.read(table_name=table_to_read)
        df = self.engine.process(df)
        self.writer.write(dataframe=df, table_name=table_to_write)

    def __clean(self, table_to_read: TableName) -> None:
        df = self.reader.read(table_name=table_to_read)
        data_subsets = split_dataframe(dataframe=df, column_to_split=self.column_separator)
        for subset in data_subsets:
            subset_table_name = get_subset_table_name(dataframe=subset, subset_col_id=self.column_separator)
            processed_table = self.engine.process(subset)
            self.writer.write(dataframe=processed_table, table_name=subset_table_name)

    def execute(self, table_to_read: TableName = None, table_to_write: TableName = None) -> None:
        self.logger.info(f"Starting pipeline execution for {self.engine.type.value.upper()} process")

        if self.engine.type == EngineType.EXTRACTION:
            self.__extract(table_to_read=table_to_read, table_to_write=table_to_write)

        if self.engine.type == EngineType.CLEANING:
            self.__clean(table_to_read=table_to_read)

        if self.engine.type == EngineType.REFINEMENT:
            list_of_tables = self.engine.tool.apply()
            for table in list_of_tables:
                table_name = table.split("/")[0]
                df = self.reader.read(table_name=table_name)
                df = self.engine.process(df)
                self.writer.write(dataframe=df, table_name=table_name)

        self.logger.info(f"Pipeline execution for {self.engine.type.value.upper()} process finished")
