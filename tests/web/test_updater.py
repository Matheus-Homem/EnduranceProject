import unittest
from unittest.mock import MagicMock

from src.shared.database.tables import MySqlTable
from src.web.parser import HTMLParser
from src.web.updater import ElementSchemasController


class TestElementSchemasController(unittest.TestCase):

    def setUp(self):
        self.table = MagicMock(spec=MySqlTable)
        self.parser = MagicMock(spec=HTMLParser)
        self.controller = ElementSchemasController(table=self.table, parser=self.parser)

    def test_reenumerate_fields(self):
        fields = {0: "date_input", 1: "boolTest", 5: "snackMorning"}
        expected = {0: "date_input", 1: "boolTest", 2: "snackMorning"}
        result = self.controller._reenumerate_fields(fields)
        self.assertEqual(result, expected)

    def test_reenumerate_dtypes(self):
        dtypes = {0: "date", 1: "bool", 5: "ordinal"}
        expected = {0: "date", 1: "bool", 2: "ordinal"}
        result = self.controller._reenumerate_dtypes(dtypes)
        self.assertEqual(result, expected)

    def test_filter_duplicate_fields(self):
        field_mapping = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest", 6: "ordinalTest"}
        dtype_mapping = {0: "date", 1: "bool", 2: "double", 3: "hhmmss", 4: "int", 5: "ordinal", 6: "ordinal"}
        expected_fields = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest"}
        expected_dtypes = {0: "date", 1: "bool", 2: "double", 3: "hhmmss", 4: "int", 5: "ordinal"}
        result_fields, result_dtypes = self.controller._filter_duplicate_fields(field_mapping, dtype_mapping)
        self.assertEqual(result_fields, expected_fields)
        self.assertEqual(result_dtypes, expected_dtypes)

    def test_get_unique_columns(self):
        field_mapping = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest", 6: "ordinalTest"}
        expected = ["date_input", "boolTest", "doubleTest", "hhmmssTest", "intTest", "ordinalTest"]
        result = self.controller._get_unique_columns(field_mapping)
        self.assertCountEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
