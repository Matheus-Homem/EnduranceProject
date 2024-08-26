import unittest
from unittest.mock import MagicMock, call, patch

from src.etl.definitions import BronzeTable, GoldTable, SilverTable
from src.etl.manager import DataProcessingManager
from src.shared.database.tables import MySqlMorningTable


class TestDataProcessingManager(unittest.TestCase):

    def setUp(self):
        self.logger_manager = MagicMock()
        self.logger_manager.get_logger.return_value = MagicMock()
        self.manager = DataProcessingManager(logger_manager=self.logger_manager, bronze=True, silver=True, gold=True)

    def test_error_missing_layer_param(self):
        with self.assertRaises(Exception):
            DataProcessingManager(logger_manager=self.logger_manager)

    @patch("src.etl.pipeline.extractor.ExtractorPipeline.execute")
    @patch("src.etl.pipeline.cleaner.CleanerPipeline.execute")
    @patch("src.etl.pipeline.refiner.RefinerPipeline.execute")
    def test_process_table(self, mock_refiner_execute, mock_cleaner_execute, mock_extractor_execute):
        bronze_table = BronzeTable(name="test_bronze_table", source=None)
        silver_table = SilverTable(name="test_silver_table", source=bronze_table)
        gold_table = GoldTable(name="test_gold_table", source=silver_table)

        DataProcessingManager.process_table(bronze_table)
        mock_extractor_execute.assert_called_once_with(table=bronze_table)

        DataProcessingManager.process_table(silver_table)
        mock_cleaner_execute.assert_called_once_with(table=silver_table)

        DataProcessingManager.process_table(gold_table)
        mock_refiner_execute.assert_called_once_with(table=gold_table)

    def test_get_layer_class(self):
        self.assertEqual(self.manager.get_layer_class("BronzeTable"), BronzeTable)
        self.assertEqual(self.manager.get_layer_class("SilverTable"), SilverTable)
        self.assertEqual(self.manager.get_layer_class("GoldTable"), GoldTable)
        with self.assertRaises(Exception):
            self.manager.get_layer_class("InvalidTable")

    def test_get_source(self):
        source = self.manager.get_source(BronzeTable, "MySqlMorningTable")
        self.assertEqual(source, MySqlMorningTable)

        source = self.manager.get_source(SilverTable, "test_bronze_table")
        self.assertIsInstance(source, BronzeTable)
        self.assertEqual(source.name, "test_bronze_table")

        source = self.manager.get_source(GoldTable, "test_silver_table")
        self.assertIsInstance(source, SilverTable)
        self.assertEqual(source.name, "test_silver_table")

        with self.assertRaises(Exception):
            self.manager.get_source(BronzeTable, "InvalidSource")

    @patch("src.etl.manager.DataProcessingManager.process_table")
    @patch("src.etl.manager.DataProcessingManager.get_source")
    @patch("src.etl.manager.DataProcessingManager.get_layer_class")
    @patch(
        "src.etl.manager.yaml.safe_load",
        return_value={
            "tables": [
                {"layer_class": "BronzeTable", "source": "MySqlMorningTable", "name": "morning_raw"},
                {"layer_class": "BronzeTable", "source": "MySqlNightTable", "name": "night_raw"},
                {"layer_class": "SilverTable", "source": "night_raw", "name": "navigator"},
                {"layer_class": "GoldTable", "source": "navigator", "name": "gold_test"},
            ]
        },
    )
    def test_run_pipeline(self, mock_safe_load, mock_get_layer_class, mock_get_source, mock_process_table):
        # Mocking objects
        bronze_table_1 = MagicMock(name="BronzeTable1")
        bronze_table_2 = MagicMock(name="BronzeTable2")
        silver_table = MagicMock(name="SilverTable")
        gold_table = MagicMock(name="GoldTable")

        bronze_table_1_instance = MagicMock(name="BronzeTable1Instance")
        bronze_table_2_instance = MagicMock(name="BronzeTable2Instance")
        silver_table_instance = MagicMock(name="SilverTableInstance")
        gold_table_instance = MagicMock(name="GoldTableInstance")

        bronze_table_1.return_value = bronze_table_1_instance
        bronze_table_2.return_value = bronze_table_2_instance
        silver_table.return_value = silver_table_instance
        gold_table.return_value = gold_table_instance

        mock_get_layer_class.side_effect = [bronze_table_1, bronze_table_2, silver_table, gold_table]

        # Running the test
        self.manager.run_pipeline()

        # Asserting yaml.safe_load
        mock_safe_load.assert_called_once()

        # Asserting get_layer_class calls
        expected_get_layer_class_calls = [call("BronzeTable"), call("BronzeTable"), call("SilverTable"), call("GoldTable")]
        mock_get_layer_class.assert_called()
        mock_get_layer_class.assert_has_calls(expected_get_layer_class_calls, any_order=False)

        # Asserting get_source calls
        expected_get_source_calls = [
            call(bronze_table_1, "MySqlMorningTable"),
            call(bronze_table_2, "MySqlNightTable"),
            call(silver_table, "night_raw"),
            call(gold_table, "navigator"),
        ]
        mock_get_source.assert_called()
        mock_get_source.assert_has_calls(expected_get_source_calls, any_order=False)

        # Asserting process_table calls
        expected_process_table_calls = [
            call(bronze_table_1_instance),
            call(bronze_table_2_instance),
            call(silver_table_instance),
            call(gold_table_instance),
        ]
        mock_process_table.assert_called()
        mock_process_table.assert_has_calls(expected_process_table_calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
