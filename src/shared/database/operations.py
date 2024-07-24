from src.shared.decorators import establish_mysql_connection


class DatabaseOperations:

    @staticmethod
    @establish_mysql_connection
    def execute_command(cursor, command: str):
        """
        Commands examples:
        - 'INSERT INTO local_test (data) VALUES (\'{"key1": "value1", "key2": "value2"}\');'
        - 'UPDATE local_test SET data = \'{"key1": "new_value"}\' WHERE id = 1;'
        - 'DELETE FROM local_test WHERE id = 1;'
        """
        cursor.execute(command)
        print("Command successfully executed")

    @staticmethod
    @establish_mysql_connection
    def select_data(cursor, command: str):
        """
        Commands example:
        - 'SELECT * FROM local_test;'
        """
        cursor.execute(command)
        result = cursor.fetchall()
        for row in result:
            print(row)
        return result

    @staticmethod
    @establish_mysql_connection
    def count_rows(cursor, table: str):
        command = f"SELECT COUNT(*) FROM {table}"
        cursor.execute(command)
        result = cursor.fetchone()
        print(f"Row count: {result[0]}")
        return result[0]
