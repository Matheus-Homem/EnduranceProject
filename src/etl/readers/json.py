from src.etl.definitions import Reader


class JsonReader(Reader):

    def read(self):
        print("Reading from JSON file")
        return None
