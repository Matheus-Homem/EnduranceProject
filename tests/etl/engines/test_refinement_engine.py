import unittest
from unittest.mock import MagicMock
import pandas as pd
from typing import Optional

from src.etl.core.definitions import PandasDF
from src.etl.engines.refinement import RefinementEngine

class TestRefinementEngine(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.engine = RefinementEngine()
        self.df = pd.DataFrame({
            'element_category': ['cat1', 'cat2'],
            'element_name': ['name1', 'name2'],
            'user_id': ['user1', 'user2'],
            'date_input': pd.to_datetime(['2023-01-01', '2023-01-02']),
            'value': [10, 20]
        })

    def test_build_summary_statistics(self):
        # Mock do método _build_summary_statistics
        self.engine._build_summary_statistics = MagicMock(return_value=self.df)
        result = self.engine._build_summary_statistics(self.df)
        self.engine._build_summary_statistics.assert_called_once_with(self.df)
        self.assertIsInstance(result, pd.DataFrame)

    def test_build_monthly_statistics(self):
        # Mock do método _build_monthly_statistics
        self.engine._build_monthly_statistics = MagicMock(return_value=self.df)
        result = self.engine._build_monthly_statistics(self.df)
        self.engine._build_monthly_statistics.assert_called_once_with(self.df)
        self.assertIsInstance(result, pd.DataFrame)

    def test_build_weekly_statistics(self):
        # Mock do método _build_weekly_statistics
        self.engine._build_weekly_statistics = MagicMock(return_value=self.df)
        result = self.engine._build_weekly_statistics(self.df)
        self.engine._build_weekly_statistics.assert_called_once_with(self.df)
        self.assertIsInstance(result, pd.DataFrame)

    def test_process(self):
        # Mock dos métodos _build_summary_statistics, _build_monthly_statistics e _build_weekly_statistics
        self.engine._build_summary_statistics = MagicMock(return_value=self.df)
        self.engine._build_monthly_statistics = MagicMock(return_value=None)
        self.engine._build_weekly_statistics = MagicMock(return_value=self.df)

        result = self.engine.process(self.df)

        self.engine._build_summary_statistics.assert_called_once_with(self.df)
        self.engine._build_monthly_statistics.assert_called_once_with(self.df)
        self.engine._build_weekly_statistics.assert_called_once_with(self.df)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], pd.DataFrame)
        self.assertIsInstance(result[1], pd.DataFrame)

if __name__ == '__main__':
    unittest.main()