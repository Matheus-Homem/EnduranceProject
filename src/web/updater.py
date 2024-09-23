from typing import Dict, List, Tuple

from src.shared.credentials import PRD
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import ElementSchemas, MySqlTable
from src.shared.utils import DictUtils
from src.web.parser import HTMLParser


class ElementSchemasController:

    def __init__(self, table: MySqlTable = ElementSchemas(), parser: HTMLParser = HTMLParser()):
        self.table = table
        self.parser = parser

    def _generate_schema_version(self, fields: List[str]) -> int:
        pass

    def _reenumerate_fields(self, fields: Dict[int, str]) -> Dict[int, str]:
        return {new_idx: value for new_idx, (old_idx, value) in enumerate(fields.items())}

    def _reenumerate_dtypes(self, dtypes: Dict[int, str]) -> Dict[int, str]:
        return {new_idx: dtypes[old_idx] for new_idx, (old_idx, value) in enumerate(dtypes.items())}

    def _filter_duplicate_fields(self, field_mapping: Dict[int, str], dtype_mapping: Dict[int, str]) -> Tuple[Dict[int, str], Dict[int, str]]:
        unique_fields, unique_dtypes = {}, {}
        seen_values = set()
        for k, v in field_mapping.items():
            if v not in seen_values:
                seen_values.add(v)
                unique_fields[k] = v
                unique_dtypes[k] = dtype_mapping[k]
        return unique_fields, unique_dtypes

    def _get_unique_columns(self, field_mapping: Dict[int, str]) -> List[str]:
        return list(set(field_mapping.values()))

    def update_element_schemas(self):
        parsed_html_elements = self.parser.parse_html_files(directory="src/web/templates/core")
        table_uc = self.table.get_unique_constraint_name()

        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            existing_table = executor.select(self.table)
            for element, v in parsed_html_elements.items():

                category = v.get("category")
                field_mapping = v.get("fields")
                dtype_mapping = v.get("dtypes")

                unique_columns = self._get_unique_columns(field_mapping=field_mapping)
                unique_fields, unique_dtypes = self._filter_duplicate_fields(field_mapping=field_mapping, dtype_mapping=dtype_mapping)
                renumbered_fields = self._reenumerate_fields(fields=unique_fields)
                renumbered_dtypes = self._reenumerate_dtypes(dtypes=unique_dtypes)

                executor.upsert(
                    table=self.table,
                    uc_name=table_uc,
                    element_category=category,
                    element_name=element,
                    schema_version=self._generate_schema_version(fields=field_mapping),
                    schema_hash=self.table.get_schema_hash(schema_fields=unique_columns),
                    schema_fields=DictUtils.clean_and_serialize_dict(input_dict=renumbered_fields),
                    schema_dtypes=DictUtils.clean_and_serialize_dict(input_dict=renumbered_dtypes),
                )
