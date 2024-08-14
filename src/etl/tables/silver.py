from src.etl.definitions import PipelineDefinition, Table
from src.etl.readers.parquet import ParquetReader
from src.etl.tables.bronze import BronzeTable
from src.etl.writers.delta import DeltaWriter


class SilverTable(Table):
    LAYER: str = "silver"
    READER = ParquetReader
    WRITER = DeltaWriter
    SOURCE_TABLE: BronzeTable
