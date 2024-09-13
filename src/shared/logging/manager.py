import logging

import colorlog

from src.shared.logging.custom_formatter import CustomColoredFormatter

SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)


logging.Logger.success = success


class LoggingManager:
    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        self._add_console_handler(logger)

    def _add_console_handler(self, logger: logging.Logger) -> None:
        formatter = CustomColoredFormatter(
            "%(log_color)s%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "purple",
                "INFO": "cyan",
                "SUCCESS": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(formatter)

        def filter_empty_messages(record):
            message = formatter.format(record)
            return message != ""

        console_handler.addFilter(filter_empty_messages)
        logger.addHandler(console_handler)
