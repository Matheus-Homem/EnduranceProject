from typing import Protocol


class Builder(Protocol):

    def get_definition(self, definition):
        pass

    def parse_definition(self):
        pass

    def build(self):
        pass


class InputBuilder(Builder):

    def get_definition(self, definition):
        self.definition = definition

    def parse_definition(self):
        pass

    def build(self):
        pass


class PersonaBuilder(Builder):

    def get_definition(self, definition):
        pass

    def build(self):
        pass


class PillarBuilder(Builder):

    def get_definition(self, definition):
        pass

    def build(self):
        pass


class FormBuilder(Builder):

    def get_definition(self, definition):
        pass

    def build(self):
        pass
