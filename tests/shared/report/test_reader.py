import unittest

from src.shared.report.reader import convert_all_float_to_int


class TestGoldReader(unittest.TestCase):

    # @patch.object(IOManager, 'get_handler')
    # def test_summary(self, mock_get_handler):
    #     data = {
    #         "element_name": ["element1", "element2", "element1"],
    #         "last_date": [pd.to_datetime("2022-01-01"), pd.to_datetime("2022-01-02"), pd.to_datetime("2022-01-03")],
    #         "total": [10, 20, 30],
    #         "longest_streak": [5, 10, 15],
    #         "longest_gap": [2, 4, 6]
    #     }
    #     df_mock = pd.DataFrame(data)

    #     mock_handler = MagicMock()
    #     mock_handler.read.return_value = df_mock
    #     mock_get_handler.return_value = mock_handler

    #     result = GoldReader.summary("element1")

    #     expected_result = [
    #         {
    #             "element_name": "element1",
    #             "last_date": pd.to_datetime("2022-01-01"),
    #             "total": 10,
    #             "longest_streak": 5,
    #             "longest_gap": 2
    #         },
    #         {
    #             "element_name": "element1",
    #             "last_date": pd.to_datetime("2022-01-03"),
    #             "total": 30,
    #             "longest_streak": 15,
    #             "longest_gap": 6
    #         }
    #     ]

    #     for record in expected_result:
    #         record["last_date"] = record["last_date"].strftime('%Y-%m-%d')

    #     for record in result:
    #         record["last_date"] = pd.to_datetime(record["last_date"]).strftime('%Y-%m-%d')

    #     self.assertEqual(result, expected_result)

    def test_convert_all_float_to_int(self):
        df_dict = [{"a": 1.0, "b": 2.0, "c": float("nan")}, {"a": 3.0, "b": 4.0, "c": 5.0}]
        expected_result = [{"a": 1, "b": 2, "c": None}, {"a": 3, "b": 4, "c": 5}]
        result = convert_all_float_to_int(df_dict)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
