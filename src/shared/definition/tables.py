from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class Table:
    NAME: str
    COLUMNS_SPECS: Dict[str, str]
    PRIMARY_KEY: str
    STORED_AS: str
    SCHEMA: Optional[str] = None

    def __str__(self):
        return f"{self.SCHEMA}.{self.NAME}"
    
    @property
    def COLUMNS(self):
        return ', '.join(self.COLUMNS_SPECS.keys())
    
    def get_type(self, column):
        return self.COLUMNS_SPECS[column]

    def validate_existence(self, column):
        return column in self.COLUMNS_SPECS.keys()

@dataclass
class RawTable(Table):
    SCHEMA: str = "raw"
    COLUMNS_SPEC = {
        "id": "STRING",
        "data": "JSON",
    }
    PRIMARY_KEY = "id"
    STORED_AS = "mysql"

@dataclass
class CleanedTable(Table):
    PRIMARY_KEY: str = "date"
    STORED_AS: str = "delta"

@dataclass
class RefinedTable(Table):
    SCHEMA: str
    STORED_AS: str = "mysql"

@dataclass
class MorningRawTable(Table):
    NAME: str = "morning"
    COLUMNS_SPECS = {
        "id": "INT",
        "data": "JSON",
    }
    PRIMARY_KEY = "id"
    STORED_AS = "mysql"

@dataclass
class NightRawTable:
    NAME: str = "night"
    COLUMNS: 