import unittest
from unittest.mock import MagicMock

from pandas import DataFrame

from src.etl.core.definitions import Engine, IOHandler
from src.etl.core.pipeline import Pipeline


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.reader = MagicMock(spec=IOHandler)
        self.engine = MagicMock(spec=Engine)
        self.writer = MagicMock(spec=IOHandler)

        self.table = DataFrame({"col1": [1, 2], "col2": [3, 4]})
        self.processed_table = DataFrame({"col1": [10, 20], "col2": [30, 40]})

        self.reader.read.return_value = self.table
        self.engine.process.return_value = self.processed_table

        self.pipeline = Pipeline(reader=self.reader, engine=self.engine, writer=self.writer)

    def test_execute(self):
        self.pipeline.execute()

        self.reader.read.assert_called_once()
        self.engine.process.assert_called_once_with(table=self.table)
        self.writer.write.assert_called_once_with(table=self.processed_table)


if __name__ == "__main__":
    unittest.main()
