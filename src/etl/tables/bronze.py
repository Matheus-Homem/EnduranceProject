from src.etl.definitions import Table, PipelineDefinition
from src.etl.readers.database import DatabaseReader
from src.etl.writers.parquet import ParquetWriter
from src.shared.database.tables import MySqlTable, MySqlMorningTable



class RawTable(Table):
    READER = DatabaseReader
    WRITER = ParquetWriter
    SOURCE_TABLE: MySqlTable
    TARGET_TABLE: Table


class MorningTable(RawTable):
    SOURCE_TABLE = MySqlMorningTable
    # TARGET_TABLE: str = "morning_raw"

    def __init__(self):
        super().__init__()

    def generate_pipeline_properties(self) -> PipelineDefinition:
        return PipelineDefinition(
            reader=self.READER(table=self.SOURCE_TABLE),
            writer=self.WRITER(table=RawTable),
        )


class NightTable(RawTable):
    NAME: str = "night"
