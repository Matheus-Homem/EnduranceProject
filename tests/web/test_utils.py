import unittest

from src.web.utils import clean_string, prepare_form_data


class TestUtils(unittest.TestCase):
    def test_clean_string(self):
        self.assertEqual(clean_string("Hello\r\nWorld"), "HelloWorld")
        self.assertEqual(clean_string("NoNewLine"), "NoNewLine")
        self.assertEqual(clean_string("Line1\r\n Line2\r\n"), "Line1 Line2")
        self.assertEqual(clean_string(" "), " ")
        self.assertEqual(clean_string("\r\n"), "")

    def test_prepare_form_data(self):
        data = {
            "name": "John\r\n Doe",
            "email": "\r\njohn.doe@example.com\r\n",
            "address": "123 Main St\r\n",
        }
        expected_output = '{"name": "John Doe", "email": "john.doe@example.com", "address": "123 Main St"}'
        self.assertEqual(prepare_form_data(data), expected_output)

        data_empty = {}
        expected_output_empty = "{}"
        self.assertEqual(prepare_form_data(data_empty), expected_output_empty)

        data_no_newlines = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "address": "456 Elm St",
        }
        expected_output_no_newlines = '{"name": "Jane Doe", "email": "jane.doe@example.com", "address": "456 Elm St"}'
        self.assertEqual(
            prepare_form_data(data_no_newlines), expected_output_no_newlines
        )


if __name__ == "__main__":
    unittest.main()
