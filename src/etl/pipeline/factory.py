from src.etl.definitions import Table
from src.etl.pipeline.models import CleanerPipeline, ExtractorPipeline, RefinerPipeline
from src.etl.tables.bronze import BronzeTable
from src.etl.tables.gold import GoldTable
from src.etl.tables.silver import SilverTable


class FactoryPipeline:

    @staticmethod
    def execute_table(table: Table):

        if isinstance(table, BronzeTable):
            ExtractorPipeline.execute(table=table)

        if isinstance(table, SilverTable):
            CleanerPipeline.execute(table=table)

        if isinstance(table, GoldTable):
            RefinerPipeline.execute(table=table)
