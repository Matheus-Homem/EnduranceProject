import logging

import colorlog

from os_local import join_paths

SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)


logging.Logger.success = success


class LoggerInitializer:
    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        self._add_console_handler(logger)

    def _custom_format(self, record) -> str:
        src_path = join_paths("src", "")
        src_index = record.pathname.lower().find(src_path)

        if src_index == -1:
            return ""

        record.pathname = record.pathname[src_index:]

        if hasattr(record, "funcName") and hasattr(record, "module"):
            record.funcName = f"{record.name}.{record.funcName}" if not "." in record.funcName else record.funcName

        return self.formatter.format(record)

    def _filter_empty_messages(self, record) -> bool:
        message = self._custom_format(record)
        return message != ""

    def _add_console_handler(self, logger: logging.Logger) -> None:
        self.formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
            log_colors={
                "DEBUG": "purple",
                "INFO": "cyan",
                "SUCCESS": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(self.formatter)

        console_handler.addFilter(self._filter_empty_messages)
        logger.addHandler(console_handler)

    @staticmethod
    def raise_error_and_log(logger: logging.Logger, error_message: str) -> None:
        logger.error(error_message)
        raise ValueError(error_message)

    @staticmethod
    def reset_logger() -> None:
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
