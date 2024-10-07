import logging

from src.etl.core.definitions import DataFrameType, Engine, IOHandler, TableName


class Pipeline:

    def __init__(
        self,
        reader: IOHandler,
        engine: Engine,
        writer: IOHandler,
    ):
        self.logger = logging.getLogger(__class__.__name__)
        self.reader = reader
        self.engine = engine
        self.writer = writer
        self.pipeline_type = self.engine.__class__.__name__.replace("Engine", "").upper()

    def execute(self, table_to_read: TableName = None, table_to_write: TableName = None) -> None:
        data = self.reader.read(table_name=table_to_read)

        if self.engine.should_split_data():
            self._split_and_write_data_subsets(data)
        else:
            self._process_and_write(data, table_to_write)

    def _process_and_write(self, dataframe: DataFrameType, table_to_write: TableName) -> None:
        processed_table = self.engine.process(dataframe)
        self.writer.write(dataframe=processed_table, table_name=table_to_write)

    def _split_and_write_data_subsets(self, data: DataFrameType) -> None:
        data_subsets = self.engine.split(data)
        for subset in data_subsets:
            table_name = self.engine.get_table_name(subset)
            self._process_and_write(dataframe=subset, table_to_write=table_name)
