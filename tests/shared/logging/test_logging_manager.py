import logging
import unittest
from unittest.mock import MagicMock, patch

from src.shared.logging.manager import SUCCESS_LEVEL_NUM, LoggingManager


class TestLoggingManager(unittest.TestCase):

    @patch("src.shared.logging.manager.colorlog.StreamHandler")
    @patch("src.shared.logging.manager.CustomColoredFormatter")
    def test_add_console_handler(self, mock_colored_formatter, mock_stream_handler):

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

    @patch("src.shared.logging.manager.logging.getLogger")
    @patch.object(LoggingManager, "_add_console_handler")
    def test_initialize_logger(self, mock_add_console_handler, mock_get_logger):
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = False
        mock_get_logger.return_value = mock_logger

        LoggingManager()

        mock_add_console_handler.assert_called_once_with(mock_logger)

    def test_success_logging(self):
        LoggingManager()
        logger = logging.getLogger()

        with patch.object(logger, "success") as mock_success:
            logger.success("This is a success message")
            mock_success.assert_called_once_with("This is a success message")

    def test_success_level(self):
        self.assertEqual(logging.getLevelName(SUCCESS_LEVEL_NUM), "SUCCESS")

    def test_success_method(self):
        logger = logging.getLogger()
        with patch.object(logger, "_log") as mock_log:
            logger.success("Test success message")
            mock_log.assert_called_once_with(SUCCESS_LEVEL_NUM, "Test success message", ())


if __name__ == "__main__":
    unittest.main()
