from sqlalchemy import JSON, Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Table(Base):
    __abstract__ = True


class LocalTest(Table):
    __tablename__ = "local_test"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: dict = Column(JSON, nullable=True)


class MorningData(Table):
    __tablename__ = "morning_data"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: dict = Column(JSON, nullable=True)


class NightData(Table):
    __tablename__ = "night_data"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: dict = Column(JSON, nullable=True)
