from typing import Any, Dict, List, Tuple

from src.shared.credentials import PRD
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import ElementSchemas, MySqlTable
from src.shared.logging.adapters import LoggingPrinter
from src.shared.utils import DictUtils
from src.web.schema.parser import HTMLParser


class ColumnNotDefinedError(Exception):
    pass


class SchemaUpdater(LoggingPrinter):

    def __init__(
        self,
        table: MySqlTable = ElementSchemas,
        parser: HTMLParser = HTMLParser(),
        encoded_column: str = "schema_encoded",
        version_column: str = "schema_version",
        category_column: str = "element_category",
        element_column: str = "element_name",
    ):
        super().__init__(class_name=self.__class__.__name__)
        self.table = table
        self.parser = parser
        self.directory_path = "src/web/templates/core"
        self.encoded_column = encoded_column
        self.version_column = version_column
        self.category_column = category_column
        self.element_column = element_column
        self._validate_columns(columns=[self.encoded_column, self.version_column, self.category_column, self.element_column])

    def _validate_columns(self, columns: List[str]):
        for column in columns:
            if not hasattr(self.table, column):
                raise ColumnNotDefinedError(f"Column '{column}' is not defined in the table '{self.table.__tablename__}'.")

    def _extract_unique_fields(self, field_mapping: Dict[int, str]) -> List[str]:
        return list(set(field_mapping.values()))

    def _filter_duplicate_fields(
        self,
        field_mapping: Dict[int, str],
        dtype_mapping: Dict[int, str],
    ) -> Tuple[Dict[int, str], Dict[int, str]]:
        unique_fields, unique_dtypes = {}, {}
        seen_values = set()
        for k, v in field_mapping.items():
            if v not in seen_values:
                seen_values.add(v)
                unique_fields[k] = v
                unique_dtypes[k] = dtype_mapping[k]
        return unique_fields, unique_dtypes

    def _reenumerate_fields(self, fields: Dict[int, str]) -> Dict[int, str]:
        return {new_idx: value for new_idx, (old_idx, value) in enumerate(fields.items())}

    def _reenumerate_dtypes(self, dtypes: Dict[int, str]) -> Dict[int, str]:
        return {new_idx: dtypes[old_idx] for new_idx, (old_idx, value) in enumerate(dtypes.items())}

    def _is_version_defined(
        self,
        category: str,
        element: str,
        current_encode: str,
        defined_schemas: List[Dict[str, Any]],
    ) -> bool:
        for schema in defined_schemas:
            if (
                schema.get(self.category_column) == category
                and schema.get(self.element_column) == element
                and schema.get(self.encoded_column) == current_encode
            ):
                return True
        return False

    def _fetch_next_schema_version(
        self,
        category: str,
        element: str,
        defined_schemas: List[Dict[str, Any]],
    ) -> int:
        schema_versions = [
            schema.get(self.version_column)
            for schema in defined_schemas
            if schema.get(self.category_column) == category and schema.get(self.element_column) == element
        ]
        latest_version = max(schema_versions, default=0)
        return latest_version + 1

    def update_element_schemas(self):
        self.logger.info("Starting schema update process")

        skipped_schemas = []
        updated_schemas = []

        parsed_html_elements = self.parser.parse_html_files(directory=self.directory_path)
        category_keyname = self.parser.get_category_keyname()
        field_keyname = self.parser.get_field_keyname()
        dtype_keyname = self.parser.get_dtype_keyname()

        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            existing_table = executor.select(self.table)
            for element, v in parsed_html_elements.items():

                category = v.get(category_keyname)
                field_mapping = v.get(field_keyname)
                dtype_mapping = v.get(dtype_keyname)

                unique_columns = self._extract_unique_fields(field_mapping=field_mapping)
                unique_fields, unique_dtypes = self._filter_duplicate_fields(field_mapping=field_mapping, dtype_mapping=dtype_mapping)

                renumbered_fields = self._reenumerate_fields(fields=unique_fields)
                renumbered_dtypes = self._reenumerate_dtypes(dtypes=unique_dtypes)

                schema_encoded = self.table.get_schema_encoded(schema_fields=unique_columns)

                if self._is_version_defined(
                    category=v.get("category"),
                    element=element,
                    current_encode=schema_encoded,
                    defined_schemas=existing_table,
                ):
                    skipped_schemas.append(element.upper() if element else element)
                    continue
                else:
                    updated_schemas.append(element.upper() if element else element)
                    schema_version = self._fetch_next_schema_version(
                        category=v.get("category"),
                        element=element,
                        defined_schemas=existing_table,
                    )

                    executor.upsert(
                        table=self.table,
                        element_category=category,
                        element_name=element,
                        schema_version=schema_version,
                        schema_encoded=schema_encoded,
                        schema_fields=DictUtils.serialize_dict(data=renumbered_fields),
                        schema_dtypes=DictUtils.serialize_dict(data=renumbered_dtypes),
                    )
        self.logger.success("Schema update process completed")
        self.logger.info(f"Skipped schemas: {skipped_schemas}")
        self.logger.info(f"Updated schemas: {updated_schemas}")