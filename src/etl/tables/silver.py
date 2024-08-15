from src.etl.definitions import PipelineDefinition, Table
from src.etl.readers.parquet import ParquetReader
from src.etl.tables.bronze import BronzeTable, MorningTable, NightTable
from src.etl.writers.delta import DeltaWriter



class SilverTable(Table):
    LAYER: str = "silver"
    FORMAT: str = None
    READER = ParquetReader
    WRITER = DeltaWriter
    SOURCE: BronzeTable


class NavigatorTable(SilverTable):
    SOURCE = NightTable
    TARGET: str = "navigator"

    def __init__(self):
        super().__init__()

    def generate_pipeline_properties(self) -> PipelineDefinition:
        return PipelineDefinition(
            reader=self.READER(source=self.SOURCE().get_path()),
            writer=self.WRITER(path=self.get_path()),
        )