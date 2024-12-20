import base64
import hashlib
import json
import re
from datetime import date, datetime
from typing import List

import pytz
from unidecode import unidecode


class StringUtils:

    @staticmethod
    def remove_linebreaks(input: str) -> str:
        return re.sub(r"[\r\n]", "", input)

    @staticmethod
    def remove_special_characters(input: str) -> str:
        return unidecode(input)

    @staticmethod
    def clean_string(input: str) -> str:
        return StringUtils.remove_special_characters(StringUtils.remove_linebreaks(input))

    @staticmethod
    def stringify_list(list: List[str]) -> str:
        return ",".join(list)


class DictUtils:

    @staticmethod
    def serialize_dict(dict: dict) -> str:
        return json.dumps(dict)

    @staticmethod
    def clean_and_serialize_dict(input_dict: dict) -> str:
        cleaned_dict = {StringUtils.clean_string(key): StringUtils.clean_string(str(value)) for key, value in input_dict.items()}
        serialized_dict = DictUtils.serialize_dict(cleaned_dict)
        return serialized_dict

    @staticmethod
    def deserialize_dict(data: str) -> dict:
        return json.loads(data)


class ValidationUtils:

    @staticmethod
    def is_valid_password(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_list_of_strings(input: List[str]) -> bool:
        return isinstance(input, list) and all(isinstance(item, str) for item in input)


class DateUtils:

    @staticmethod
    def convert_date_input(date_to_convert: str, format=None) -> date:
        """
        For YYYY-MM-DD format, use format='%Y-%m-%d'
        For YYYY/MM/DD format, use format='%Y/%m/%d'
        For YYYYMMDD format, use format='%Y%m%d'
        """
        if not format:
            return date.fromisoformat(date_to_convert)
        return datetime.strptime(date_to_convert, format).date()

    @staticmethod
    def get_brasilia_datetime() -> datetime:
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    @staticmethod
    def get_brasilia_date() -> date:
        return datetime.now(pytz.timezone("America/Sao_Paulo")).date()

    @staticmethod
    def get_utc_date() -> date:
        return datetime.now().date()

    @staticmethod
    def fetch_current_date_sao_paulo() -> str:
        return datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d")


class HashUtils:

    @staticmethod
    def string_to_sha256(input: str) -> str:
        return hashlib.sha256(input.encode("utf-8")).hexdigest()


class EncodingUtils:
    @staticmethod
    def encode_to_base64(input_string: str) -> str:
        return base64.b64encode(input_string.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_from_base64(encoded_string: str) -> str:
        return base64.b64decode(encoded_string.encode("utf-8")).decode("utf-8")
