from src.web.platform.core.enums import DefinitionType
from src.web.platform.core.protocols import Definition


class Builder:

    def set_definition(self, definition: Definition):
        self.definition = definition
        self.validated = False

    def validate_definition(self):
        valid_definitions = DefinitionType.get_all()
        try:
            definition_type = self.definition.get_definition()
            definition_type in valid_definitions
            self.validated = True
        except AttributeError:
            raise AttributeError(f"{type(self.definition)} is not a Definition")

    def parse_definition(self):
        pass

    def build(self):
        if self.validated:
            self.definition.build_definition()
        else:
            raise AttributeError("Definition has not been validated")


def build_definition(definition: Definition):
    builder = Builder()
    builder.set_definition(definition=definition)
    builder.validate_definition()
    builder.parse_definition()
    builder.build()
