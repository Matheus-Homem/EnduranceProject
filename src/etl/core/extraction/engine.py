from src.etl.core.definitions import DatabaseDF, Engine, EngineType, PandasDF


class ExtractionEngine(Engine):

    def __init__(self):
        super().__init__(class_name=__class__.__name__, type=EngineType.EXTRACTION)
        self.column_to_partition = None

    def set_date_column(
        self,
        date_column_to_partition: str,
    ) -> None:
        self.column_to_partition = date_column_to_partition

    def _convert_to_dataframe(
        self,
        input_data: DatabaseDF,
    ) -> PandasDF:
        return self._pd.DataFrame(input_data)

    def _add_partition_columns(
        self,
        dataframe: PandasDF,
    ) -> PandasDF:
        if self.column_to_partition not in dataframe.columns:
            raise ValueError(f"Column '{self.column_to_partition}' not found in DataFrame")

        datetime_partition_column = self._pd.to_datetime(dataframe[self.column_to_partition], errors="coerce")
        if datetime_partition_column.isnull().any():
            raise ValueError(f"Column '{self.column_to_partition}' contains invalid date values")

        dataframe["year"] = datetime_partition_column.dt.year
        dataframe["month"] = datetime_partition_column.dt.month
        dataframe["day"] = datetime_partition_column.dt.day
        return dataframe

    def process(self, dataframe: DatabaseDF) -> PandasDF:
        self.logger.info("Starting data processing for extraction tables")

        if self.column_to_partition is None:
            raise ValueError("Date column for partitioning is not set. Please call 'set_date_column' method first.")

        dataframe = self._convert_to_dataframe(dataframe)
        dataframe = self._add_partition_columns(dataframe)
        return dataframe
