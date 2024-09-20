from datetime import datetime

import pytz
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

Base = declarative_base(metadata=MetaData())


def current_brasilia_sp_time():
    return datetime.now(pytz.timezone("America/Sao_Paulo"))


class MySqlTable(Base):
    __abstract__ = True


class ElementEntries(MySqlTable):
    __tablename__ = "element_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, nullable=False)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    element_string = Column(Text, nullable=False)
    schema_version = Column(Integer, nullable=False)
    op = Column(Enum("c", "u", "d"), nullable=False, default="c")
    created_at = Column(DateTime, nullable=False, default=current_brasilia_sp_time)
    updated_at = Column(DateTime, nullable=False, default=current_brasilia_sp_time, onupdate=current_brasilia_sp_time)

    __table_args__ = (UniqueConstraint("date", "user_id", "element_category", "element_name", name="_entry_uc"),)


class ElementSchemas(MySqlTable):
    __tablename__ = "element_schemas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    schema_version = Column(Integer, nullable=False)
    schema_definition = Column(Text, nullable=False)
