from datetime import datetime

import pytz
from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    Enum,
    Integer,
    MetaData,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

metadata = MetaData()

Base = declarative_base(metadata=metadata)

current_brasilia_sp_time = lambda: datetime.now(pytz.timezone("America/Sao_Paulo"))


class MySqlTable(Base):
    __abstract__ = True


class LocalTest(MySqlTable):
    __tablename__ = "local_test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class MySqlMorningTable(MySqlTable):
    __tablename__ = "morning_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class MySqlNightTable(MySqlTable):
    __tablename__ = "night_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class ElementEntries(MySqlTable):
    __tablename__ = "element_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, nullable=False)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    element_string = Column(Text, nullable=False)
    schema_version = Column(Integer, nullable=False)
    op = Column(Enum("c", "d", "u"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=current_brasilia_sp_time)
    updated_at = Column(DateTime, nullable=False, default=current_brasilia_sp_time, onupdate=current_brasilia_sp_time)


class ElementSchemas(MySqlTable):
    __tablename__ = "element_schemas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    element_category = Column(String(255), nullable=False)
    element_name = Column(String(255), nullable=False)
    schema_version = Column(Integer, nullable=False)
    schema_definition = Column(Text, nullable=False)
