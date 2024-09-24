import unittest
from unittest.mock import MagicMock

from src.shared.database.tables import MySqlTable
from src.web.schema.parser import HTMLParser
from src.web.schema.updater import ColumnNotDefinedError, SchemaUpdater


class TestSchemaUpdater(unittest.TestCase):

    def setUp(self):
        self.table = MagicMock(spec=MySqlTable)
        self.table.__tablename__ = "mock_table"
        self.table.schema_hash = "schema_hash"
        self.table.schema_version = "schema_version"
        self.table.element_category = "element_category"
        self.table.element_name = "element_name"
        self.parser = MagicMock(spec=HTMLParser)
        self.updater = SchemaUpdater(table=self.table, parser=self.parser)

    def test_column_not_defined_error(self):
        with self.assertRaises(ColumnNotDefinedError):
            self.updater._validate_columns("non_existent_column")

    def test_reenumerate_fields(self):
        fields = {0: "date_input", 1: "boolTest", 5: "snackMorning"}
        expected = {0: "date_input", 1: "boolTest", 2: "snackMorning"}
        result = self.updater._reenumerate_fields(fields)
        self.assertEqual(result, expected)

    def test_reenumerate_dtypes(self):
        dtypes = {0: "date", 1: "bool", 5: "ordinal"}
        expected = {0: "date", 1: "bool", 2: "ordinal"}
        result = self.updater._reenumerate_dtypes(dtypes)
        self.assertEqual(result, expected)

    def test_filter_duplicate_fields(self):
        field_mapping = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest", 6: "ordinalTest"}
        dtype_mapping = {0: "date", 1: "bool", 2: "double", 3: "hhmmss", 4: "int", 5: "ordinal", 6: "ordinal"}
        expected_fields = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest"}
        expected_dtypes = {0: "date", 1: "bool", 2: "double", 3: "hhmmss", 4: "int", 5: "ordinal"}
        result_fields, result_dtypes = self.updater._filter_duplicate_fields(field_mapping, dtype_mapping)
        self.assertEqual(result_fields, expected_fields)
        self.assertEqual(result_dtypes, expected_dtypes)

    def test_extract_unique_fields(self):
        field_mapping = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest", 6: "ordinalTest"}
        expected = ["date_input", "boolTest", "doubleTest", "hhmmssTest", "intTest", "ordinalTest"]
        result = self.updater._extract_unique_fields(field_mapping)
        self.assertCountEqual(result, expected)

    def test_is_version_defined(self):
        defined_schemas = [
            {"element_category": "category1", "element_name": "element1", "schema_hash": "hash1", "schema_version": 2},
            {"element_category": "category2", "element_name": "element2", "schema_hash": "hash2", "schema_version": 3},
        ]
        category = "category1"
        element = "element1"
        current_hash = "hash1"
        result = self.updater._is_version_defined(category, element, current_hash, defined_schemas)
        self.assertTrue(result)

    def test_is_version_not_defined(self):
        defined_schemas = [
            {"element_category": "category1", "element_name": "element1", "schema_hash": "hash1", "schema_version": 2},
            {"element_category": "category2", "element_name": "element2", "schema_hash": "hash2", "schema_version": 3},
        ]
        category = "category1"
        element = "element1"
        current_hash = "hash2"
        result = self.updater._is_version_defined(category, element, current_hash, defined_schemas)
        self.assertFalse(result)

    def test_fetch_next_schema_version(self):
        defined_schemas = [
            {"element_category": "category1", "element_name": "element1", "schema_version": 2},
            {"element_category": "category1", "element_name": "element1", "schema_version": 3},
            {"element_category": "category2", "element_name": "element2", "schema_version": 1},
        ]
        category = "category1"
        element = "element1"
        result = self.updater._fetch_next_schema_version(category, element, defined_schemas)
        self.assertEqual(result, 4)

    def test_update_element_schemas(self):
        self.parser.parse_html_files.return_value = {
            "element1": {
                "category": "category1",
                "fields": {0: "date_input", 1: "boolTest", 5: "snackMorning"},
                "dtypes": {0: "date", 1: "bool", 5: "ordinal"},
            }
        }
        self.table.get_unique_constraint_name.return_value = "unique_constraint"
        self.table.get_schema_hash.return_value = "hash1"
        self.updater._fetch_next_schema_version = MagicMock(return_value=1)
        self.updater._extract_unique_fields = MagicMock(return_value=["date_input", "boolTest", "snackMorning"])
        self.updater._filter_duplicate_fields = MagicMock(
            return_value=({0: "date_input", 1: "boolTest", 2: "snackMorning"}, {0: "date", 1: "bool", 2: "ordinal"})
        )
        self.updater._reenumerate_fields = MagicMock(return_value={0: "date_input", 1: "boolTest", 2: "snackMorning"})
        self.updater._reenumerate_dtypes = MagicMock(return_value={0: "date", 1: "bool", 2: "ordinal"})

        executor = MagicMock()
        executor.__enter__.return_value.select.return_value = []
        executor.__enter__.return_value.upsert.return_value = []
        with unittest.mock.patch("src.web.schema.updater.DatabaseExecutorBuilder", return_value=executor):
            self.updater.update_element_schemas()

        self.parser.parse_html_files.assert_called_once_with(directory=self.updater.directory_path)
        self.table.get_unique_constraint_name.assert_called_once()
        self.table.get_schema_hash.assert_called_once_with(schema_fields=["date_input", "boolTest", "snackMorning"])
        self.updater._fetch_next_schema_version.assert_called_once_with(category="category1", element="element1", defined_schemas=[])

        executor.__enter__.return_value.upsert.assert_called_once_with(
            table=self.table,
            uc_name="unique_constraint",
            element_category=None,
            element_name="element1",
            schema_version=1,
            schema_hash="hash1",
            schema_fields='{"0": "date_input", "1": "boolTest", "2": "snackMorning"}',
            schema_dtypes='{"0": "date", "1": "bool", "2": "ordinal"}',
        )


if __name__ == "__main__":
    unittest.main()
