from sqlalchemy import Column, Integer, String, JSON, DateTime, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class Table(Base):
    __abstract__ = True

class LocalTest(Table):
    __tablename__ = "local_test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class MorningData(Table):
    __tablename__ = "morning_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class NightData(Table):
    __tablename__ = "night_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
