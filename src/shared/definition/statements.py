from src.shared.definition.tables import Table

from typing import List


class DataManipulationLanguage:

    def __init__(
        self,
        connection
    ):
        self.connection = connection
        self.cursor = self.connection.get_cursor()

    def select(
            self,
            table: Table,
            condition: str = None,
        ) -> List[str]:
        sql_select_query = f"SELECT * FROM {table}"
        if condition is not None:
            sql_select_query += f" WHERE {condition}"
        self.cursor.execute(sql_select_query)
        rows = self.cursor.fetchall()
        return rows

    def select_columns(
            self,
            table: Table,
            columns: List[str],
            condition: str = None
        ) -> List[str]:
        sql_select_columns_query = f"SELECT {', '.join(columns)} FROM {table}"
        if condition is not None:
            sql_select_columns_query += f" WHERE {condition}"
        self.cursor.execute(sql_select_columns_query)
        rows = self.cursor.fetchall()
        return rows

    def top(
            self,
            table: Table,
            n: int
        ) -> List[str]:
        sql_top_query = f"SELECT * FROM {table} LIMIT {n}"
        self.cursor.execute(sql_top_query)
        rows = self.cursor.fetchall()
        return rows

    def count(
            self,
            table: Table
        ) -> int:
        sql_count_query = f"SELECT COUNT(*) FROM {table}"
        self.cursor.execute(sql_count_query)
        count = self.cursor.fetchone()[0]
        return count

    def insert(
        self,
        table: Table,
        values: List[str]
    ):
        sql_insert_query = f"INSERT INTO {table} ({Table.COLUMNS}) VALUES ({', '.join(['%s' for _ in values])})"
        self.cursor.execute(sql_insert_query, values)
        self.connection.commit()

    def delete(
            self,
            table: Table,
            condition: str
        ):
        sql_delete_query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(sql_delete_query)
        self.connection.commit()

    def update(
            self,
            table: Table,
            column: str,
            new_value: str,
            condition: str
        ):
        if not table.validate_existence(column):
            raise ValueError(f"Column {column} does not exist in table {table}")
        sql_update_query = f"UPDATE {table} SET {column} = %s WHERE {condition}"
        self.cursor.execute(sql_update_query, (new_value,))
        self.connection.commit()

    def merge(
            self,
            table: Table,
            values: List[str],
            condition: str
        ):
        sql_merge_query = f"MERGE INTO {table} ({table.COLUMNS}) VALUES ({', '.join(['%s' for _ in values])}) WHERE {condition}"
        self.cursor.execute(sql_merge_query, values)
        self.connection.commit()