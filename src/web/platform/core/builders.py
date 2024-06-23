from src.web.platform.core.enums import DefinitionType
from src.web.platform.core.protocols import Definition


class Builder:

    def set_definition(self, definition: Definition):
        self.definition = definition

    # def _validate_definition(self):
    #     if not isinstance(self.definition, Definition):
    #         raise TypeError(f"{self.definition.private_name} is not of type 'Definition'")

    def _validate_definition(self):
        valid_definitions = DefinitionType.get_all()
        try:
            definition_type = self.definition.get_definition()
            definition_type in valid_definitions
        except AttributeError:
            raise AttributeError(f"{type(self.definition)} is not a Definition")

    def _parse_definition(self):
        pass

    def build(self):
        self._validate_definition()
