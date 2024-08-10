from src.etl.definitions import Table
from src.etl.pipeline.execute import execute_pipeline
from src.etl.pipeline.properties import PipelineProperties
from src.etl.readers.database import DatabaseReader
from src.etl.writers.delta import DeltaWriter


class RawTable(Table):
    READER = DatabaseReader
    WRITER = DeltaWriter


class MorningTable(RawTable):
    NAME: str = "morning"

    def __init__(self):
        super().__init__()

    def generate_pipeline_properties(self) -> PipelineProperties:
        return PipelineProperties(
            reader=self.READER(table_name=self.NAME),
            writer=self.WRITER(table_name=self.NAME),
        )


class NightTable(RawTable):
    NAME: str = "night"
