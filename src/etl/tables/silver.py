# from src.etl.definitions import Path, Table
# from src.etl.readers.parquet import ParquetReader
# from src.etl.tables.bronze import BronzeTable, NightBronzeTable
# from src.etl.writers.delta import DeltaWriter


# class SilverTable(Table):
#     source: Path
#     layer: str = "silver"


# class NavigatorTable(SilverTable):
#     source = NightBronzeTable.get_path
#     name = "navigator"
