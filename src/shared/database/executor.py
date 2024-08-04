from tabulate import tabulate
from sqlalchemy import text
from typing import List, Optional, Union

from sqlalchemy.orm import Session
from src.shared.database.connector import Connector
from src.shared.credentials import Credential
from src.shared.database.tables import Table
from src.shared.logger import LoggingManager


class DatabaseExecutor:
    def __init__(
        self,
        connector: Connector,
        mysql_credentials: Credential,
        ssh_credentials: Credential,
        logger_manager: LoggingManager = LoggingManager(),
    ):
        logger_manager.set_class_name(__class__.__name__)
        self.logger = logger_manager.get_logger()
        self.connector_instance = connector
        self.session: Session = self.connector_instance.get_session(mysql_credentials, ssh_credentials)

    def close(self) -> None:
        self.connector_instance.close()
        self.logger.info("Database connection closed successfully")

    def describe(self, table: Table):
        table_name = table.__tablename__
        result = self.session.execute(text(f"DESCRIBE {table_name}"))
        columns = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        rows = [list(row) for row in result]
        print(tabulate(rows, headers=columns, tablefmt="grid"))
        self.logger.info(f"Table {table_name} described successfully")

    def count(self, table: Table) -> int:
        print(self.session.query(table).count())
        self.logger.info(f"Count of records in {table.__tablename__} selected successfully")

    def select(
        self,
        table: Table,
        columns: Union[str, List[str]] = "*",
        order: str = "asc",
        limit: Optional[int] = None,
        **filters
    ):
        if columns == "*":
            query = self.session.query(table)
        else:
            if isinstance(columns, str):
                columns = [columns]
            columns = [getattr(table.c, col) for col in columns]
            query = self.session.query(*columns)

        if filters:
            query = query.filter_by(**filters)

        if order.lower() == "desc":
            query = query.order_by(table.c.id.desc())
        else:
            query = query.order_by(table.c.id.asc())

        if limit is not None:
            query = query.limit(limit)

        result = query.all()

        if result:
            headers = columns if columns != "*" else table.columns.keys()
            headers = [col.key if hasattr(col, 'key') else col for col in headers]
            rows = [list(row) for row in result]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print(f"No data found in {table.__tablename__}")
        self.logger.info(f"Data from {table.__tablename__} selected successfully")

    def insert(self, table: Table, **columns) -> None:
        """
        Example:
            json_data = {"example_key": "example_value"}
            
            executor.insert(LocalTest, data=json_data)
        """
        new_record = table(**columns)
        self.session.add(new_record)
        self.session.commit()

    def delete(self, table: Table, **filters) -> None:
        """
        Example:
            # Delete rows from the LocalTest table where the 'name' column is 'John Doe' and age is 25
            executor.delete(LocalTest, name='John Doe', age=25)
        """
        self.session.query(table).filter_by(**filters).delete()
        self.session.commit()    



    def update(self, table: Table, filters: dict, updates: dict) -> None:
        """
        Example:
            # Update rows in LocalTest where 'name' is 'John Doe' and set 'age' to 30
            executor.update(LocalTest, {'name': 'John Doe'}, {'age': 30})
        """
        self.session.query(table).filter_by(**filters).update(updates)
        self.session.commit()