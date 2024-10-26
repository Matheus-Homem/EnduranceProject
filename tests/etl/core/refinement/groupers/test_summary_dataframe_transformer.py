from unittest import TestCase

import pandas as pd

from src.etl.core.definitions import Format, Layer
from src.etl.core.io import IOManager
from src.etl.core.refinement.groupers.summary import SummaryDataFrameTransformer


class TestSummaryDataFrameTransformer(TestCase):

    def setUp(self):
        self.df_navigator = IOManager(layer=Layer.SILVER, format=Format.DELTA).get_handler().read("navigator")
        self.df_diplomat = IOManager(layer=Layer.SILVER, format=Format.DELTA).get_handler().read("diplomat")
        self.summary_transformer = SummaryDataFrameTransformer()

    def test_apply(self):
        df_summary = self.summary_transformer.apply(self.df_navigator)
        pd.testing.assert_frame_equal(df_summary, self.df_navigator)
        self.assertIsInstance(df_summary, pd.DataFrame)
