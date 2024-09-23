from typing import Dict, List

from bs4 import BeautifulSoup

from os_local import (
    get_absolute_path,
    is_directory,
    is_path_valid,
    join_paths,
    list_directory_contents,
)


class HTMLParser:

    def _list_subfolders(self, abs_directory: str) -> List[str]:
        return [subfolder for subfolder in list_directory_contents(abs_directory) if is_directory(join_paths(abs_directory, subfolder))]

    def _list_html_files(self, subfolder_path: str) -> List[str]:
        return [filename for filename in list_directory_contents(subfolder_path) if filename.endswith(".html")]

    def _extract_fields(self, inputs: List[BeautifulSoup], attribute: str) -> Dict[int, str]:
        return {index: input_tag.get(attribute) for index, input_tag in enumerate(inputs) if input_tag.get(attribute)}

    def _process_html_file(self, filepath: str, subfolder: str) -> Dict[str, Dict[int, str]]:
        with open(filepath, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            inputs = soup.find_all(["input", "textarea"])
            return {
                "category": subfolder,
                "fields": self._extract_fields(inputs, "name"),
                "dtypes": self._extract_fields(inputs, "dtype"),
            }

    def parse_html_files(self, directory: str) -> Dict[str, Dict[str, Dict[int, str]]]:
        parsed_element_mapping = {}

        abs_directory = get_absolute_path(directory)
        if not is_path_valid(abs_directory):
            raise FileNotFoundError(f"The specified directory does not exist: {abs_directory}")

        subfolders = self._list_subfolders(abs_directory)

        for subfolder in subfolders:
            subfolder_path = join_paths(abs_directory, subfolder)
            html_files = self._list_html_files(subfolder_path)
            for filename in html_files:
                filepath = join_paths(subfolder_path, filename)
                element = filename[:-5]
                parsed_element_mapping[element] = self._process_html_file(filepath, subfolder)

        return parsed_element_mapping
