import logging
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, call, patch

from src.shared.logger import CustomFormatter, LoggingManager


class TestLoggingManager(unittest.TestCase):

    @patch("src.shared.logger.logging.getLogger")
    @patch.object(LoggingManager, "_add_file_handler")
    @patch.object(LoggingManager, "_add_console_handler")
    def test_initialize_logger_adds_handlers(
        self, mock_add_console_handler, mock_add_file_handler, mock_get_logger
    ):
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = False
        mock_get_logger.return_value = mock_logger

        log_level = logging.DEBUG
        log_file = None
        class_name = "TestLoggingManager"

        logging_manager = LoggingManager(log_level, log_file, class_name)

        mock_add_file_handler.assert_called_once_with(mock_logger, log_file, class_name)
        mock_add_console_handler.assert_called_once_with(mock_logger)

    @patch("src.shared.logger.logging.getLogger")
    @patch.object(LoggingManager, "_add_file_handler")
    @patch.object(LoggingManager, "_add_console_handler")
    def test_initialize_logger_does_not_add_handlers(
        self, mock_add_console_handler, mock_add_file_handler, mock_get_logger
    ):
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = True
        mock_get_logger.return_value = mock_logger

        log_level = logging.DEBUG
        log_file = None
        class_name = "TestLoggingManager"

        logging_manager = LoggingManager(log_level, log_file, class_name)
        logging_manager._initialize_logger(log_level, log_file, class_name)

        mock_add_file_handler.assert_not_called()
        mock_add_console_handler.assert_not_called()

    @patch("src.shared.logger.os.makedirs")
    @patch("src.shared.logger.logging.FileHandler")
    @patch("src.shared.logger.datetime")
    def test_can_add_file_handler(
        self, mock_datetime, mock_file_handler, mock_makedirs
    ):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.strftime = datetime.strftime

        logger = logging.getLogger("test_logger")
        logger.handlers = []

        logging_manager = LoggingManager(logging.DEBUG, None, "TestClass")

        logging_manager._add_file_handler(logger, None, "TestClass")

        mock_makedirs.assert_called_once_with(
            os.path.join("outputs", "logs", "2023-01-01"), exist_ok=True
        )

        expected_log_file = os.path.join(
            "outputs", "logs", "2023-01-01", "logs_20230101_120000.log"
        )
        mock_file_handler.assert_called_once_with(expected_log_file)

        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], MagicMock)

        self.assertIsInstance(
            logger.handlers[0].setFormatter.call_args[0][0], CustomFormatter
        )

    @patch("src.shared.logger.colorlog.StreamHandler")
    @patch("src.shared.logger.colorlog.ColoredFormatter")
    def test_add_console_handler(self, mock_colored_formatter, mock_stream_handler):
        mock_logger = MagicMock(spec=logging.Logger)

        logging_manager = LoggingManager(logging.DEBUG, None, "TestLoggingManager")

        logging_manager._add_console_handler(mock_logger)

        mock_colored_formatter.assert_called_once_with(
            "%(log_color)s%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "purple",
                "INFO": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
            },
        )

        mock_stream_handler_instance = mock_stream_handler.return_value
        mock_stream_handler_instance.setFormatter.assert_called_once_with(
            mock_colored_formatter.return_value
        )

        mock_logger.addHandler.assert_called_once_with(mock_stream_handler_instance)

    @patch.object(LoggingManager, "_initialize_logger")
    def test_if_set_class_name_can_initializes_logger(self, mock_initialize_logger):
        logging_manager = LoggingManager(log_level=logging.DEBUG)

        mock_logger = MagicMock()
        logging_manager.logger = mock_logger

        class_name = "TestClassName"
        logging_manager.set_class_name(class_name)

        self.assertEqual(logging_manager.class_name, class_name)
        self.assertEqual(mock_initialize_logger.call_count, 2)

    def test_get_logger(self):
        logging_manager = LoggingManager(logging.DEBUG, None, "TestClassName")

        mock_logger = MagicMock()
        logging_manager.logger = mock_logger

        logger = logging_manager.get_logger()

        self.assertEqual(logger, mock_logger)


if __name__ == "__main__":
    unittest.main()
