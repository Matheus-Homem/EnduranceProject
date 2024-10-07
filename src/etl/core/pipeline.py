import logging

from src.etl.core.definitions import Engine, IOHandler, TableName


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

        if self.engine.need_split():
            self._process_and_write_subsets(data, table_to_write)
        else:
            self._process_and_write(data, table_to_write)

    def _process_and_write(self, data, table_to_write: TableName) -> None:
        processed_table = self.engine.process(data)
        self.writer.write(dataframe=processed_table, table_name=table_to_write)

    def _process_and_write_subsets(self, data, table_to_write: TableName) -> None:
        data_subsets = self.engine.split(data)
        for subset in data_subsets:
            table_to_write = self.engine.get_table_name(subset)
            self._process_and_write(subset, table_to_write)
