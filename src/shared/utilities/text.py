import json
import re

from unidecode import unidecode


class TextUtilities:

    @staticmethod
    def remove_newlines(input: str) -> str:
        return re.sub(r"[\r\n]", "", input)

    @staticmethod
    def remove_special_characters(input: str) -> str:
        return unidecode(input)

    @staticmethod
    def clean_string(input: str) -> str:
        return TextUtilities.remove_special_characters(TextUtilities.remove_newlines(input))

    @staticmethod
    def serialize_dict(data: dict) -> str:
        return json.dumps(data)
