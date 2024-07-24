import json
import re


def clean_string(input: str) -> str:
    return re.sub(r"[\r\n]", "", input)


def prepare_form_data(data: dict) -> str:
    cleaned_data = {
        clean_string(key): clean_string(str(value)) for key, value in data.items()
    }
    seriealized_data = json.dumps(cleaned_data)
    return seriealized_data
