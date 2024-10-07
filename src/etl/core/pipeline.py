import logging

from src.etl.core.definitions import Engine, IOHandler


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

    def execute(self) -> None:
        data = self.reader.read()
        processed_table = self.engine.process(data)
        self.writer.write(dataframe=processed_table)
