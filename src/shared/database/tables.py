from sqlalchemy import JSON, Column, DateTime, Integer, MetaData, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class MySqlTable(Base):
    __abstract__ = True


class LocalTest(MySqlTable):
    __tablename__ = "local_test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    def get_schema(self):
        return {
            "id": self.id,
            "data": self.data,
            "profile": self.profile,
            "created_at": self.created_at,
        }


class MySqlMorningTable(MySqlTable):
    __tablename__ = "morning_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())


class NightData(MySqlTable):
    __tablename__ = "night_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False, default={})
    profile = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
