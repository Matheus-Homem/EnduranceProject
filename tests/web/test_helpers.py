from src.web.helpers import clean_and_serialize_dict


def test_prepare_dict_to_command():
    data = {
        "name": "JOÃO\r\n DANÇARINO",
        "email": "\r\njohn.doe@example.com\r\n",
        "address": "Rua\r\n do\r\n Açaí",
        "number": 123,
    }
    expected_output = '{"name": "JOAO DANCARINO", "email": "john.doe@example.com", "address": "Rua do Acai", "number": "123"}'
    assert clean_and_serialize_dict(data) == expected_output

    data_empty = {}
    expected_output_empty = "{}"
    assert clean_and_serialize_dict(data_empty) == expected_output_empty
