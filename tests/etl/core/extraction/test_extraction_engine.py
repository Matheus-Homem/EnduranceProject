import unittest

import pandas as pd

from src.etl.core.extraction import ExtractionEngine


class TestExtractionEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ExtractionEngine()

    def test_process(self):
        data = [
            {
                "id": 1,
                "entry_date": pd.Timestamp("2021-01-01"),
                "user_id": "0",
                "element_category": "test_category",
                "element_name": "test_name",
                "element_string": "{'nao':'nao'}",
                "schema_encoded": "1",
                "op": "u",
                "created_at": pd.Timestamp("2024-09-20 06:14:57"),
                "updated_at": pd.Timestamp("2024-09-20 06:24:51"),
            }
        ]

        expected_df = pd.DataFrame(data)

        result_df = self.engine.process(data)

        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == "__main__":
    unittest.main()
