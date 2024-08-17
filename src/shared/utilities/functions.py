from logging import Logger


def get_class_by_name(class_name: str, object_list: list):
    return next((cls for cls in object_list if cls.__name__ == class_name), None)


def log_and_raise_error(logger: Logger, error_message: str, exception: Exception):
    logger.error(error_message)
    raise exception(error_message)
