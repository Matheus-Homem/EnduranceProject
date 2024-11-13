from typing import Dict, List

from src.etl.core.definitions import Format, Layer
from src.etl.core.io.manager import IOManager


class GoldReader:

    @staticmethod
    def summary(habit_action: str = None) -> List[Dict[str, str]]:
        gold_handler = IOManager(layer=Layer.GOLD, format=Format.DELTA).get_handler()
        df_sorted = gold_handler.read("summary").sort_values(by="last_date", ascending=False)
        if habit_action:
            df_sorted = df_sorted[df_sorted["habit_action"] == habit_action]
        return convert_all_float_to_int(df_sorted.to_dict(orient="records"))

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
                record[key] = int(value)
    return df_dict
