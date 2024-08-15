from src.etl.definitions import PipelineDefinition, Table
from src.etl.readers.database import DatabaseReader
from src.etl.writers.parquet import ParquetWriter
from src.shared.database.tables import MySqlMorningTable, MySqlNightTable, MySqlTable


class BronzeTable(Table):
    LAYER: str = "bronze"
    FORMAT: str = "parquet"
    READER = DatabaseReader
    WRITER = ParquetWriter
    SOURCE: MySqlTable


class MorningTable(BronzeTable):
    SOURCE = MySqlMorningTable
    TARGET: str = "morning_raw"

    def __init__(self):
        super().__init__()

    def generate_pipeline_properties(self) -> PipelineDefinition:
        return PipelineDefinition(
            reader=self.READER(source=self.SOURCE),
            writer=self.WRITER(path=self.get_path()),
        )


class NightTable(BronzeTable):
    SOURCE = MySqlNightTable
    TARGET: str = "night_raw"

    def __init__(self):
        super().__init__()

    def generate_pipeline_properties(self) -> PipelineDefinition:
        return PipelineDefinition(
            reader=self.READER(source=self.SOURCE),
            writer=self.WRITER(path=self.get_path()),
        )
