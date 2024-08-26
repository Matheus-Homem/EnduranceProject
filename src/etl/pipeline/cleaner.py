from src.etl.definitions import Pipeline, SilverTable
from src.etl.engines.cleaner.fomatter import CleanerFormatter
from src.etl.engines.cleaner.tools import CleanerTools
from src.etl.readers.parquet import ParquetReader
from src.etl.writers.parquet import ParquetWriter


class CleanerPipeline(Pipeline):

    def __init__(self) -> None:
        super().__init__(class_name=self.__class__.__name__)

    def execute(
        self,
        table: SilverTable,
        reader=ParquetReader(),
        writer=ParquetWriter(),
        formatter=CleanerFormatter(),
        tools=CleanerTools(),
    ) -> None:
        self.logger.info(f"Cleaning data for table {table.name}")
        date_col, time_col, datetime_col = tools.get_datetime_cols(table.source.name.split("_")[0])
        dataframe = reader.read_dataframe(source=table.source.get_path())
        dataframe_unnested = tools.unnest_expanded_data(dataframe, json_column="data")
        dataframe_formatted = formatter.format_dataframe_columns(
            dataframe_unnested, default_date_col=date_col, default_time_col=time_col, new_datetime_col=datetime_col
        )
        dataframe_cleaned = tools.drop_columns(dataframe_formatted, columns=[date_col, time_col, "data"])
        writer.write_dataframe(dataframe=dataframe_cleaned, path=table.get_path())
