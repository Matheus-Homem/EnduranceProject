import pytest

from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    PersonaDefinition,
    SectionDefinition,
)
from src.web.platform.core.enums import InputType
from src.web.platform.core.builders import InputBuilder, PersonaBuilder, PillarBuilder


class TestInputBuilder:

    def test_text_input_builder(self):

        input_builder = InputBuilder()

        text_input_definition = InputDefinition(
            private_name="text_input_test",
            type=InputType.TEXT,
        )

        input_builder.get_definition(definition=text_input_definition)

        input_builder.build()

        #print(text_input_definition.asdict())
        assert isinstance(input_builder, InputBuilder)

