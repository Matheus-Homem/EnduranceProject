from src.shared.utilities.text import TextUtilities
from datetime import date


def clean_and_serialize_dict(data: dict) -> str:
    cleaned_dict = {TextUtilities.clean_string(key): TextUtilities.clean_string(str(value)) for key, value in data.items()}
    serialized_dict = TextUtilities.serialize_dict(cleaned_dict)
    return serialized_dict

    
def convert_input_date(date_to_convert: str) -> date:
    return date.fromisoformat(date_to_convert)


def print_green(text: str):
    print(f"\033[92mSUCCESS - {text}\033[0m")
