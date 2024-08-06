import unittest

from src.shared.utilities.text import TextUtilities


class TestStringUtils(unittest.TestCase):

    def test_remove_newlines(self):
        self.assertEqual(TextUtilities.remove_newlines("Hello\r\nWorld"), "HelloWorld")
        self.assertEqual(TextUtilities.remove_newlines("NoNewLine"), "NoNewLine")
        self.assertEqual(
            TextUtilities.remove_newlines("Line1\r\n Line2\r\n"), "Line1 Line2"
        )
        self.assertEqual(TextUtilities.remove_newlines(" "), " ")
        self.assertEqual(TextUtilities.remove_newlines("\r\n"), "")

    def test_remove_special_characters(self):
        cleaned_string = TextUtilities.remove_special_characters(
            "áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ"
        )
        self.assertEqual(
            cleaned_string,
            "aaaaeeiooouucAAAAEEIOOOUUC",
        )

    def test_clean_string(self):
        self.assertEqual(
            TextUtilities.clean_string("João\r\n Dançarino"), "Joao Dancarino"
        )

    def test_serialize_dict(self):
        data = {
            "name": "JOAO DANCARINO",
            "email": "john.doe@example.com",
            "address": "Rua do Acai",
            "number": "123",
        }
        expected_output = '{"name": "JOAO DANCARINO", "email": "john.doe@example.com", "address": "Rua do Acai", "number": "123"}'
        self.assertEqual(TextUtilities.serialize_dict(data), expected_output)

        data_empty = {}
        expected_output_empty = "{}"
        self.assertEqual(
            TextUtilities.serialize_dict(data_empty), expected_output_empty
        )


if __name__ == "__main__":
    unittest.main()
