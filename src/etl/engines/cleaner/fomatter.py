from typing import Union

from polars import Boolean, DataFrame, Date, Time, UInt8, UInt16, Utf8, col


class CleanerFormatter:
    def __init__(self):
        self.default_columns = ["data", "profile", "user_id", "created_at", "updated_at", "deleted_at"]

    def _get_time_conversion(self, col_name: str) -> callable:
        return (
            (lambda x: f"{x}:00" if isinstance(x, str) else x)
            if "time_header" in col_name
            else (lambda x: f"{(int(x[:2])//60):02}:{(int(x[:2])%60):02}:{(int(x[2:])):02}" if x not in ["", None, "null"] else None)
        )

    def _get_integer_cast(self, col_name: str) -> Union[UInt16, UInt8]:
        if any(keyword in col_name for keyword in ["calories", "distance"]):
            return UInt16
        elif any(keyword in col_name for keyword in ["radio", "id"]):
            return UInt8

    def _to_date(self, df: DataFrame, col_name: str) -> DataFrame:
        return df.with_columns(col(col_name).cast(Date).alias(col_name))

    def _to_time(self, df: DataFrame, col_name: str) -> DataFrame:
        return df.with_columns(col(col_name).map_elements(self._get_time_conversion(col_name)).str.strptime(Time, "%H:%M:%S").alias(col_name))

    def _to_boolean(self, df: DataFrame, col_name: str) -> DataFrame:
        return df.with_columns(
            col(col_name).map_elements(lambda x: True if x == "True" else (False if x == "False" else None)).cast(Boolean).alias(col_name)
        )

    def _to_string(self, df: DataFrame, col_name: str) -> DataFrame:
        return df.with_columns(col(col_name).map_elements(lambda x: None if x == "" else x).cast(Utf8).alias(col_name))

    def _to_integer(self, df: DataFrame, col_name: str) -> DataFrame:
        return df.with_columns(
            col(col_name).map_elements(lambda x: None if x == "" else int(x)).cast(self._get_integer_cast(col_name)).alias(col_name)
        )

    def _factory_cast(self, df: DataFrame, col_name: str) -> DataFrame:
        if col_name in self.default_columns:
            return df
        else:
            prefix = col_name.split("_")[0]
            if prefix == "date":
                df = self._to_date(df, col_name)
            elif prefix == "time":
                df = self._to_time(df, col_name)
            elif prefix in ["toggle", "multi"]:
                df = self._to_boolean(df, col_name)
            elif prefix in ["text", "textarea"]:
                df = self._to_string(df, col_name)
            elif prefix in ["calories", "distance", "radio", "id"]:
                df = self._to_integer(df, col_name)
            else:
                raise ValueError(f"Invalid column name prefix: {prefix}")
            return df

    def format_dataframe_columns(self, df: DataFrame) -> DataFrame:
        for col_name in df.columns:
            df = self._factory_cast(df, col_name)
        return df
