import os

import yaml

from src.etl.definitions import BronzeTable, GoldTable, SilverTable, Table
from src.etl.pipeline.models import CleanerPipeline, ExtractorPipeline, RefinerPipeline
from src.shared.database.tables import MySqlMorningTable, MySqlNightTable
from src.shared.logger import LoggingManager
from src.shared.utilities.functions import get_class_by_name


class PipelineManager:
    logger_manager = LoggingManager()
    logger_manager.set_class_name("PipelineManager")
    logger = logger_manager.get_logger()

    @staticmethod
    def process_table(table: Table):
        logger = PipelineManager.logger

        if isinstance(table, BronzeTable):
            logger.info(f"Processing table '{table.name}' with ExtractorPipeline")
            ExtractorPipeline.execute(table=table)
            logger.info(
                f"Successfully processed table '{table.name}' as a BronzeTable."
            )

        if isinstance(table, SilverTable):
            logger.info(f"Processing table '{table.name}' with CleanerPipeline")
            CleanerPipeline.execute(table=table)
            logger.info(
                f"Successfully processed table '{table.name}' as a SilverTable."
            )

        if isinstance(table, GoldTable):
            logger.info(f"Processing table '{table.name}' with RefinerPipeline")
            RefinerPipeline.execute(table=table)
            logger.info(f"Successfully processed table '{table.name}' as a GoldTable.")

    @staticmethod
    def run_pipeline(bronze: bool = False, silver: bool = False, gold: bool = False):

        logger = PipelineManager.logger
        c = 0

        table_class_mapping = {
            "BronzeTable": bronze,
            "SilverTable": silver,
            "GoldTable": gold,
        }

        if not any([bronze, silver, gold]):
            error_message = "At least one of the parameters 'bronze', 'silver', or 'gold' must be set to True"
            logger.error(f"No pipeline selected for execution: {error_message}")
            raise ValueError(error_message)

        with open(os.path.join("src", "etl", "tables.yaml"), "r") as file:
            data = yaml.safe_load(file)

        logger.info(
            "Starting pipeline execution for layers: "
            + ", ".join([k for k, v in table_class_mapping.items() if v])
        )

        for table in data["tables"]:
            table_class_name = table["table_class"]
            source_name = table["source"]
            name = table["name"]

            if table_class_mapping.get(table_class_name, False):

                try:
                    table_class = get_class_by_name(
                        table_class_name, [BronzeTable, SilverTable, GoldTable]
                    )
                except ValueError as e:
                    error_message = f"Name {table_class_name} must be 'BronzeTable', 'SilverTable' or 'GoldTable': {e}"
                    logger.error(error_message)
                    raise ValueError(error_message)

                try:
                    source = get_class_by_name(
                        source_name, [MySqlMorningTable, MySqlNightTable]
                    )
                except ValueError as e:
                    error_message = (
                        f"Name {source_name} must be a valid source name: {e}"
                    )
                    logger.error(error_message)
                    raise ValueError(error_message)

                PipelineManager.process_table(table_class(source=source, name=name))
                c += 1

        logger.info(f"Pipeline execution completed. Executed {c} tables.")
