from src.etl.definitions import BronzeTable, GoldTable, Pipeline, SilverTable
from src.etl.readers.database import DatabaseReader
from src.etl.readers.delta import DeltaReader
from src.etl.readers.parquet import ParquetReader
from src.etl.writers.delta import DeltaWriter
from src.etl.writers.parquet import ParquetWriter


class ExtractorPipeline(Pipeline):

    @staticmethod
    def execute(
        table: BronzeTable,
        reader=DatabaseReader(),
        writer=ParquetWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source)
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())


class CleanerPipeline(Pipeline):

    @staticmethod
    def execute(
        table: SilverTable,
        reader=ParquetReader(),
        writer=DeltaWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source.get_path())
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())


class RefinerPipeline(Pipeline):

    @staticmethod
    def execute(
        table: GoldTable,
        reader=DeltaReader(),
        writer=DeltaWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source.get_path())
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())
