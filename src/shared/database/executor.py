from typing import List, Union

from sqlalchemy import UniqueConstraint, and_, select, text
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.orm import Session
from tabulate import tabulate

from src.shared.database.tables import MySqlTable
from src.shared.logging.adapters import LoggingPrinter


class DatabaseExecutor(LoggingPrinter):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(class_name=self.__class__.__name__)
        self.session = session

    def describe(self, table: MySqlTable) -> None:
        table_name = table.__tablename__
        result = self.session.execute(text(f"DESCRIBE {table_name}"))
        columns = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        rows = [list(row) for row in result]
        print(tabulate(rows, headers=columns, tablefmt="grid"))
        self.logger.info(f"Table {table_name} described successfully")

    def count(self, table: MySqlTable) -> None:
        print(self.session.query(table).count())
        self.logger.info(f"Count of records in {table.__tablename__} selected successfully")

    def select(self, table, **filters) -> List[dict]:
        """
        Example:
            Select rows from the `LocalTest` table where id is 1 and name is 'Alice':
            `executor.select(LocalTest, id=1, name='Alice')`
        """
        stmt = select(table)
        if filters:
            conditions = []
            for column, value in filters.items():
                if hasattr(table, column):
                    conditions.append(getattr(table, column) == value)

            if conditions:
                stmt = stmt.where(and_(*conditions))

        results = self.session.execute(stmt).scalars().all()
        data = [{column.name: getattr(user, column.name) for column in table.__table__.columns} for user in results]
        self.logger.info(f"Data from {table.__tablename__} selected successfully")
        return data

    def insert(self, table: MySqlTable, **columns) -> None:
        """
        Example:
            Insert a new row into the `LocalTest` table:

            `json_data = {"example_key": "example_value"}` \n
            `executor.insert(LocalTest, data=json_data)`
        """
        new_record = table(**columns)
        self.session.add(new_record)
        self.session.commit()
        self.logger.info(f"Data inserted into {table.__tablename__} successfully")

    def delete(self, table: MySqlTable, **filters) -> None:
        """
        Example:
            Delete rows from the `LocalTest` table where the 'name' column is 'John Doe' and age is 25:
            `executor.delete(LocalTest, name='John Doe', age=25)`
        """
        self.session.query(table).filter_by(**filters).delete()
        self.session.commit()
        self.logger.info(f"Data deleted from {table.__tablename__} successfully")

    def update(self, table: MySqlTable, filters: dict, updates: dict) -> None:
        """
        Example:
            Update rows in `LocalTest` where 'name' is 'John Doe' and set 'age' to 30:
            `executor.update(LocalTest, {'name': 'John Doe'}, {'age': 30})`
        """
        self.session.query(table).filter_by(**filters).update(updates)
        self.session.commit()
        self.logger.info(f"Data in {table.__tablename__} updated successfully")

    def show_tables(self) -> List[str]:
        result = self.session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        self.logger.info("Tables shown successfully")
        return tables

    def show_create_table(self, table: Union[MySqlTable, str]) -> str:
        table_name = table.__tablename__.upper() if issubclass(table, MySqlTable) else table.upper()
        result = self.session.execute(text(f"SHOW CREATE TABLE {table}"))
        create_table_stmt = result.fetchone()[1]
        self.logger.info(f"CREATE TABLE statement for {table_name} shown successfully")
        return create_table_stmt

    def upsert(self, table: MySqlTable, **columns) -> None:
        try:
            uc_cols = self._get_unique_constraint_columns(table=table, uc_name=table.get_unique_constraint_name())

            stmt = mysql_insert(table).values(**columns)

            update_dict = {col: stmt.inserted[col] for col in columns if col not in uc_cols}

            if "updated_at" in table.__table__.columns:
                update_dict["updated_at"] = stmt.inserted["updated_at"]
            if "op" in table.__table__.columns:
                update_dict["op"] = "u"

            stmt = stmt.on_duplicate_key_update(**update_dict)

            self.session.execute(stmt)
            self.session.commit()
            self.logger.success(f"Data upserted into {table.__tablename__} successfully")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Failed to upsert data into {table.__tablename__}: {e}")
            raise

    def _get_unique_constraint_columns(self, table: MySqlTable, uc_name: str) -> List[str]:
        for constraint in table.__table__.constraints:
            if isinstance(constraint, UniqueConstraint) and constraint.name == uc_name:
                return list(constraint.columns.keys())
        raise AttributeError(f"Unique constraint {uc_name} not found in table {table.__tablename__}")
