import unittest

from src.web.updater import ElementSchemasController


class TestElementSchemasController(unittest.TestCase):
    def test_read_html_files(self):
        directory = "src/web/templates/core"
        controller = ElementSchemasController()

        # Act
        result = controller._read_html_files(directory)

        print(list(result.keys()))
        assert result.get("alchemist").get("fields") == [
            "bool_anger",
            "bool_anxiety",
            "bool_disheartenment",
            "bool_fear",
            "bool_frustration",
            "bool_sadness",
            "date_input",
            "string_vent",
        ]

    def test_update_element_schemas(self):
        controller = ElementSchemasController()

        # Act
        result = controller.update_element_schemas()

        assert result == None


if __name__ == "__main__":
    unittest.main()
