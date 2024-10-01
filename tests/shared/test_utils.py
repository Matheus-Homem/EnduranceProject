import base64
import hashlib
import unittest
from datetime import date, datetime

import pytz

from src.shared.utils import (
    DateUtils,
    DictUtils,
    EncodingUtils,
    HashUtils,
    StringUtils,
    ValidationUtils,
)


class TestStringUtils(unittest.TestCase):

    def test_remove_newlines(self):
        self.assertEqual(StringUtils.remove_linebreaks("Hello\r\nWorld"), "HelloWorld")
        self.assertEqual(StringUtils.remove_linebreaks("NoNewLine"), "NoNewLine")
        self.assertEqual(StringUtils.remove_linebreaks("Line1\r\n Line2\r\n"), "Line1 Line2")
        self.assertEqual(StringUtils.remove_linebreaks(" "), " ")
        self.assertEqual(StringUtils.remove_linebreaks("\r\n"), "")

    def test_remove_special_characters(self):
        cleaned_string = StringUtils.remove_special_characters("áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ")
        self.assertEqual(
            cleaned_string,
            "aaaaeeiooouucAAAAEEIOOOUUC",
        )

    def test_clean_string(self):
        self.assertEqual(StringUtils.clean_string("João\r\n Dançarino"), "Joao Dancarino")


class TestDictUtils(unittest.TestCase):

    def test_serialize_dict(self):
        data = {
            "name": "JOAO DANCARINO",
            "email": "john.doe@example.com",
            "address": "Rua do Acai",
            "number": "123",
        }
        expected_output = '{"name": "JOAO DANCARINO", "email": "john.doe@example.com", "address": "Rua do Acai", "number": "123"}'
        self.assertEqual(DictUtils.serialize_dict(data), expected_output)

        data_empty = {}
        expected_output_empty = "{}"
        self.assertEqual(DictUtils.serialize_dict(data_empty), expected_output_empty)

    def test_clean_and_serialize_dict(self):
        input_dict = {"Café\n": "Morn\ning"}
        expected_output = '{"Cafe": "Morning"}'
        self.assertEqual(DictUtils.clean_and_serialize_dict(input_dict), expected_output)

    def test_deserialize_dict(self):
        self.assertEqual(DictUtils.deserialize_dict('{"key": "value"}'), {"key": "value"})


class TestValidationUtils(unittest.TestCase):

    def test_is_valid_password(self):
        self.assertTrue(ValidationUtils.is_valid_password("Password1!"))
        self.assertFalse(ValidationUtils.is_valid_password("short"))
        self.assertFalse(ValidationUtils.is_valid_password("n0specialchar"))
        self.assertFalse(ValidationUtils.is_valid_password("NoNumber!"))

    def test_is_valid_email(self):
        self.assertTrue(ValidationUtils.is_valid_email("test@example.com"))
        self.assertFalse(ValidationUtils.is_valid_email("invalid-email"))

    def test_is_list_of_strings(self):
        self.assertTrue(ValidationUtils.is_list_of_strings(["a", "b", "c"]))
        self.assertFalse(ValidationUtils.is_list_of_strings(["a", 1, "c"]))
        self.assertFalse(ValidationUtils.is_list_of_strings("not a list"))
        self.assertFalse(ValidationUtils.is_list_of_strings([1, 2, 3]))


class TestDateUtils(unittest.TestCase):

    def test_convert_date_input(self):
        self.assertEqual(DateUtils.convert_date_input("2023-01-01"), date(2023, 1, 1))

    def test_get_current_brasilia_sp_datetime(self):
        current_sp_time = DateUtils.get_current_brasilia_sp_datetime()
        self.assertIsInstance(current_sp_time, datetime)
        self.assertEqual(current_sp_time, datetime.now(pytz.timezone("America/Sao_Paulo")))
        self.assertEqual(current_sp_time.tzinfo.zone, "America/Sao_Paulo")

    def test_get_brasilia_today(self):
        current_sp_date = DateUtils.get_brasilia_today()
        self.assertIsInstance(current_sp_date, date)
        self.assertEqual(current_sp_date, datetime.now(pytz.timezone("America/Sao_Paulo")).date())

    def test_get_utc_today(self):
        self.assertEqual(DateUtils.get_utc_today(), datetime.now().date())


class TestHashUtils(unittest.TestCase):

    def test_string_to_sha256(self):
        expected_result = hashlib.sha256("test".encode("utf-8")).hexdigest()
        self.assertEqual(HashUtils.string_to_sha256("test"), expected_result)


class TestEncodingUtils(unittest.TestCase):

    def test_encode_to_base64(self):
        self.assertEqual(EncodingUtils.encode_to_base64("test"), base64.b64encode("test".encode("utf-8")).decode("utf-8"))

    def test_decode_from_base64(self):
        self.assertEqual(EncodingUtils.decode_from_base64(base64.b64encode("test".encode("utf-8")).decode("utf-8")), "test")


if __name__ == "__main__":
    unittest.main()
