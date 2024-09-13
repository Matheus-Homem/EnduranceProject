import logging
import unittest
from unittest.mock import MagicMock, patch

import colorlog

from src.shared.logging.custom_formatter import CustomColoredFormatter
from src.shared.logging.manager import LoggingManager


class TestLoggingManager(unittest.TestCase):

    @patch("src.shared.logging.manager.colorlog.StreamHandler")
    @patch("src.shared.logging.manager.CustomColoredFormatter")
    def test_add_console_handler(self, mock_colored_formatter, mock_stream_handler):
        mock_logger = MagicMock(spec=logging.Logger)

        LoggingManager()

        mock_colored_formatter.assert_called_once_with(
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

        mock_stream_handler_instance = mock_stream_handler.return_value
        mock_stream_handler_instance.setFormatter.assert_called_once_with(mock_colored_formatter.return_value)

        # mock_logger.addHandler.assert_called_once_with(mock_stream_handler_instance)

    @patch("src.shared.logging.manager.logging.getLogger")
    @patch.object(LoggingManager, "_add_console_handler")
    def test_initialize_logger_adds_handlers(self, mock_add_console_handler, mock_get_logger):
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = False
        mock_get_logger.return_value = mock_logger

        LoggingManager()

        mock_add_console_handler.assert_called_once_with(mock_logger)

    # @patch("src.shared.logging.manager.logging.getLogger")
    # @patch.object(LoggingManager, "_add_console_handler")
    # def test_initialize_logger_does_not_add_handlers(self, mock_add_console_handler, mock_get_logger):
    #     mock_logger = MagicMock()
    #     mock_logger.hasHandlers.return_value = True
    #     mock_get_logger.return_value = mock_logger

    #     LoggingManager()

    #     self.assertEqual(len(mock_logger.handlers), )

    def test_success_logging(self):
        LoggingManager()
        logger = logging.getLogger()

        with patch.object(logger, "success") as mock_success:
            logger.success("This is a success message")
            mock_success.assert_called_once_with("This is a success message")


if __name__ == "__main__":
    unittest.main()
