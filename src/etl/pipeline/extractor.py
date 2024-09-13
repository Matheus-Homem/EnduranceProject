from src.etl.definitions import BronzeTable, Pipeline
from src.etl.readers.database import DatabaseReader
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
