from polars import DataFrame, col
from typing import Tuple, Literal
from src.shared.logger import LoggingManager

class CleanerTools:

    def __init__(self, logger_manager=LoggingManager()) -> None:
        logger_manager.set_class_name(self.__class__.__name__)
        self.logger = logger_manager.get_logger()

    def unnest_expanded_data(self, df: DataFrame, json_column: str) -> DataFrame:
        self.logger.info(f"Unnesting expanded data from column: {json_column}")
        df_expanded = df.with_columns(col(json_column).str.json_decode().alias("data_expanded")).unnest("data_expanded")
        return df_expanded
    
    def drop_columns(self, df: DataFrame, columns: list) -> DataFrame:
        self.logger.info(f"Dropping columns: {columns}")
        df = df.drop(columns)
        return df

    def get_datetime_cols(self, source_type: Literal["morning", "night"]) -> Tuple[str, str, str]:
        return f"date_header_{source_type}Date", f"time_header_{source_type}Time", f"datetime_header_{source_type}"
    
    def partitionate_dataframe(self, df: DataFrame, partition_cols: list) -> DataFrame:
        self.logger.info(f"Partitionating dataframe by columns: {partition_cols}")
        df = df.partition_by(partition_cols)
        return df