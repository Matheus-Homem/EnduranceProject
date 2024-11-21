import logging

from src.etl.core.definitions import (
    Engine,
    EngineType,
    Format,
    RefinementType,
    TableName,
)
from src.etl.core.io.delta import DeltaHandler
from src.etl.core.io.manager import IOManager
from src.etl.core.refinement.engine import RefinementEngine
from src.etl.core.utils import PipelineUtils


class Pipeline:

    def __init__(
        self,
        reader: IOManager,
        engine: Engine,
        writer: IOManager,
    ):
        self.logger = logging.getLogger(__class__.__name__)
        self.reader_format = reader.format
        self.reader = reader.get_handler()
        self.engine = engine
        self.writer = writer.get_handler()
        self.column_separator = "element_name"
        self.extraction_date_column = "entry_date"
        self.parquet_partition_cols = ["year", "month", "day"]

    def _extract(self, table_to_read: TableName, table_to_write: TableName) -> None:
        df = self.reader.read(table_name=table_to_read)
        self.engine.set_date_column(date_column_to_partition=self.extraction_date_column)
        df = self.engine.process(df)
        self.writer.write(dataframe=df, table_name=table_to_write, partition_cols=self.parquet_partition_cols)

    def _clean(self, table_to_read: TableName) -> None:
        df = self.reader.read(table_name=table_to_read)
        data_subsets = PipelineUtils.split_dataframe(dataframe=df, column_to_split=self.column_separator)
        for subset in data_subsets:
            subset_table_name = PipelineUtils.get_subset_table_name(dataframe=subset, subset_col_id=self.column_separator)
            processed_table = self.engine.process(subset)
            self.writer.write(dataframe=processed_table, table_name=subset_table_name)

    def _refine(self) -> None:
        if (self.reader_format == Format.DELTA) and (self.engine.type == EngineType.REFINEMENT):
            self.reader: DeltaHandler
            self.engine: RefinementEngine

            # for refined_table in ["summary", "monthly", "weekly"]:
            #     remove_path_if_exists(self.writer.generate_path(table_name=refined_table))

            for type in [RefinementType.SUMMARY]:  # , RefinementType.MONTHLY, RefinementType.WEEKLY]:
                self.engine.set_refinement_type(type)
                processed_dataframes = []
                for cleaned_path in self.reader.list_delta_tables():
                    df_cleaned = self.reader.read(table_name=cleaned_path)
                    df_processed = self.engine.process(df_cleaned)
                    processed_dataframes.append(df_processed) if df_processed is not None else None
                df_refined = self.engine.union_dataframes(dataframes=processed_dataframes)
                self.writer.write(dataframe=df_refined, table_name=type.value)

        else:
            self.logger.error("Reader is not an instance of DeltaHandler for REFINEMENT process")

    def execute(self, table_to_read: TableName = None, table_to_write: TableName = None) -> None:
        self.logger.info(f"Starting pipeline execution for {self.engine.type.value.upper()} process")

        if self.engine.type == EngineType.EXTRACTION:
            self._extract(table_to_read=table_to_read, table_to_write=table_to_write)

        if self.engine.type == EngineType.CLEANING:
            self._clean(table_to_read=table_to_read)

        if self.engine.type == EngineType.REFINEMENT:
            self._refine()

        self.logger.info(f"Pipeline execution for {self.engine.type.value.upper()} process finished")
