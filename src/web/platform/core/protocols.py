from typing import Protocol, runtime_checkable


@runtime_checkable
class Definition(Protocol):

    def get_definition(self):
        pass

    def build_definition(self):
        pass


@runtime_checkable
class Content(Protocol):
    pass
