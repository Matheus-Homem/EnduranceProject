from typing import Protocol


class Reader(Protocol):

    def read(self): ...


class Writer(Protocol):

    def write(self): ...


class ProccessingType:
    FULL = "full"
    INCREMENTAL = "incremental"
