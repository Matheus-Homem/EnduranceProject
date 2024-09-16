from datetime import date

from src.shared.utilities.text import TextUtilities


def clean_and_serialize_dict(data: dict) -> str:
    cleaned_dict = {TextUtilities.clean_string(key): TextUtilities.clean_string(str(value)) for key, value in data.items()}
    serialized_dict = TextUtilities.serialize_dict(cleaned_dict)
    return serialized_dict


def convert_input_date(date_to_convert: str) -> date:
    return date.fromisoformat(date_to_convert)


def display_success_message(text: str):
    print(f"\033[92mSUCCESS - {text}\033[0m")

def display_debug_message(text: str):
    print(f"\033[95mDEBUG - {text}\033[0m")