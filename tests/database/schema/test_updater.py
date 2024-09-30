import unittest
from unittest.mock import MagicMock

from src.database.schema.parser import HTMLSchemaParser
from src.database.schema.updater import ColumnNotDefinedError, DatabaseSchemaUpdater
from src.database.tables import MySqlTable


class TestSchemaUpdater(unittest.TestCase):

    def setUp(self):
        self.table = MagicMock(spec=MySqlTable)
        self.table.__tablename__ = "mock_table"
        self.table.schema_encoded = "schema_encoded"
        self.table.schema_version = "schema_version"
        self.table.element_category = "element_category"
        self.table.element_name = "element_name"
        self.parser = MagicMock(spec=HTMLSchemaParser)
        self.updater = DatabaseSchemaUpdater(table=self.table, parser=self.parser)

    def test_column_not_defined_error(self):
        with self.assertRaises(ColumnNotDefinedError):
            self.updater._validate_columns("non_existent_column")

    def test_can_sort_fields(self):
        fields = {0: "date_input", 1: "boolTest", 5: "snackMorning"}
        expected = ["boolTest", "date_input", "snackMorning"]
        result = self.updater._sort_fields(fields)
        self.assertEqual(result, expected)

    def test_can_map_dtypes_to_columns(self):
        fields = {0: "date_input", 1: "boolTest", 5: "ordinalSnackMorning"}
        dtypes = {0: "date", 1: "bool", 5: "ordinal"}
        expected = {"date_input": "date", "boolTest": "bool", "ordinalSnackMorning": "ordinal"}
        result = self.updater._map_dtypes_to_columns(fields, dtypes)
        self.assertEqual(result, expected)

    def test_can_filter_duplicate_fields(self):
        field_mapping = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest", 6: "ordinalTest"}
        dtype_mapping = {0: "date", 1: "bool", 2: "double", 3: "hhmmss", 4: "int", 5: "ordinal", 6: "ordinal"}
        expected_fields = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest"}
        expected_dtypes = {0: "date", 1: "bool", 2: "double", 3: "hhmmss", 4: "int", 5: "ordinal"}
        result_fields, result_dtypes = self.updater._filter_duplicate_fields(field_mapping, dtype_mapping)
        self.assertEqual(result_fields, expected_fields)
        self.assertEqual(result_dtypes, expected_dtypes)

    def test_can_extract_unique_fields(self):
        field_mapping = {0: "date_input", 1: "boolTest", 2: "doubleTest", 3: "hhmmssTest", 4: "intTest", 5: "ordinalTest", 6: "ordinalTest"}
        expected = ["date_input", "boolTest", "doubleTest", "hhmmssTest", "intTest", "ordinalTest"]
        result = self.updater._extract_unique_fields(field_mapping)
        self.assertCountEqual(result, expected)

    def test_if_version_is_defined(self):
        defined_schemas = [
            {"element_category": "category1", "element_name": "element1", "schema_encoded": "encode1", "schema_version": 2},
            {"element_category": "category2", "element_name": "element2", "schema_encoded": "encode2", "schema_version": 3},
        ]
        category = "category1"
        element = "element1"
        current_encode = "encode1"
        result = self.updater._is_version_defined(category, element, current_encode, defined_schemas)
        self.assertTrue(result)

    def test_if_version_is_not_defined(self):
        defined_schemas = [
            {"element_category": "category1", "element_name": "element1", "schema_encoded": "encode1", "schema_version": 2},
            {"element_category": "category2", "element_name": "element2", "schema_encoded": "encode2", "schema_version": 3},
        ]
        category = "category1"
        element = "element1"
        current_encode = "encode2"
        result = self.updater._is_version_defined(category, element, current_encode, defined_schemas)
        self.assertFalse(result)

    def test_can_fetch_next_schema_version(self):
        defined_schemas = [
            {"element_category": "category1", "element_name": "element1", "schema_version": 2},
            {"element_category": "category1", "element_name": "element1", "schema_version": 3},
            {"element_category": "category2", "element_name": "element2", "schema_version": 1},
        ]
        category = "category1"
        element = "element1"
        result = self.updater._fetch_next_schema_version(category, element, defined_schemas)
        self.assertEqual(result, 4)

    def test_can_update_element_schemas(self):
        self.parser.parse_html_files.return_value = {
            "element1": {
                "category": "category1",
                "fields": {0: "date_input", 1: "boolTest", 5: "ordinalTest"},
                "dtypes": {0: "date", 1: "bool", 5: "ordinal"},
            }
        }
        self.table.get_unique_constraint_name.return_value = "unique_constraint"
        self.table.get_schema_encoded.return_value = "encode1"
        self.updater._fetch_next_schema_version = MagicMock(return_value=1)
        self.updater._extract_unique_fields = MagicMock(return_value=["date_input", "boolTest", "ordinalTest"])
        self.updater._filter_duplicate_fields = MagicMock(
            return_value=({0: "date_input", 1: "boolTest", 2: "ordinalTest"}, {0: "date", 1: "bool", 2: "ordinal"})
        )
        self.updater._sort_fields = MagicMock(return_value=["boolTest", "date_input", "ordinalTest"])
        self.updater._map_dtypes_to_columns = MagicMock(return_value={"date_input": "date", "boolTest": "bool", "ordinalTest": "ordinal"})

        executor = MagicMock()
        executor.__enter__.return_value.select.return_value = []
        executor.__enter__.return_value.upsert.return_value = []
        with unittest.mock.patch("src.database.schema.updater.DatabaseExecutorBuilder", return_value=executor):
            self.updater.update_element_schemas()

        self.parser.parse_html_files.assert_called_once_with(directory=self.updater.directory_path)
        self.table.get_schema_encoded.assert_called_once_with(schema_fields=["date_input", "boolTest", "ordinalTest"])
        self.updater._fetch_next_schema_version.assert_called_once_with(category="category1", element="element1", defined_schemas=[])

        executor.__enter__.return_value.upsert.assert_called_once_with(
            table=self.table,
            element_category=None,
            element_name="element1",
            schema_version=1,
            schema_encoded="encode1",
            schema_fields="boolTest,date_input,ordinalTest",
            schema_dtypes='{"date_input": "date", "boolTest": "bool", "ordinalTest": "ordinal"}',
        )


if __name__ == "__main__":
    unittest.main()
