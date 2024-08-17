from src.shared.utilities.text import TextUtilities


def clean_and_serialize_dict(data: dict) -> str:
    cleaned_dict = {TextUtilities.clean_string(key): TextUtilities.clean_string(str(value)) for key, value in data.items()}
    serialized_dict = TextUtilities.serialize_dict(cleaned_dict)
    return serialized_dict
