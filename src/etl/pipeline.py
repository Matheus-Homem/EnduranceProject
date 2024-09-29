from src.etl.ports import Engine, IOHandler


class Pipeline:

    def __init__(
        self,
        reader: IOHandler,
        engine: Engine,
        writer: IOHandler,
    ):
        self.reader = reader
        self.engine = engine
        self.writer = writer

    def execute(self) -> None:
        for table in self.reader.read():
            processed_table = self.engine.process(table=table)
            self.writer.write(table=processed_table)
