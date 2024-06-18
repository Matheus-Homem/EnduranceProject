from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Union

from src.web.platform.core.enums import FormattingType, InputType
from src.web.platform.core.builders import *


# TODO: fazer a personalist gerar os objetos de Input e fazer com que cada objeto de input possa construir seu proprio HTML

@dataclass
class InputDefinition:
    """
    Define the structure of an input field in the form
    - private_name: str: The input field name used on HTML and send to system.
    - type: InputType: The type of the input field.
    - options: Optional[Dict]: The options dict where keys are string send to system (private) and value is strings used on HTML (public).
    - placeholder: Optional[str]: The placeholder of the input field.
    - min_length: Optional[int]: The minimum length of the input field.
    - max_length: Optional[int]: The maximum length of the input field.
    - label: Optional[str]: The label of the input field.
    - public_name: Optional[str]: The public name of the input field.
    - output_formatting: Optional[FormattingType]: The output formatting of the input field.
    - persona: Optional[str]: The persona of the input field.
    - pillar: Optional[str]: The pillar of the input field.
    - input_fullname: Optional[str]: The input fullname of the input field.
    """

    private_name: str
    type: InputType
    options: Optional[Dict] = None
    placeholder: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    label: Optional[str] = None
    public_name: Optional[str] = None
    output_formatting: Optional[FormattingType] = None
    persona: Optional[str] = None
    pillar: Optional[str] = None
    input_fullname: Optional[str] = None
    optional: Optional[bool] = False
    columns: Optional[Dict] = None
    rows: Optional[Dict] = None

    def asdict(self) -> dict:
        """
        Convert the InputDefinition object to a dictionary.

        Returns:
        - dict: The InputDefinition object as a dictionary.
        """
        return asdict(self)
    
    def get_pillar(self, pillar_name):
        self.pillar = pillar_name

    def get_persona(self, persona_name):
        self.persona = persona_name

    def get_fullname(self, full_name):
        self.input_fullname = full_name


@dataclass
class InputCluster:
    inputs_list: List[InputDefinition]
    is_recursive: Optional[bool] = False


@dataclass
class PersonaDefinition:
    public_name: str
    private_name: str
    role: str
    habit_description: str
    inputs: Union[InputCluster, List[InputDefinition]]
    outputs: Optional[Callable] = None
    pillar: Optional[str] = None
    persona_fullname: Optional[str] = None

    @property
    def inputs_list(self):
        if isinstance(self.inputs, InputCluster):
            return self.inputs.inputs_list
        return self.inputs

    def asdict(self):
        return asdict(self)
    
    def get_pillar(self, pillar_name):
        self.pillar = pillar_name

    def get_fullname(self, full_name):
        self.persona_fullname = full_name


@dataclass
class PillarDefinition:
    public_name: str
    private_name: str
    description: str
    personas: List[PersonaDefinition]

    def __post_init__(self):
        self._set_persona()
        self._set_pillar()
        self._set_fullname()

    def asdict(self):
        return asdict(self)

    def _set_persona(self):
        for persona in self.personas:
            for input in persona.inputs_list:
                input.get_persona(persona.private_name)

    def _set_pillar(self):
        for persona in self.personas:
            persona.get_pillar(self.private_name)
            for input in persona.inputs_list:
                input.get_pillar(self.private_name)

    def _set_fullname(self):
        for persona in self.personas:
            persona.get_fullname(f"{self.private_name}_{persona.private_name}")
            for input in persona.inputs_list:
                input.get_fullname(
                    f"{self.private_name}_{persona.private_name}_{input.private_name}"
                )


@dataclass
class FormDefinition:
    form_name: str
    pillars: List[PillarDefinition]
