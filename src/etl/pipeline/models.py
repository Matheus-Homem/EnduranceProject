from src.etl.definitions import BronzeTable, GoldTable, Reader, SilverTable, Writer
from src.etl.readers.database import DatabaseReader
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

    def execute(self):
        pass


class RefinerPipeline:

    def execute(self):
        pass
