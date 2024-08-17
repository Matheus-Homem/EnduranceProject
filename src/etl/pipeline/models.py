from src.etl.definitions import Reader, Writer
from src.etl.readers.database import DatabaseReader
from src.etl.tables.bronze import BronzeTable
from src.etl.writers.parquet import ParquetWriter


class ExtractorPipeline:

    @staticmethod
    def execute(
        table: BronzeTable,
        reader: Reader = DatabaseReader(),
        writer: Writer = ParquetWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source)
        writer.write_dataframe(dataframe=dataframe, path=table.path)


class CleanerPipeline:

    def execute(self):
        pass


class RefinerPipeline:

    def execute(self):
        pass
