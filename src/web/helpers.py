import re
from datetime import date

from src.shared.utilities.text import TextUtilities


class WebUtils:

    @staticmethod
    def clean_and_serialize_dict(data: dict) -> str:
        cleaned_dict = {TextUtilities.clean_string(key): TextUtilities.clean_string(str(value)) for key, value in data.items()}
        serialized_dict = TextUtilities.serialize_dict(cleaned_dict)
        return serialized_dict

    @staticmethod
    def convert_input_date(date_to_convert: str) -> date:
        return date.fromisoformat(date_to_convert)

    @staticmethod
    def is_valid_password(password) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    @staticmethod
    def is_valid_email(email) -> bool:
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None


class SimpleMessagePrinter:

    @staticmethod
    def success(text: str) -> None:
        print(f"\033[92mSUCCESS - {text}\033[0m")

    @staticmethod
    def debug(text: str) -> None:
        print(f"\033[95mDEBUG - {text}\033[0m")

    @staticmethod
    def error(text: str) -> None:
        print(f"\033[91mERROR - {text}\033[0m")
