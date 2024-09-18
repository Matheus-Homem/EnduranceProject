import unittest
from unittest.mock import MagicMock, patch

from src.shared.logging.adapters import (
    LoggingPrinter,
    raise_error_and_log,
    reset_logger,
)
from src.shared.logging.manager import LoggingManager


class TestLoggingPrinter(unittest.TestCase):

    @patch.object(LoggingManager, "__init__", lambda x: None)
    def test_logging_printer_initialization(self):
        class_name = "TestClass"
        printer = LoggingPrinter(class_name)
        self.assertEqual(printer.logger.name, class_name)


class TestRaiseErrorAndLog(unittest.TestCase):

    def test_raise_error_and_log(self):
        logger = MagicMock()
        error_message = "This is an error message"

        with self.assertRaises(ValueError) as context:
            raise_error_and_log(logger, error_message)

        logger.error.assert_called_once_with(error_message)
        self.assertEqual(str(context.exception), error_message)


class TestResetLogger(unittest.TestCase):

    @patch("src.shared.logging.adapters.logging.getLogger")
    def test_reset_logger(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        handler1 = MagicMock()
        handler2 = MagicMock()
        mock_logger.handlers = [handler1, handler2]

        reset_logger()

        mock_logger.removeHandler.assert_any_call(handler1)
        mock_logger.removeHandler.assert_any_call(handler2)
        self.assertEqual(mock_logger.removeHandler.call_count, 2)


if __name__ == "__main__":
    unittest.main()
