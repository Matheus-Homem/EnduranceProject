import unittest
import logging
import os
from unittest.mock import patch, MagicMock
from src.shared.logger import CustomFormatter, LoggingManager

class TestCustomFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = CustomFormatter('%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s', 'TestClass')

    def test_format_initialization(self):
        self.assertEqual(self.formatter.class_name, 'TestClass')

    def test_format_method(self):
        record = logging.LogRecord(
            name='test',
            level=logging.DEBUG,
            pathname='/path/to/src/file.py',
            lineno=10,
            msg='Test message',
            args=(),
            exc_info=None
        )
        formatted_message = self.formatter.format(record)
        self.assertIn('TestClass', formatted_message)
        self.assertIn('src/file.py', formatted_message)

# class TestLogger(unittest.TestCase):
#     @patch('src.shared.logger.inspect.stack')  # Adjusted import path
#     @patch('src.shared.logger.inspect.getframeinfo')  # Adjusted import path
#     def test_singleton_behavior(self, mock_getframeinfo, mock_stack):
#         mock_stack.return_value = [MagicMock()]  # Ensure this returns a list with at least one item
#         mock_getframeinfo.return_value = MagicMock(filename='test_file.py', function='test_function')

#         logger1 = Logger(class_name='TestClass')
#         logger2 = Logger(class_name='TestClass')
#         self.assertIs(logger1, logger2)

#     @patch('src.shared.logger.inspect.stack')  # Adjusted import path
#     @patch('src.shared.logger.inspect.getframeinfo')  # Adjusted import path
#     def test_logger_initialization(self, mock_getframeinfo, mock_stack):
#         mock_stack.return_value = [MagicMock()]  # Ensure this returns a list with at least one item
#         mock_getframeinfo.return_value = MagicMock(filename='test_file.py', function='test_function')

#         logger_instance = Logger(class_name='TestClass')
#         logger = logger_instance.get_logger()
#         self.assertIsInstance(logger, logging.Logger)

#     @patch('src.shared.logger.os.makedirs')  # Adjusted import path
#     @patch('src.shared.logger.logging.FileHandler')  # Adjusted import path
#     @patch('src.shared.logger.inspect.stack')  # Adjusted import path
#     @patch('src.shared.logger.inspect.getframeinfo')  # Adjusted import path
#     def test_file_handler_creation(self, mock_getframeinfo, mock_stack, mock_file_handler, mock_makedirs):
#         mock_stack.return_value = [MagicMock()]  # Ensure this returns a list with at least one item
#         mock_getframeinfo.return_value = MagicMock(filename='test_file.py', function='test_function')

#         logger_instance = Logger(class_name='TestClass')
#         logger = logger_instance.get_logger()
#         mock_file_handler.assert_called_once()

#     @patch('src.shared.logger.colorlog.StreamHandler')  # Adjusted import path
#     @patch('src.shared.logger.inspect.stack')  # Adjusted import path
#     @patch('src.shared.logger.inspect.getframeinfo')  # Adjusted import path
#     def test_console_handler_creation(self, mock_getframeinfo, mock_stack, mock_stream_handler):
#         mock_stack.return_value = [MagicMock()]  # Ensure this returns a list with at least one item
#         mock_getframeinfo.return_value = MagicMock(filename='test_file.py', function='test_function')

#         logger_instance = Logger(class_name='TestClass')
#         logger = logger_instance.get_logger()
#         mock_stream_handler.assert_called_once()

#     @patch('src.shared.logger.inspect.stack')  # Adjusted import path
#     @patch('src.shared.logger.inspect.getframeinfo')  # Adjusted import path
#     def test_get_logger(self, mock_getframeinfo, mock_stack):
#         mock_stack.return_value = [MagicMock()]  # Ensure this returns a list with at least one item
#         mock_getframeinfo.return_value = MagicMock(filename='test_file.py', function='test_function')

#         logger_instance = Logger(class_name='TestClass')
#         logger = logger_instance.get_logger()
#         self.assertIsInstance(logger, logging.Logger)

if __name__ == '__main__':
    unittest.main()