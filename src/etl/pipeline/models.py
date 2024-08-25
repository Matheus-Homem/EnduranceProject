from src.etl.definitions import BronzeTable, GoldTable, Pipeline, SilverTable
from src.etl.engines.cleaner.fomatter import CleanerFormatter
from src.etl.engines.cleaner.tools import CleanerTools
from src.etl.readers.database import DatabaseReader
from src.etl.readers.delta import DeltaReader
from src.etl.readers.parquet import ParquetReader
from src.etl.writers.delta import DeltaWriter
from src.etl.writers.parquet import ParquetWriter
import logging


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
        writer=ParquetWriter(),
        formatter=CleanerFormatter(),
        tools=CleanerTools(),
    ) -> None:
        date_col, time_col, datetime_col = tools.get_datetime_cols(table.source.name.split("_")[0])
        dataframe = reader.read_dataframe(source=table.source.get_path())
        dataframe_unnested = tools.unnest_expanded_data(dataframe, json_column="data")
        dataframe_formatted = formatter.format_dataframe_columns(dataframe_unnested, default_date_col=date_col, default_time_col=time_col, new_datetime_col=datetime_col)
        dataframe_cleaned = tools.drop_columns(dataframe_formatted, columns=[date_col, time_col, "data"])
        writer.write_dataframe(dataframe=dataframe_cleaned, path=table.get_path())

class RefinerPipeline(Pipeline):

    @staticmethod
    def execute(
        table: GoldTable,
        reader=DeltaReader(),
        writer=DeltaWriter(),
    ) -> None:
        dataframe = reader.read_dataframe(source=table.source.get_path())
        writer.write_dataframe(dataframe=dataframe, path=table.get_path())
