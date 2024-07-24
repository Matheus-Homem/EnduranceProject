import json
import re

def clean_form_data(data: dict) -> str:
    def regex_remove(input: str) -> str:
        return re.sub(r'[\r\n]', '', str(input))
    cleaned_data = {regex_remove(key): regex_remove(str(value)) for key, value in data.items()}
    seriealized_data = json.dumps(cleaned_data)
    return seriealized_data