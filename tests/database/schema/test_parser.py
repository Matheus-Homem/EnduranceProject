import unittest
from unittest.mock import MagicMock, mock_open, patch

from os_local import (
    get_absolute_path,
    is_directory,
    join_paths,
    list_directory_contents,
)
from src.database.schema.parser import HTMLParser


class TestHTMLParser(unittest.TestCase):

    def setUp(self):
        self.parser = HTMLParser()

    def test_list_subfolders(self):
        test_path = get_absolute_path("src/")
        subfolders = self.parser._list_subfolders(test_path)
        correct_subfolders = [subfolder for subfolder in list_directory_contents(test_path) if is_directory(join_paths(test_path, subfolder))]

        self.assertEqual(subfolders, correct_subfolders)

    def test_list_html_files(self):
        test_path = get_absolute_path("src/")
        html_files = self.parser._list_html_files(test_path)
        correct_html_files = [filename for filename in list_directory_contents(test_path) if filename.endswith(".html")]

        self.assertEqual(html_files, correct_html_files)

    def test_extract_fields(self):
        mock_input_tags = [
            MagicMock(get=lambda attr: "field1" if attr == "name" else "text"),
            MagicMock(get=lambda attr: "field2" if attr == "name" else "number"),
        ]

        fields = self.parser._extract_fields(mock_input_tags, "name")
        self.assertEqual(fields, {0: "field1", 1: "field2"})

    def test_process_html_file(self):
        mock_open_file = mock_open(read_data="<input name='field1' dtype='text'><input name='field2' dtype='number'>")
        with patch("builtins.open", mock_open_file):
            filepath = "src/web/templates/core/test.html"
            subfolder = "core"
            parsed_data = self.parser._process_html_file(filepath, subfolder)

            self.assertEqual(parsed_data, {"category": subfolder, "fields": {0: "field1", 1: "field2"}, "dtypes": {0: "text", 1: "number"}})

    def test_parse_invalid_directory(self):
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_html_files("src/web/templates/invalid")

    def test_get_keynames(self):
        self.assertEqual(self.parser.get_category_keyname(), "category")
        self.assertEqual(self.parser.get_field_keyname(), "fields")
        self.assertEqual(self.parser.get_dtype_keyname(), "dtypes")

    def test_parse_html_file(self):
        parsed_data = self.parser.parse_html_files("src/web/templates/core")
        test_data = parsed_data.get("test")
        expected_test_data = {
            "category": "_template",
            "fields": {
                0: "date_input",
                1: "boolTest",
                2: "doubleTest",
                3: "hhmmssTest",
                4: "intTest",
                5: "ordinalTest",
                6: "ordinalTest",
                7: "ordinalTest",
                8: "ordinalTest",
                9: "timestampTest",
                10: "hhmmTest",
                11: "stringTest",
            },
            "dtypes": {
                0: "date",
                1: "bool",
                2: "double",
                3: "hhmmss",
                4: "int",
                5: "ordinal",
                6: "ordinal",
                7: "ordinal",
                8: "ordinal",
                9: "timestamp",
                10: "hhmm",
                11: "string",
            },
        }

        self.assertEqual(test_data, expected_test_data)


if __name__ == "__main__":
    unittest.main()
