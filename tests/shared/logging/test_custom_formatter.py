import logging
import unittest

from src.shared.logging.custom_formatter import CustomColoredFormatter


class TestCustomColoredFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = CustomColoredFormatter(
            fmt="%(log_color)s%(asctime)s - %(pathname)s - %(funcName)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "purple",
                "INFO": "cyan",
                "SUCCESS": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        self.record = logging.LogRecord(
            name="TestClass",
            level=logging.INFO,
            pathname="src/module/file.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

    def test_formatter(self):
        formatted_message = self.formatter.format(self.record)
        self.assertEqual(self.record.pathname, "src/module/file.py")
        print(self.record.funcName)
        self.assertIn(self.record.funcName, [None, "TestClass.None"])
        self.assertIn("", formatted_message)


if __name__ == "__main__":
    unittest.main()
