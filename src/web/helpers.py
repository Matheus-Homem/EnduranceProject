import re
from datetime import date

from src.shared.utilities.text import TextUtilities


def clean_and_serialize_dict(data: dict) -> str:
    cleaned_dict = {TextUtilities.clean_string(key): TextUtilities.clean_string(str(value)) for key, value in data.items()}
    serialized_dict = TextUtilities.serialize_dict(cleaned_dict)
    return serialized_dict


def convert_input_date(date_to_convert: str) -> date:
    return date.fromisoformat(date_to_convert)


def display_success_message(text: str) -> None:
    print(f"\033[92mSUCCESS - {text}\033[0m")


def display_debug_message(text: str) -> None:
    print(f"\033[95mDEBUG - {text}\033[0m")


def display_error_message(text: str) -> None:
    print(f"\033[91mERROR - {text}\033[0m")


def is_valid_password(password) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


def is_valid_email(email) -> bool:
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None
