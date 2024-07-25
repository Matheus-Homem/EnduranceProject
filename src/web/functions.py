from src.shared.utils import StringUtils


def prepare_dict_to_command(data: dict) -> str:
    cleaned_dict = {
        StringUtils.clean_string(key): StringUtils.clean_string(str(value))
        for key, value in data.items()
    }
    serialized_dict = StringUtils.serialize_dict(cleaned_dict)
    return serialized_dict
