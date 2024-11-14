from math import isnan
from typing import Dict, List

from src.etl.core.definitions import Format, Layer
from src.etl.core.io.manager import IOManager


class GoldReader:

    @staticmethod
    def summary(element: str) -> List[Dict[str, str]]:
        gold_handler = IOManager(layer=Layer.GOLD, format=Format.DELTA).get_handler()
        df_sorted = gold_handler.read("summary").sort_values(by="last_date", ascending=False)
        df_filtered = df_sorted[df_sorted["element_name"] == element]
        return convert_all_float_to_int(df_filtered.to_dict(orient="records"))

    @staticmethod
    def monthly() -> List[Dict[str, str]]:
        pass

    @staticmethod
    def weekly() -> List[Dict[str, str]]:
        pass


def convert_all_float_to_int(df_dict: List[Dict[str, str]]) -> List[Dict[str, str]]:
    for record in df_dict:
        for key, value in record.items():
            if isinstance(value, float):
                record[key] = int(value) if not isnan(value) else None
    return df_dict
