import hashlib
import json
import re
from datetime import date, datetime
import pytz
from unidecode import unidecode


class StringUtils:

    @staticmethod
    def remove_newlines(input: str) -> str:
        return re.sub(r"[\r\n]", "", input)

    @staticmethod
    def remove_special_characters(input: str) -> str:
        return unidecode(input)

    @staticmethod
    def clean_string(input: str) -> str:
        return StringUtils.remove_special_characters(StringUtils.remove_newlines(input))
    
    @staticmethod
    def convert_list_to_string(input_list: list) -> str:
        return ",".join(input_list)


class DictUtils:

    @staticmethod
    def serialize_dict(data: dict) -> str:
        return json.dumps(data)

    @staticmethod
    def clean_and_serialize_dict(data: dict) -> str:
        cleaned_dict = {StringUtils.clean_string(key): StringUtils.clean_string(str(value)) for key, value in data.items()}
        serialized_dict = DictUtils.serialize_dict(cleaned_dict)
        return serialized_dict


class ValidationUtils:

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


class DateUtils:

    @staticmethod
    def convert_input_date(date_to_convert: str) -> date:
        return date.fromisoformat(date_to_convert)
    
    @staticmethod
    def current_brasilia_sp_time():
        return datetime.now(pytz.timezone("America/Sao_Paulo"))


class HashUtils:

    @staticmethod
    def hash_list(input_list: list) -> str:
        return hashlib.sha256(str(input_list).encode("utf-8")).hexdigest()
