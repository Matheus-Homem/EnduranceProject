from src.etl.definitions import Reader


class DeltaReader(Reader):

    def read_data(self):
        print("Reading from Delta table")
        return None
