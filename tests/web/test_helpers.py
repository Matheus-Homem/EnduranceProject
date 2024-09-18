import sys
import unittest
from datetime import date
from io import StringIO

from src.web.helpers import (
    clean_and_serialize_dict,
    convert_input_date,
    display_debug_message,
    display_error_message,
    display_success_message,
)


class TestHelpers(unittest.TestCase):

    def test_clean_and_serialize_dict(self):
        data = {
            "name": "JOÃO\r\n DANÇARINO",
            "email": "\r\njohn.doe@example.com\r\n",
            "address": "Rua\r\n do\r\n Açaí",
            "number": 123,
        }
        expected_output = '{"name": "JOAO DANCARINO", "email": "john.doe@example.com", "address": "Rua do Acai", "number": "123"}'
        assert clean_and_serialize_dict(data) == expected_output

        data_empty = {}
        expected_output_empty = "{}"
        assert clean_and_serialize_dict(data_empty) == expected_output_empty

    def test_convert_input_date(self):
        date_str = "2023-10-01"
        expected_date = date(2023, 10, 1)
        result = convert_input_date(date_str)
        self.assertEqual(result, expected_date)

    def test_display_success_message(self):
        text = "This is a success message"
        expected_output = f"\033[92mSUCCESS - {text}\033[0m\n"
        captured_output = StringIO()
        sys.stdout = captured_output
        display_success_message(text)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_display_debug_message(self):
        text = "This is a debug message"
        expected_output = f"\033[95mDEBUG - {text}\033[0m\n"
        captured_output = StringIO()
        sys.stdout = captured_output
        display_debug_message(text)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_display_error_message(self):
        text = "This is an error message"
        expected_output = f"\033[91mERROR - {text}\033[0m\n"
        captured_output = StringIO()
        sys.stdout = captured_output
        display_error_message(text)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
