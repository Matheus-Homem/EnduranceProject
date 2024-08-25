import os
from typing import Union

import logging
import yaml

from src.etl.definitions import BronzeTable, GoldTable, SilverTable, Table
from src.etl.pipeline.models import CleanerPipeline, ExtractorPipeline, RefinerPipeline
from src.shared.database.tables import MySqlMorningTable, MySqlNightTable, MySqlTable
from src.shared.logger import LoggingManager, raise_error_and_log

LoggingManager.initialize_logger(log_level=logging.DEBUG)

class PipelineManager:

    def __init__(self, logger_manager=LoggingManager(), bronze: bool = False, silver: bool = False, gold: bool = False) -> None:
        logger_manager.set_class_name(self.__class__.__name__)
        self.logger = logging.getLogger(self.__class__.__name__)

        if not any([bronze, silver, gold]):
            raise_error_and_log("At least one of the parameters 'bronze', 'silver', or 'gold' must be set to True")

        self.table_layer_flags = {
            "BronzeTable": bronze,
            "SilverTable": silver,
            "GoldTable": gold,
        }
        self.active_layers = ", ".join([k.replace("Table", "") for k, v in self.table_layer_flags.items() if v])
        self.valid_layer_classes = [BronzeTable, SilverTable, GoldTable]
        self.sql_tables_list = [MySqlMorningTable, MySqlNightTable]

    @staticmethod
    def process_table(table: Table) -> None:
        if isinstance(table, BronzeTable):
            ExtractorPipeline.execute(table=table)

        if isinstance(table, SilverTable):
            CleanerPipeline.execute(table=table)

        if isinstance(table, GoldTable):
            RefinerPipeline.execute(table=table)

    def get_layer_class(self, layer_class_str: str) -> Table:
        layer_class = next((cls for cls in self.valid_layer_classes if cls.__name__ == layer_class_str), None)
        raise_error_and_log(f"Name {layer_class_str} must be 'BronzeTable', 'SilverTable' or 'GoldTable'") if layer_class is None else None
        return layer_class

    def get_source(self, layer_class: Table, source_str: str) -> Union[MySqlTable, Table]:
        if layer_class == BronzeTable:
            source = next((cls for cls in self.sql_tables_list if cls.__name__ == source_str), None)
            raise_error_and_log(f"Name {source_str} must be a valid source name") if source is None else None
        elif layer_class == SilverTable:
            source = BronzeTable(name=source_str, source=None)
        elif layer_class == GoldTable:
            source = SilverTable(name=source_str, source=None)
        return source

    def run_pipeline(self) -> None:

        processed_tables = []
        skipped_tables = []

        with open(os.path.join("src", "etl", "tables.yaml"), "r") as file:
            data = yaml.safe_load(file)

        self.logger.info("Starting pipeline execution for layers: " + self.active_layers)

        for table in data["tables"]:
            layer_class_str, source_str, name = (
                table["layer_class"],
                table["source"],
                table["name"],
            )

            if self.table_layer_flags.get(layer_class_str, False):

                layer_class = self.get_layer_class(layer_class_str)
                source = self.get_source(layer_class, source_str)

                self.logger.info(f"Executing for table: {name}")
                PipelineManager.process_table(layer_class(source=source, name=name))

                processed_tables.append(table["name"])

            else:
                skipped_tables.append(table["name"])

        self.logger.info(f"Skipped tables ({len(skipped_tables)}): {', '.join(skipped_tables)}") if skipped_tables else None
        self.logger.success(f"Pipeline execution completed. Executed {len(processed_tables)} tables.")
