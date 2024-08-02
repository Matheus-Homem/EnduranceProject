from dataclasses import dataclass

from sqlalchemy import JSON, Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class LocalTest(Base):
    __tablename__ = "local_test"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: dict = Column(JSON, nullable=True)


@dataclass
class MorningData(Base):
    __tablename__ = "morning_data"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: dict = Column(JSON, nullable=True)


@dataclass
class NightData(Base):
    __tablename__ = "night_data"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: dict = Column(JSON, nullable=True)
