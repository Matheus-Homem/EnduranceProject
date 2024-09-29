import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.database.connection.executor import DatabaseExecutor
from src.database.tables import MockTable


class TestDatabaseExecutor(unittest.TestCase):

    def setUp(self):
        self.builder = MagicMock()
        self.session = MagicMock(spec=Session)
        self.executor = DatabaseExecutor(session=self.session)

    def test_describe(self):
        with patch("src.database.connection.builder.DatabaseExecutorBuilder", return_value=self.builder):
            with patch("builtins.print") as mocked_print:
                self.executor.describe(MockTable)
                mocked_print.assert_called()
                self.session.execute.assert_called()

    def test_count(self):
        with patch("src.database.connection.builder.DatabaseExecutorBuilder", return_value=self.builder):
            with patch("builtins.print") as mocked_print:
                self.executor.count(MockTable)
                mocked_print.assert_called()
                self.session.query(MockTable).count.assert_called()

    def test_select_with_filters(self):
        mock_result = [
            MagicMock(mock_id=1, mock_colA="Alice", op="c", updated_at="2021-01-01 00:00:00"),
        ]
        self.session.execute.return_value.scalars.return_value.all.return_value = mock_result

        result = self.executor.select(MockTable, mock_id=1, mock_colA="Alice")
        expected_result = [{"mock_id": 1, "mock_colA": "Alice", "op": "c", "updated_at": "2021-01-01 00:00:00"}]

        self.session.execute.assert_called()
        print(result)
        self.assertEqual(result, expected_result)

    def test_select_without_filters(self):
        mock_result = [
            MagicMock(mock_id=1, mock_colA="Alice", op="c", updated_at="2021-01-01 00:00:00"),
            MagicMock(mock_id=2, mock_colA="Bob", op="u", updated_at="2021-01-01 00:00:00"),
        ]
        self.session.execute.return_value.scalars.return_value.all.return_value = mock_result

        result = self.executor.select(MockTable)
        expected_result = [
            {"mock_id": 1, "mock_colA": "Alice", "op": "c", "updated_at": "2021-01-01 00:00:00"},
            {"mock_id": 2, "mock_colA": "Bob", "op": "u", "updated_at": "2021-01-01 00:00:00"},
        ]

        self.session.execute.assert_called()
        self.assertEqual(result, expected_result)

    def test_insert(self):
        with patch("src.database.connection.builder.DatabaseExecutorBuilder", return_value=self.builder):
            self.executor.insert(MockTable, mock_id=1, mock_colA="Alice")
            self.session.add.assert_called_once()
            self.session.commit.assert_called_once()

    def test_delete(self):
        with patch("src.database.connection.builder.DatabaseExecutorBuilder", return_value=self.builder):
            self.executor.delete(MockTable, mock_id=1)
            self.session.query(MockTable).filter_by(mock_id=1).delete.assert_called_once()
            self.session.commit.assert_called_once()

    def test_update(self):
        with patch("src.database.connection.builder.DatabaseExecutorBuilder", return_value=self.builder):
            self.executor.update(MockTable, filters={"mock_id": 1}, updates={"mock_colA": "Alice"})
            self.session.query(MockTable).filter_by(**{"mock_id": 1}).update.assert_called_once()
            self.session.commit.assert_called_once()

    def test_show_tables(self):
        self.session.execute.return_value = [("table1",), ("table2",)]
        result = self.executor.show_tables()
        self.assertEqual(result, ["table1", "table2"])

    def test_show_create_table(self):
        self.session.execute.return_value.fetchone.return_value = (None, "CREATE TABLE test_table ...")
        result = self.executor.show_create_table(MockTable)
        self.assertEqual(result, "CREATE TABLE test_table ...")

    def test_upsert(self):
        self.executor._get_unique_constraint_columns = MagicMock(return_value=["mock_id"])
        self.executor.upsert(MockTable, mock_id=1, mock_colA="Alice")
        self.session.execute.assert_called()
        self.session.commit.assert_called()

    def test_upsert_exception(self):
        self.executor._get_unique_constraint_columns = MagicMock(return_value=["mock_id"])
        self.session.execute.side_effect = SQLAlchemyError("Simulated exception")

        with self.assertRaises(SQLAlchemyError):
            self.executor.upsert(MockTable, mock_id=1, mock_colA="Alice")

        self.session.rollback.assert_called()

    def test_get_unique_constraint_columns(self):
        result = self.executor._get_unique_constraint_columns(MockTable, MockTable.get_unique_constraint_name())
        self.assertEqual(result, ["mock_id"])

    def test_undefined_unique_constraint_column(self):
        with self.assertRaises(AttributeError):
            self.executor._get_unique_constraint_columns(MockTable, "undefined_column")


if __name__ == "__main__":
    unittest.main()
