import logging

from src.etl.core.definitions import DataFrameType, Engine, TableName
from src.etl.io.manager import IOManager


class Pipeline:

    def __init__(
        self,
        reader: IOManager,
        engine: Engine,
        writer: IOManager,
    ):
        self.logger = logging.getLogger(__class__.__name__)
        self.reader = reader
        self.engine = engine
        self.writer = writer
        self._set_pipeline_type(engine.__class__.__name__)

    def _set_pipeline_type(self, engine_class_name: str) -> str:
        self.pipeline_type = engine_class_name.replace("Engine", "").upper()

    def _proccess_and_save(self, dataframe: DataFrameType, table_to_write: TableName) -> None:
        processed_table = self.engine.process(dataframe)
        self.writer.write(dataframe=processed_table, table_name=table_to_write)

    def _split_process_and_save(self, dataframe: DataFrameType) -> None:
        data_subsets = self.engine.splitter.split(dataframe=dataframe)
        for subset in data_subsets:
            table_to_write = self.engine.splitter.get_table_name(subset)
            processed_table = self.engine.process(subset)
            self.writer.write(dataframe=processed_table, table_name=table_to_write)

    def execute(self, table_to_read: TableName = None, table_to_write: TableName = None) -> None:
        self.logger.info(f"Starting pipeline execution for {self.pipeline_type} layer")

        data = self.reader.read(table_name=table_to_read)

        if self.engine.should_split_data():
            self._split_process_and_save(data)
        else:
            self._proccess_and_save(data, table_to_write)

        self.logger.info(f"Pipeline execution for {self.pipeline_type} layer finished")
