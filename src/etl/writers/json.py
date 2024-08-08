from src.etl.definitions import Writer


class JsonWriter(Writer):

    def write(self, df):
        print("Writing to JSON file")
