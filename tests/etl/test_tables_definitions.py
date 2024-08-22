import os
import unittest
from unittest.mock import MagicMock

from src.etl.definitions import BronzeTable, GoldTable, Path, SilverTable, Table


class TestTable(unittest.TestCase):

    def test_get_path(self):
        table = Table(name="test_table", source=None, layer="bronze", format="parquet")
        suffix = f".parquet"
        expected_path = Path(os.path.join("data", "bronze", "test_table") + suffix)
        self.assertEqual(table.get_path(), expected_path)


class TestBronzeTable(unittest.TestCase):

    def test_init(self):
        source = MagicMock()
        bronze_table = BronzeTable(name="test_bronze_table", source=source)
        self.assertEqual(bronze_table.name, "test_bronze_table")
        self.assertEqual(bronze_table.source, source)
        self.assertEqual(bronze_table.layer, "bronze")
        self.assertEqual(bronze_table.folder, "data")
        self.assertEqual(bronze_table.format, "parquet")


class TestSilverTable(unittest.TestCase):

    def test_init(self):
        source = MagicMock()
        silver_table = SilverTable(name="test_silver_table", source=source)
        self.assertEqual(silver_table.name, "test_silver_table")
        self.assertEqual(silver_table.source, source)
        self.assertEqual(silver_table.layer, "silver")
        self.assertEqual(silver_table.folder, "data")
        self.assertIsNone(silver_table.format)


class TestGoldTable(unittest.TestCase):

    def test_init(self):
        source = MagicMock()
        gold_table = GoldTable(name="test_gold_table", source=source)
        self.assertEqual(gold_table.name, "test_gold_table")
        self.assertEqual(gold_table.source, source)
        self.assertEqual(gold_table.layer, "gold")
        self.assertEqual(gold_table.folder, "data")
        self.assertIsNone(gold_table.format)


if __name__ == "__main__":
    unittest.main()
