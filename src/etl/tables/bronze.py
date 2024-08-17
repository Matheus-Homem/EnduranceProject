# from src.etl.definitions import Table
# from src.shared.database.tables import MySqlMorningTable, MySqlNightTable, MySqlTable


# class BronzeTable(Table):

#     def __init__(
#         self,
#         name: str,
#         source: MySqlTable,
#         layer: str = "bronze",
#         format: str = "parquet",
#     ) -> None:
#         super().__init__(name, source, layer, format=format)


# class MorningBronzeTable(BronzeTable):
#     source = MySqlMorningTable
#     name = "morning_raw"


# class NightBronzeTable(BronzeTable):
#     source = MySqlNightTable
#     name = "night_raw"
