from src.etl.definitions import BronzeTable, GoldTable, Reader, SilverTable, Writer
from src.etl.readers.database import DatabaseReader
from src.etl.readers.delta import DeltaReader
from src.etl.readers.parquet import ParquetReader
from src.etl.writers.delta import DeltaWriter
from src.etl.writers.parquet import ParquetWriter


class ExtractorPipeline:

    @staticmethod
    def execute(
        table: BronzeTable,
        reader: Reader = DatabaseReader(),
        writer: Writer = ParquetWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source)
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())


class CleanerPipeline:

    @staticmethod
    def execute(
        table: SilverTable,
        reader: Reader = ParquetReader(),
        writer: Writer = DeltaWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source.get_path())
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())


class RefinerPipeline:

    @staticmethod
    def execute(
        table: GoldTable,
        reader: Reader = DeltaReader(),
        writer: Writer = DeltaWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source.get_path())
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())
