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
from src.shared.utils import DateUtils

Base = declarative_base(metadata=MetaData())

class MySqlTable(Base):
    __abstract__ = True


class User(MySqlTable):
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
    schema_version = Column(Integer, nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time)
    updated_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time, onupdate=DateUtils.current_brasilia_sp_time)

    __table_args__ = (UniqueConstraint("date", "user_id", "element_category", "element_name", name=__unique_constraint_name__),)

    @classmethod
    def get_unique_constraint_name(cls):
        return cls.__unique_constraint_name__


class ElementSchemas(MySqlTable):
    __tablename__ = "element_schemas"
    __unique_constraint_name__ = "_schema_uc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    schema_version = Column(String(64), nullable=False)
    schema_definition = Column(Text, nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time)
    updated_at = Column(DateTime, nullable=False, default=DateUtils.current_brasilia_sp_time, onupdate=DateUtils.current_brasilia_sp_time)

    __table_args__ = (UniqueConstraint("element_category", "element_name", "schema_version", name=__unique_constraint_name__),)

    @classmethod
    def get_unique_constraint_name(cls):
        return cls.__unique_constraint_name__