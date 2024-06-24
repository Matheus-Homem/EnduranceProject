import pytest

from src.web.platform.core.builders import Builder
from src.web.platform.core.definitions import (
    BoxDefinition,
    InputCluster,
    InputDefinition,
    PageDefinition,
    SectionDefinition,
)
from src.web.platform.core.enums import FormattingType, Icon, InputType, SectionType
from src.web.platform.core.protocols import Definition


class TestBuilder:

    def setup_method(self):
        self.builder = Builder()

        self.test_input_definition = InputDefinition(
            private_name="test_input_definition",
            type=InputType.TEXT,
        )

        self.test_box_definition = BoxDefinition(
            private_name="test_box_definition",
            public_name="Test Box",
            role="Test Role",
            habit_description="Test Habit Description",
            content=[self.test_input_definition],
        )

        self.test_section_definition = SectionDefinition(
            private_name="test_section_definition",
            type=SectionType.BASIC,
            header="Test Header",
            description="Test Description",
            boxes=[self.test_box_definition],
        )

        self.test_page_definition = PageDefinition(
            private_name="test_page_definition",
            title="Test Title",
            header="Test Header",
            sections=[self.test_section_definition],
        )

    def test_get_definition(self):
        self.builder.set_definition(definition=self.test_page_definition)

        assert self.builder.definition.private_name == "test_page_definition"

    def test_validate_definition_success(self):
        self.builder.set_definition(definition=self.test_page_definition)
        self.builder.validate_definition()

    def test_validate_definition_failed(self):
        section_type_basic = SectionType.BASIC
        self.builder.set_definition(definition=section_type_basic)

        with pytest.raises(AttributeError):
            self.builder.validate_definition()

    def test_build(self):
        self.builder.set_definition(definition=self.test_page_definition)
        self.builder.validate_definition()
        self.builder.build()
