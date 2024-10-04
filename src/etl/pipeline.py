import logging

from src.etl.ports import Engine, IOHandler


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
        self.logger.info(f"Starting {self.pipeline_type } pipeline execution")
        table = self.reader.read()
        processed_table = self.engine.process(table=table)
        self.writer.write(table=processed_table)
