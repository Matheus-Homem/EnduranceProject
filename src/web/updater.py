import os
from typing import Dict, List

from bs4 import BeautifulSoup

from src.shared.credentials import PRD
from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import ElementSchemas
from src.shared.utils import HashUtils, StringUtils


class ElementSchemasController:

    def __init__(self):
        self.table = ElementSchemas

    def _read_html_files(self, directory: str) -> Dict[str, Dict[str, List[str]]]:
        input_names = {}

        abs_directory = os.path.abspath(directory)

        if not os.path.exists(abs_directory):
            raise FileNotFoundError(f"The specified directory does not exist: {abs_directory}")

        subfolders = os.listdir(abs_directory)
        for subfolder in subfolders:
            subfolder_path = os.path.join(abs_directory, subfolder)
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".html"):
                    filepath = os.path.join(subfolder_path, filename)
                    with open(filepath, "r", encoding="utf-8") as file:
                        soup = BeautifulSoup(file, "html.parser")
                        inputs = soup.find_all(["input", "textarea"])
                        input_names[filename[:-5]] = {
                            "category": subfolder,
                            "fields": sorted({input_tag.get("name") for input_tag in inputs if input_tag.get("name")}),
                        }

        return input_names

    def _generate_schema_version(self, fields: List[str]) -> int:
        pass

    def _generate_schema_fields(self, fields: List[str]) -> str:
        pass

    def _generate_schema_dtypes(self, fields: List[str]) -> str:
        pass

    def update_element_schemas(self):
        input_names_dict = self._read_html_files("src/web/templates/core")
        table_uc = self.table.get_unique_constraint_name()

        with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
            existing_table = executor.select(self.table)
            for element, v in input_names_dict.items():
                category = v.get("category")
                fields = v.get("fields")

                executor.upsert(
                    table=self.table,
                    uc_name=table_uc,
                    element_category=category,
                    element_name=element,
                    schema_version=self._generate_schema_version(fields=fields),
                    schema_hash=self.table.get_schema_hash(schema_fields=fields),
                    schema_fields=self._generate_schema_fields(fields=fields),
                    schema_dtypes=self._generate_schema_dtypes(fields=fields),
                )
