import inspect
import logging
import os
from datetime import datetime

import colorlog


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, class_name):
        super().__init__(fmt)
        self.class_name = class_name

    def set_class_name(self, class_name):
        self.class_name = class_name

    def format(self, record):
        src_index = record.pathname.find("src")
        if src_index != -1:
            record.pathname = record.pathname[src_index:]
        if isinstance(self.class_name, str):
            record.funcName = f"{self.class_name}.{record.funcName}"
        return super().format(record)


class LoggingManager:
    def __init__(self, log_level=logging.DEBUG, log_file=None, class_name=None):
        self.logger = self._initialize_logger(log_level, log_file, class_name)
        self.class_name = class_name

    def _initialize_logger(self, log_level, log_file, class_name):
        caller_frame = inspect.stack()[1]
        frame_info = inspect.getframeinfo(caller_frame[0])
        caller_filename = frame_info.filename
        caller_function = frame_info.function

        logger_name = f"{caller_filename}.{class_name}.{caller_function}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        self._add_file_handler(logger, log_file, class_name)
        self._add_console_handler(logger)

        return logger

    def _add_file_handler(self, logger, log_file, class_name):
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join("outputs", "logs", date_str)
        os.makedirs(log_dir, exist_ok=True)

        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"logs_{timestamp}.log")

        file_handler = logging.FileHandler(log_file)
        self.file_formatter = CustomFormatter(
            "%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s",
            class_name,
        )
        file_handler.setFormatter(self.file_formatter)
        logger.addHandler(file_handler)

    def _add_console_handler(self, logger):
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "purple",
                "INFO": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
            },
        )
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def set_class_name(self, class_name):
        if self.class_name is None:
            self.class_name = class_name
            self.logger = self._initialize_logger(self.logger.level, None, class_name)

    def get_logger(self):
        return self.logger