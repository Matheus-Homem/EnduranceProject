from src.etl.definitions import Writer


class DeltaWriter(Writer):

    def write_data(self, df):
        print("Writing to Delta table")
