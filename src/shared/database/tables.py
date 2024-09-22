from typing import List

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Integer,
    MetaData,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base

from src.shared.utils import DateUtils, HashUtils

Base = declarative_base(metadata=MetaData())


class MySqlTable(Base):
    __abstract__ = True
    __unique_constraint_name__ = None

    @classmethod
    def get_unique_constraint_name(cls) -> str:
        return cls.__unique_constraint_name__

    @staticmethod
    def get_schema_hash(schema_fields: List[str]) -> str:
        fields_as_string = ",".join(schema_fields)
        return HashUtils.string_to_sha256(fields_as_string)


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
    date = Column(Date, nullable=False)
    user_id = Column(String(36), nullable=False)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    element_string = Column(Text, nullable=False)
    schema_hash = Column(String(64), nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time)
    updated_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time, onupdate=DateUtils.current_brasilia_sp_time)

    __table_args__ = (UniqueConstraint("date", "user_id", "element_category", "element_name", name=__unique_constraint_name__),)


class ElementSchemas(MySqlTable):
    __tablename__ = "element_schemas"
    __unique_constraint_name__ = "_schema_uc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    schema_version = Column(Integer, nullable=False)
    schema_hash = Column(String(64), nullable=False)
    schema_fields = Column(Text, nullable=False)
    schema_dtypes = Column(Text, nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time)
    updated_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time, onupdate=DateUtils.current_brasilia_sp_time)

    __table_args__ = (UniqueConstraint("element_category", "element_name", "schema_version", name=__unique_constraint_name__),)
