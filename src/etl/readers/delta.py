from src.etl.definitions import Reader


class DeltaReader(Reader):

    def read_dataframe(self):
        print("Reading from Delta table")
        return None
