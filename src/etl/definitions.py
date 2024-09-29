from enum import Enum


class Layer(Enum):
    DATABASE = "database"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
