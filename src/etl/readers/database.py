from src.etl.definitions import Reader


class DatabaseReader(Reader):

    def read(self):
        print("Reading from database")
        return None
