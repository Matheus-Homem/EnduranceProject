from src.etl.definitions import Table
from src.shared.database.tables import MySqlMorningTable, MySqlNightTable, MySqlTable


class BronzeTable(Table):
    source: MySqlTable
    layer: str = "bronze"
    format: str = "parquet"


class MorningBronzeTable(BronzeTable):
    source = MySqlMorningTable
    name = "morning_raw"


class NightBronzeTable(BronzeTable):
    source = MySqlNightTable
    name = "night_raw"
