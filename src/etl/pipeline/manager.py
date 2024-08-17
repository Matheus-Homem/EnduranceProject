import os
from typing import Any

import yaml

from src.etl.definitions import BronzeTable, GoldTable, SilverTable, Table
from src.etl.pipeline.models import CleanerPipeline, ExtractorPipeline, RefinerPipeline
from src.shared.database.tables import MySqlMorningTable, MySqlNightTable
from src.shared.logger import LoggingManager
from src.shared.utilities.functions import get_class_by_name, log_and_raise_error


class PipelineManager:

    def __init__(self, bronze: bool = False, silver: bool = False, gold: bool = False) -> None:
        logger_manager = LoggingManager()
        logger_manager.set_class_name(self.__class__.__name__)
        self.logger = logger_manager.get_logger()
        self.bronze = bronze
        self.silver = silver
        self.gold = gold
        self.has_enabled_layers = any([bronze, silver, gold])

    @staticmethod
    def process_table(table: Table) -> None:

        if isinstance(table, BronzeTable):
            ExtractorPipeline.execute(table=table)

        if isinstance(table, SilverTable):
            CleanerPipeline.execute(table=table)

        if isinstance(table, GoldTable):
            RefinerPipeline.execute(table=table)

    def get_class_or_raise(self, class_name: str, object_list: list, error_message: str) -> Any:
        retrieved_class = get_class_by_name(class_name, object_list)
        if retrieved_class is None:
            log_and_raise_error(
                error_message=error_message,
                logger=self.logger,
                exception=ValueError,
            )
        return retrieved_class

    @property
    def table_layer_flags(self) -> dict:
        return {
            "BronzeTable": self.bronze,
            "SilverTable": self.silver,
            "GoldTable": self.gold,
        }

    def load_table_data(self) -> dict:
        with open(os.path.join("src", "etl", "tables.yaml"), "r") as file:
            return yaml.safe_load(file)

    def run_pipeline(self) -> None:

        processed_tables = []

        if not self.has_enabled_layers:
            log_and_raise_error(
                error_message="At least one of the parameters 'bronze', 'silver', or 'gold' must be set to True",
                logger=self.logger,
                exception=ValueError,
            )

        data = self.load_table_data()

        self.logger.info("Starting pipeline execution for layers: " + ", ".join([k for k, v in self.table_layer_flags.items() if v]))

        for table in data["tables"]:
            self.logger.info(f"Processing table {table['name']} as {table['table_class']} with source {table['source']}")
            table_class_name, source_name, name = (
                table["table_class"],
                table["source"],
                table["name"],
            )

            table_class = self.get_class_or_raise(
                table_class_name,
                [BronzeTable, SilverTable, GoldTable],
                f"Name {table_class_name} must be 'BronzeTable', 'SilverTable' or 'GoldTable'",
            )
            source = self.get_class_or_raise(
                source_name,
                [MySqlMorningTable, MySqlNightTable],
                f"Name {source_name} must be a valid source name",
            )

            if self.table_layer_flags.get(table_class_name, False):

                PipelineManager.process_table(table_class(source=source, name=name))
                self.logger.info(f"Table {table['name']} processed successfully.")
                processed_tables.append(table["name"])

        self.logger.info(f"Pipeline execution completed. Executed {len(processed_tables)} tables.")
