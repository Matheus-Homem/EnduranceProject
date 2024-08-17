import os
from typing import List, Tuple, Type

import yaml

from src.etl.definitions import BronzeTable, GoldTable, SilverTable, Table
from src.etl.pipeline.models import CleanerPipeline, ExtractorPipeline, RefinerPipeline
from src.shared.database.tables import MySqlMorningTable, MySqlNightTable
from src.shared.logger import LoggingManager


class PipelineManager:

    def __init__(self, bronze: bool = False, silver: bool = False, gold: bool = False) -> None:
        logger_manager = LoggingManager()
        logger_manager.set_class_name(self.__class__.__name__)
        self.logger = logger_manager.get_logger()
        self.table_layer_flags = {
            "BronzeTable": bronze,
            "SilverTable": silver,
            "GoldTable": gold,
        }
        self.has_enabled_layers = any([bronze, silver, gold])
        self.active_layers = ", ".join([k.replace("Table", "") for k, v in self.table_layer_flags.items() if v])

    @staticmethod
    def process_table(table: Table) -> None:

        if isinstance(table, BronzeTable):
            ExtractorPipeline.execute(table=table)

        if isinstance(table, SilverTable):
            CleanerPipeline.execute(table=table)

        if isinstance(table, GoldTable):
            RefinerPipeline.execute(table=table)

    @staticmethod
    def load_table_data() -> dict:
        with open(os.path.join("src", "etl", "tables.yaml"), "r") as file:
            return yaml.safe_load(file)

    def check_enabled_layers(self) -> None:
        if not self.has_enabled_layers:
            error_message = "At least one of the parameters 'bronze', 'silver', or 'gold' must be set to True"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def get_class_or_raise(self, class_name: str, object_list: List[Type], error_message: str) -> Type:
        retrieved_class = get_class_by_name(class_name, object_list)
        if retrieved_class is None:
            self.logger.error(error_message)
            raise ValueError(error_message)
        return retrieved_class

    def identify_table_and_source(self, table_type_str: str, source_str: str) -> Tuple:

        table_type = self.get_class_or_raise(
            table_type_str,
            [BronzeTable, SilverTable, GoldTable],
            f"Name {table_type_str} must be 'BronzeTable', 'SilverTable' or 'GoldTable'",
        )

        if table_type == BronzeTable:
            source = self.get_class_or_raise(
                source_str,
                [MySqlMorningTable, MySqlNightTable],
                f"Name {source_str} must be a valid source name",
            )
        elif table_type == SilverTable:
            source = BronzeTable(name=source_str, source=None)
        elif table_type == GoldTable:
            source = SilverTable(name=source_str, source=None)

        return table_type, source

    def run_pipeline(self) -> None:

        processed_tables = []

        self.check_enabled_layers()

        data = PipelineManager.load_table_data()

        self.logger.info("Starting pipeline execution for layers: " + self.active_layers)

        for table in data["tables"]:
            table_type_str, source_str, name = (
                table["table_type"],
                table["source"],
                table["name"],
            )

            self.logger.info(f"Trying to process table '{name}' as {table_type_str} with source {source_str}")

            if self.table_layer_flags.get(table_type_str, False):

                table_type, source = self.identify_table_and_source(table_type_str, source_str)

                self.logger.info(f"Starting '{name}' table execution.")
                PipelineManager.process_table(table_type(source=source, name=name))
                self.logger.info(f"Finished '{name}' table execution.")
                processed_tables.append(table["name"])
            else:
                self.logger.info(f"Table '{name}' was not processed because layer {table_type_str} is not enabled.")

        self.logger.info(f"Pipeline execution completed. Executed {len(processed_tables)} tables.")


def get_class_by_name(class_name: str, object_list: list):
    return next((cls for cls in object_list if cls.__name__ == class_name), None)
