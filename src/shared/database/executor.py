from sqlalchemy import and_, select, text
from sqlalchemy.orm import Session
from tabulate import tabulate

from src.shared.database.tables import MySqlTable
from src.shared.logging.printer import LoggingPrinter


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

    def select(self, table, **filters) -> list:
        """
        Example:
            # Select rows from the LocalTest table where id is 1 and name is 'Alice':
            executor.select(LocalTest, id=1, name='Alice')
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
        headers = [column.name for column in table.__table__.columns]
        data = [{column.name: getattr(user, column.name) for column in table.__table__.columns} for user in results]
        self.logger.info(f"Data from {table.__tablename__} selected successfully")
        return data

    def insert(self, table: MySqlTable, **columns) -> None:
        """
        Example:
            # Insert a new row into the LocalTest table:

            json_data = {"example_key": "example_value"}
            executor.insert(LocalTest, data=json_data)
        """
        new_record = table(**columns)
        self.session.add(new_record)
        self.session.commit()
        self.logger.info(f"Data inserted into {table.__tablename__} successfully")

    def delete(self, table: MySqlTable, **filters) -> None:
        """
        Example:
            # Delete rows from the LocalTest table where the 'name' column is 'John Doe' and age is 25:
            executor.delete(LocalTest, name='John Doe', age=25)
        """
        self.session.query(table).filter_by(**filters).delete()
        self.session.commit()
        self.logger.info(f"Data deleted from {table.__tablename__} successfully")

    def update(self, table: MySqlTable, filters: dict, updates: dict) -> None:
        """
        Example:
            # Update rows in LocalTest where 'name' is 'John Doe' and set 'age' to 30:
            executor.update(LocalTest, {'name': 'John Doe'}, {'age': 30})
        """
        self.session.query(table).filter_by(**filters).update(updates)
        self.session.commit()
        self.logger.info(f"Data in {table.__tablename__} updated successfully")
