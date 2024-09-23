from os_local import get_absolute_path, join_paths
from src.shared.credentials import PRD
from src.shared.database.builder import DatabaseExecutorBuilder


def export_db_statements():
    path = get_absolute_path("database")
    file_path = join_paths(path, "create_tables.sql")
    create_table_statements = []

    with DatabaseExecutorBuilder(use_production_db=PRD) as executor:
        
        tables = executor.show_tables()
        for table in tables:
            statement = executor.show_create_table(table)
            create_table_statements.append(statement)


    with open(file_path, "w") as file:
        for statement in create_table_statements:
            file.write(statement + ";\n\n")


if __name__ == "__main__":
    export_db_statements()