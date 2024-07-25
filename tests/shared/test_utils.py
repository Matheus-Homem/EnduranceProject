import unittest

from src.shared.utils import StringUtils


class TestStringUtils(unittest.TestCase):

    def test_remove_newlines(self):
        self.assertEqual(StringUtils.remove_newlines("Hello\r\nWorld"), "HelloWorld")
        self.assertEqual(StringUtils.remove_newlines("NoNewLine"), "NoNewLine")
        self.assertEqual(
            StringUtils.remove_newlines("Line1\r\n Line2\r\n"), "Line1 Line2"
        )
        self.assertEqual(StringUtils.remove_newlines(" "), " ")
        self.assertEqual(StringUtils.remove_newlines("\r\n"), "")

    def test_remove_special_characters(self):
        cleaned_string = StringUtils.remove_special_characters(
            "áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ"
        )
        self.assertEqual(
            cleaned_string,
            "aaaaeeiooouucAAAAEEIOOOUUC",
        )

    def test_clean_string(self):
        self.assertEqual(
            StringUtils.clean_string("João\r\n Dançarino"), "Joao Dancarino"
        )

    def test_serialize_cleaned_data(self):
        data = {
            "name": "JOAO DANCARINO",
            "email": "john.doe@example.com",
            "address": "Rua do Acai",
            "number": "123",
        }
        expected_output = '{"name": "JOAO DANCARINO", "email": "john.doe@example.com", "address": "Rua do Acai", "number": "123"}'
        self.assertEqual(StringUtils.serialize_dict(data), expected_output)

        data_empty = {}
        expected_output_empty = "{}"
        self.assertEqual(StringUtils.serialize_dict(data_empty), expected_output_empty)


if __name__ == "__main__":
    unittest.main()
