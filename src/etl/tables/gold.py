from src.etl.definitions import PipelineDefinition, Table
from src.etl.readers.parquet import ParquetReader
from src.etl.writers.delta import DeltaWriter


class GoldTable(Table):
    LAYER: str = "gold"
    READER = ParquetReader
    WRITER = DeltaWriter
    SOURCE: Table
