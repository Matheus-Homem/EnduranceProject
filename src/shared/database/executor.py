from sqlalchemy.orm import scoped_session
from sqlalchemy.inspection import inspect

from src.shared.database.tables import Base

class SQLExecutor:
    def __init__(self, session: scoped_session):
        self.session = session

    def insert(self, table: Base, **kwargs) -> None:
        new_record = table(**kwargs)
        self.session.add(new_record)
        self.session.commit()

    def select(self, table: Base, **kwargs):
        return self.session.query(table).filter_by(**kwargs).all()

    def select_count(self, table: Base) -> int:
        return self.session.query(table).count()

    def describe(self, table: Base):
        return inspect(table).columns.keys()

    def update(self, table: Base, filters: dict, updates: dict) -> None:
        self.session.query(table).filter_by(**filters).update(updates)
        self.session.commit()

    def delete(self, table: Base, **kwargs) -> None:
        self.session.query(table).filter_by(**kwargs).delete()
        self.session.commit()

# Example usage
# def main():
#     # Assuming `session` is an instance of SQLAlchemy session
#     executor = SQLExecutor(session)

#     # Insert into the User table
#     executor.insert(User, username='john_doe', email='john@example.com')

#     # Select from the User table
#     users = executor.select(User, username='john_doe')
#     print(users)

#     # Select count from the User table
#     user_count = executor.select_count(User)
#     print(user_count)

#     # Describe the User table
#     user_columns = executor.describe(User)
#     print(user_columns)

#     # Update the User table
#     executor.update(User, {'username': 'john_doe'}, {'email': 'john_new@example.com'})

#     # Delete from the User table
#     executor.delete(User, username='john_doe')

# if __name__ == "__main__":
#     main()