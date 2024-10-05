import logging

from src.etl.core.definitions import Engine, IOHandler
from src.etl.core.entity import EntityDTO


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
        # self.entity_dto = None

    # def _validate_entity(self) -> None:
    #     if not self.entity:
    #         raise ValueError("Entity not set. Please set the entity before executing the pipeline")

    def execute(self) -> None:
        entity = EntityDTO()
        data = self.reader.read()

        processed_table = self.engine.process(data)

        self.writer.write(data=processed_table)
