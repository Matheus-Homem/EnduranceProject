import unittest
from unittest.mock import MagicMock

from polars import DataFrame

from src.etl.definitions import Path, Reader, Table, Writer
from src.shared.logger import LoggingManager


class ConcreteReader(Reader):
    def read_dataframe(self, source: Table) -> DataFrame:
        return DataFrame()


class ConcreteWriter(Writer):
    def write_dataframe(self, dataframe: DataFrame, path: Path) -> None:
        pass


class TestReaderWriterInit(unittest.TestCase):

    def setUp(self):
        self.mock_logger_manager = MagicMock(spec=LoggingManager)
        self.mock_logger = MagicMock()
        self.mock_logger_manager.get_logger.return_value = self.mock_logger

    def test_reader_init(self):
        reader = ConcreteReader(logger_manager=self.mock_logger_manager)
        self.assertEqual(reader.logger_manager, self.mock_logger_manager)
        self.assertEqual(reader.logger, self.mock_logger)
        self.mock_logger_manager.set_class_name.assert_called_with("ConcreteReader")

    def test_writer_init(self):
        writer = ConcreteWriter(logger_manager=self.mock_logger_manager)
        self.assertEqual(writer.logger_manager, self.mock_logger_manager)
        self.assertEqual(writer.logger, self.mock_logger)
        self.mock_logger_manager.set_class_name.assert_called_with("ConcreteWriter")


if __name__ == "__main__":
    unittest.main()
