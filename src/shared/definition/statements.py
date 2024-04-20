from src.shared.definition.tables import Table

from typing import List


class DataManipulationLanguage:

    def __init__(
        self,
        cursor
    ):
        self.cursor = cursor

    def select(
            self,
            table: Table,
            condition: str = None,
        ) -> List[str]:
        try:
            sql_select_query = f"SELECT * FROM {table}"
            if condition is not None:
                sql_select_query += f" WHERE {condition}"
            self.cursor.execute(sql_select_query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"An error occurred when selecting from {table}: {e}")

    def select_cols(
            self,
            table: Table,
            columns: List[str],
            condition: str = None
        ) -> List[str]:
        try:
            sql_select_columns_query = f"SELECT {', '.join(columns)} FROM {table}"
            if condition is not None:
                sql_select_columns_query += f" WHERE {condition}"
            self.cursor.execute(sql_select_columns_query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"An error occurred when selecting cols from {table}: {e}")

    def top(
            self,
            table: Table,
            n: int
        ) -> List[str]:
        try:
            sql_top_query = f"SELECT * FROM {table} LIMIT {n}"
            self.cursor.execute(sql_top_query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"An error occurred when top selecting from {table}: {e}")

    def count(
            self,
            table: Table
        ) -> int:
        try:
            sql_count_query = f"SELECT COUNT(*) FROM {table}"
            self.cursor.execute(sql_count_query)
            count = self.cursor.fetchone()[0]
            print(f"A tabela {table} possui {count} linhas.")
        except Exception as e:
            print(f"An error occurred when counting from {table}: {e}")

    def insert(
        self,
        table: Table,
        values: List[str]
    ):
        try:
            sql_insert_query = f"INSERT INTO {table} ({Table.COLUMNS}) VALUES ({', '.join(['%s' for _ in values])})"
            self.cursor.execute(sql_insert_query, values)
            self.cursor.commit()
        except Exception as e:
            print(f"An error occurred when inserting into {table}: {e}")

    def delete(
            self,
            table: Table,
            condition: str
        ):
        try:
            sql_delete_query = f"DELETE FROM {table} WHERE {condition}"
            self.cursor.execute(sql_delete_query)
            self.cursor.commit()
        except Exception as e:
            print(f"An error occurred when deleting from {table}: {e}")

    def update(
            self,
            table: Table,
            column: str,
            new_value: str,
            condition: str
        ):
        try:
            if not table.validate_existence(column):
                raise ValueError(f"Column {column} does not exist in table {table}")
            sql_update_query = f"UPDATE {table} SET {column} = %s WHERE {condition}"
            self.cursor.execute(sql_update_query, (new_value,))
            self.cursor.commit()
        except Exception as e:
            print(f"An error occurred when updating {table}: {e}")

    def merge(
            self,
            table: Table,
            values: List[str],
            condition: str
        ):
        try:
            sql_merge_query = f"MERGE INTO {table} ({table.COLUMNS}) VALUES ({', '.join(['%s' for _ in values])}) WHERE {condition}"
            self.cursor.execute(sql_merge_query, values)
            self.cursor.commit()
        except Exception as e:
            print(f"An error occurred when merging {table}: {e}")