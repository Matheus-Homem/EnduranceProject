from typing import List

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Integer,
    MetaData,
    String,
    Text,
    UniqueConstraint,
    inspect,
)
from sqlalchemy.orm import declarative_base

from src.shared.utils import DateUtils, EncodingUtils, ValidationUtils

Base = declarative_base(metadata=MetaData())


class MySqlTable(Base):
    __tablename__: str
    __abstract__: str = True
    __unique_constraint_name__: str = None

    @classmethod
    def get_unique_constraint_name(cls) -> str:
        return cls.__unique_constraint_name__

    @classmethod
    def get_columns(cls):
        inspector = inspect(cls)
        columns = [column.name for column in inspector.columns]
        return columns

    @classmethod
    def get_dtypes(cls):
        inspector = inspect(cls)
        dtypes = {column.name: str(column.type) for column in inspector.columns}
        return dtypes

    @staticmethod
    def get_schema_encoded(schema_fields: List[str]) -> str:
        if not ValidationUtils.is_list_of_strings(schema_fields):
            raise ValueError("Input `schema_fields` must be a list of strings.")
        sorted_fields_as_string = ",".join(sorted(schema_fields))
        return EncodingUtils.encode_to_base64(sorted_fields_as_string)

    @staticmethod
    def decode_schema(encoded_schema: str) -> List[str]:
        decoded_string = EncodingUtils.decode_from_base64(encoded_schema)
        return decoded_string.split(",")


class Users(MySqlTable):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_id = Column(String(36), unique=True, nullable=False)


class ElementEntries(MySqlTable):
    __tablename__ = "element_entries"
    __unique_constraint_name__ = "_entry_uc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_date = Column(Date, nullable=False)
    user_id = Column(String(36), nullable=False)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    element_string = Column(Text, nullable=False)
    schema_encoded = Column(Text, nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=DateUtils.get_brasilia_datetime)
    updated_at = Column(DateTime, nullable=False, default=DateUtils.get_brasilia_datetime, onupdate=DateUtils.get_brasilia_datetime)

    __table_args__ = (UniqueConstraint("entry_date", "user_id", "element_category", "element_name", name=__unique_constraint_name__),)


class ElementSchemas(MySqlTable):
    __tablename__ = "element_schemas"
    __unique_constraint_name__ = "_schema_uc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    schema_version = Column(Integer, nullable=False)
    schema_encoded = Column(Text, nullable=False)
    schema_fields = Column(Text, nullable=False)
    schema_dtypes = Column(Text, nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=DateUtils.get_brasilia_datetime)
    updated_at = Column(DateTime, nullable=False, default=DateUtils.get_brasilia_datetime, onupdate=DateUtils.get_brasilia_datetime)

    __table_args__ = (UniqueConstraint("element_category", "element_name", "schema_version", name=__unique_constraint_name__),)


class DailyControl(MySqlTable):
    __tablename__ = "daily_control"
    __unique_constraint_name__ = "_control_uc"

    entry_date = Column(Date, primary_key=True)
    user_id = Column(String(36), primary_key=True)
    element_category = Column(String(255), primary_key=True)
    element_name = Column(String(255), primary_key=True)
    has_data = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("entry_date", "user_id", "element_category", "element_name", name=__unique_constraint_name__),)


class MockTable(MySqlTable):
    __tablename__ = "mock_table"
    __unique_constraint_name__ = "_mock_uc"

    mock_id = Column(String(36), primary_key=True)
    mock_colA = Column(String(255))
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    updated_at = Column(DateTime, nullable=False, default=DateUtils.get_brasilia_datetime, onupdate=DateUtils.get_brasilia_datetime)

    __table_args__ = (UniqueConstraint("mock_id", name=__unique_constraint_name__),)
