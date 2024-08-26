from src.shared.logging.manager import LoggingManager
import logging

LoggingManager()

class LoggingPrinter:

    def __init__(self, class_name: str) -> None:
        self.logger = logging.getLogger(class_name)

def raise_error_and_log(logger: logging.Logger, error_message: str) -> None:
    logger.error(error_message)
    raise ValueError(error_message)