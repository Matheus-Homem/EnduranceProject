from src.shared.database.builder import DatabaseExecutorBuilder
from src.shared.database.tables import ElementSchemas, MySqlTable
from src.shared.utils import HashUtils, StringUtils
import os
from bs4 import BeautifulSoup
from typing import Dict, List

class ElementSchemasController:

    def __init__(self):
        pass

    def read_html_files(self, directory:str) -> Dict[str, Dict[str, List[str]]]:
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
                    with open(filepath, 'r', encoding='utf-8') as file:
                        soup = BeautifulSoup(file, 'html.parser')
                        inputs = soup.find_all(['input', 'textarea'])
                        input_names[filename[:-5]] = {"category": subfolder, "fields" : sorted({input_tag.get('name') for input_tag in inputs if input_tag.get('name')})}

        return input_names
    
    def update_element_schemas(self, table: ElementSchemas = ElementSchemas):
        input_names_dict = self.read_html_files('src/web/templates/core')
        table_uc = table.get_unique_constraint_name()


        with DatabaseExecutorBuilder(use_production_db=False) as executor:
            for element, v in input_names_dict.items():
                category = v.get("category")
                fields = v.get("fields")       
            
                executor.upsert(
                    table=table,
                    uc_name=table_uc,
                    element_category=category,
                    element_name=element,
                    schema_version=HashUtils.hash_list(fields),
                    schema_definition=StringUtils.convert_list_to_string(fields),
                )