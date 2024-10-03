import logging
import unittest
from unittest.mock import MagicMock, patch

from src.shared.logger import SUCCESS_LEVEL_NUM, LoggerInitializer


class TestLoggingManager(unittest.TestCase):

    @patch("src.shared.logger.colorlog.StreamHandler")
    @patch("src.shared.logger.colorlog.ColoredFormatter")
    def test_add_console_handler(self, mock_colored_formatter, mock_stream_handler):
        LoggerInitializer()

        mock_colored_formatter.assert_called_once_with(
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

        mock_stream_handler_instance = mock_stream_handler.return_value
        mock_stream_handler_instance.setFormatter.assert_called_once_with(mock_colored_formatter.return_value)

    @patch("src.shared.logger.logging.getLogger")
    @patch.object(LoggerInitializer, "_add_console_handler")
    def test_initialize_logger(self, mock_add_console_handler, mock_get_logger):
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = False
        mock_get_logger.return_value = mock_logger

        LoggerInitializer()

        mock_add_console_handler.assert_called_once_with(mock_logger)

    def test_success_logging(self):
        LoggerInitializer()
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

    @patch("src.shared.logger.logging.getLogger")
    def test_raise_error_and_log(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with self.assertRaises(ValueError) as context:
            LoggerInitializer.raise_error_and_log(mock_logger, "Test error message")

        mock_logger.error.assert_called_once_with("Test error message")
        self.assertEqual(str(context.exception), "Test error message")

    @patch("src.shared.logger.logging.getLogger")
    def test_reset_logger(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_logger.handlers = [MagicMock(), MagicMock(), MagicMock()]
        mock_get_logger.return_value = mock_logger

        LoggerInitializer.reset_logger()

        self.assertTrue(mock_logger.removeHandler.called)
        self.assertEqual(mock_logger.removeHandler.call_count, len(mock_logger.handlers))

    @patch("src.shared.logger.join_paths", return_value="src/")
    @patch("src.shared.logger.colorlog.ColoredFormatter.format", return_value="formatted message")
    def test_custom_format(self, mock_format, mock_join_paths):
        logger_initializer = LoggerInitializer()
        formatter = logger_initializer.formatter

        record = MagicMock()
        record.pathname = "src/shared/logger.py"
        record.name = "test_logger"
        record.funcName = "test_func"

        result = logger_initializer._custom_format(record)
        self.assertEqual(result, "formatted message")
        mock_format.assert_called_once_with(record)

    @patch("src.shared.logger.join_paths", return_value="src/")
    @patch("src.shared.logger.colorlog.ColoredFormatter.format", return_value="")
    def test_filter_empty_messages(self, mock_format, mock_join_paths):
        logger_initializer = LoggerInitializer()
        formatter = logger_initializer.formatter

        record = MagicMock()
        record.pathname = "src/shared/logger.py"
        record.name = "test_logger"
        record.funcName = "test_func"

        result = logger_initializer._filter_empty_messages(record)
        self.assertFalse(result)
        mock_format.assert_called_once_with(record)


if __name__ == "__main__":
    unittest.main()
