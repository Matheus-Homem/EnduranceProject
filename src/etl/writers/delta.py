from src.etl.definitions import Writer


class DeltaWriter(Writer):

    def write(self, df):
        print("Writing to Delta table")
