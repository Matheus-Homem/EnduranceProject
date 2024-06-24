from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Union

from src.web.platform.core.enums import (
    DefinitionType,
    FormattingType,
    InputType,
    SectionType,
    TemplateType,
)
from src.web.platform.core.protocols import Content, Definition
from src.web.platform.core.functions import generate_html


@dataclass
class ButtonDefinition(Content, Definition):

    def get_definition(self):
        return DefinitionType.BUTTON


@dataclass
class InputDefinition(Content, Definition):
    private_name: str
    type: InputType
    options: Optional[Dict] = None
    placeholder: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    label: Optional[str] = None
    public_name: Optional[str] = None
    output_formatting: Optional[FormattingType] = None
    box: Optional[str] = None
    section: Optional[str] = None
    input_fullname: Optional[str] = None
    optional: Optional[bool] = False
    columns: Optional[Dict] = None
    rows: Optional[Dict] = None

    def get_definition(self):
        return DefinitionType.INPUT

    def asdict(self) -> dict:
        """
        Convert the InputDefinition object to a dictionary.

        Returns:
        - dict: The InputDefinition object as a dictionary.
        """
        return asdict(self)

    def get_section(self, section_name):
        self.section = section_name

    def get_box(self, box_name):
        self.box = box_name

    def get_fullname(self, full_name):
        self.input_fullname = full_name


class TextInput(InputDefinition):
    def validate(self):
        pass  # TODO: implementar validação


class TextInput(InputDefinition):
    def validate(self):
        if self.options is not None:
            raise ValueError("TextInput should not have options.")
        if self.min_length is not None:
            raise ValueError("TextInput should not have min_length.")
        if self.max_length is not None:
            raise ValueError("TextInput should not have max_length.")
        if not (self.label or self.placeholder):
            raise ValueError("TextInput must have at least a label or a placeholder.")


class DateInput(InputDefinition):
    def validate(self):
        pass


class RangeInput(InputDefinition):
    def validate(self):
        pass


class NumberInput(InputDefinition):
    def validate(self):
        pass


class ToggleInput(InputDefinition):
    def validate(self):
        pass


class MultipleAlternativeInput(InputDefinition):
    def validate(self):
        pass


class SingleAlternativeInput(InputDefinition):
    def validate(self):
        pass


class TextAreaInput(InputDefinition):
    def validate(self):
        pass


class DateTimeInput(InputDefinition):
    def validate(self):
        pass


@dataclass
class InputCluster(Content):
    content_list: List[InputDefinition]
    is_recursive: Optional[bool] = False


@dataclass
class BoxDefinition(Definition):
    private_name: str
    public_name: str
    role: str
    habit_description: str
    content: Content | List[Content]
    outputs: Optional[Callable] = None
    section: Optional[str] = None
    box_fullname: Optional[str] = None

    def get_definition(self):
        return DefinitionType.BOX

    @property
    def content_list(self):
        if isinstance(self.content, Content):
            return self.content
        else:
            return self.content.content_list

    def asdict(self):
        return asdict(self)

    def get_section(self, section_name):
        self.section = section_name

    def get_fullname(self, full_name):
        self.box_fullname = full_name

    def map_input_definitions(self):
        self.mapped_content = []
        for content in self.content_list:
            if content.type == InputType.TEXT:
                self.mapped_content.append(TextInput(**content.asdict()))
            elif content.type == InputType.DATE:
                self.mapped_content.append(DateInput(**content.asdict()))
            elif content.type == InputType.RANGE:
                self.mapped_content.append(RangeInput(**content.asdict()))
            elif content.type == InputType.NUMBER:
                self.mapped_content.append(NumberInput(**content.asdict()))
            elif content.type == InputType.TOGGLE:
                self.mapped_content.append(ToggleInput(**content.asdict()))
            elif content.type == InputType.MULTI:
                self.mapped_content.append(MultipleAlternativeInput(**content.asdict()))
            elif content.type == InputType.SINGLE:
                self.mapped_content.append(SingleAlternativeInput(**content.asdict()))
            elif content.type == InputType.TEXT_AREA:
                self.mapped_content.append(TextAreaInput(**content.asdict()))
            elif content.type == InputType.DATETIME:
                self.mapped_content.append(DateTimeInput(**content.asdict()))
            else:
                raise ValueError(f"Unknown content type: {content.type}")
        return self.mapped_content


@dataclass
class SectionDefinition(Definition):
    private_name: str
    type: SectionType
    header: str
    boxes: List[BoxDefinition]
    description: Optional[str] = None

    def __post_init__(self):
        self._set_box()
        self._set_section()
        self._set_fullname()

    def get_definition(self):
        return DefinitionType.SECTION

    def asdict(self):
        return asdict(self)

    def _set_box(self):
        for box in self.boxes:
            for input in box.content_list:
                input.get_box(box.private_name)

    def _set_section(self):
        for box in self.boxes:
            box.get_section(self.type)
            for input in box.content_list:
                input.get_section(self.type)

    def _set_fullname(self):
        for box in self.boxes:
            box.get_fullname(f"{self.type}_{box.private_name}")
            for input in box.content_list:
                input.get_fullname(
                    f"{self.type}_{box.private_name}_{input.private_name}"
                )


@dataclass
class PageDefinition(Definition):
    private_name: str
    title: str
    header: str
    sections: List[SectionDefinition]

    def get_definition(self):
        return DefinitionType.PAGE
    
    def get_title(self):
        return self.title
    
    def get_header(self):
        return self.header

    def build_definition(self):
        generate_html(definition_type=DefinitionType.PAGE, definition=self)
