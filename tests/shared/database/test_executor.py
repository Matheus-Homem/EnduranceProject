import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy import JSON, Column, DateTime, Integer, String, func
from sqlalchemy.orm import Session
from tabulate import tabulate

from src.shared.database.executor import DatabaseExecutor
from src.shared.database.tables import MySqlTable
from src.shared.logger import LoggingManager


class TestTable(MySqlTable):
    __tablename__ = "test_tablename"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class TestDatabaseExecutor(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)
        self.mock_logger_manager = MagicMock(spec=LoggingManager)
        self.mock_logger = MagicMock()
        self.mock_logger_manager.get_logger.return_value = self.mock_logger

        self.executor = DatabaseExecutor(self.mock_session, self.mock_logger_manager)

    def test_describe(self):
        table = TestTable

        with patch("builtins.print") as mocked_print:
            self.executor.describe(table)

        expected_headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        mocked_print.assert_called_with(
            tabulate(None, headers=expected_headers, tablefmt="grid")
        )

    def test_count(self):
        mock_table = MagicMock(spec=MySqlTable)
        mock_table.__tablename__ = "mock_table"
        self.mock_session.query.return_value.count.return_value = 42

        with patch("builtins.print") as mocked_print:
            self.executor.count(mock_table)

        self.mock_session.query.assert_called_once_with(mock_table)
        self.mock_session.query.return_value.count.assert_called_once()
        mocked_print.assert_called_once_with(42)
        self.mock_logger.info.assert_called_once_with(
            "Count of records in mock_table selected successfully"
        )

    def test_select_with_filters(self):
        table = TestTable
        self.mock_session.execute.return_value.scalars.return_value.all.return_value = (
            []
        )
        with patch("src.shared.database.executor.select") as select_mock:
            self.executor.select(table, id=1, name="Alice")

        select_mock.assert_called_once_with(table)
        self.mock_session.execute.assert_called_once()
        self.mock_session.execute.return_value.scalars.assert_called_once()
        self.mock_session.execute.return_value.scalars.return_value.all.assert_called_once()
        self.mock_logger.info.assert_called_once_with(
            "Data from test_tablename selected successfully"
        )

    def test_insert(self):
        mock_table = MagicMock(spec=MySqlTable)
        mock_table.__tablename__ = "mock_table"

        self.executor.insert(mock_table, id=1, name="Alice")

        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_logger.info.assert_called_once_with(
            "Data inserted into mock_table successfully"
        )

    def test_delete(self):
        mock_table = MagicMock(spec=MySqlTable)
        mock_table.__tablename__ = "mock_table"

        self.executor.delete(mock_table, id=1)

        self.mock_session.query.assert_called_once_with(mock_table)
        self.mock_session.query.return_value.filter_by.assert_called_once_with(id=1)
        self.mock_session.query.return_value.filter_by.return_value.delete.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_logger.info.assert_called_once_with(
            "Data deleted from mock_table successfully"
        )

    def test_update(self):
        mock_table = MagicMock(spec=MySqlTable)
        mock_table.__tablename__ = "mock_table"

        self.executor.update(mock_table, {"id": 1}, {"name": "Alice"})

        self.mock_session.query.assert_called_once_with(mock_table)
        self.mock_session.query.return_value.filter_by.assert_called_once_with(id=1)
        self.mock_session.query.return_value.filter_by.return_value.update.assert_called_once_with(
            {"name": "Alice"}
        )
        self.mock_session.commit.assert_called_once()
        self.mock_logger.info.assert_called_once_with(
            "Data in mock_table updated successfully"
        )


if __name__ == "__main__":
    unittest.main()
