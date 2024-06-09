from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Union

from src.web.platform.core.types import FormattingType, InputType


@dataclass
class InputDefinition:
    private_name: str
    type: InputType
    placeholder: Optional[str] = None
    options: Optional[List[Dict]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    label: Optional[str] = None
    public_name: Optional[str] = None
    output_formatting: Optional[FormattingType] = None
    persona: Optional[str] = None
    pillar: Optional[str] = None
    input_fullname: Optional[str] = None

    def asdict(self):
        return asdict(self)


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
                input.persona = persona.private_name

    def _set_pillar(self):
        for persona in self.personas:
            persona.pillar = self.private_name
            for input in persona.inputs_list:
                input.pillar = self.private_name

    def _set_fullname(self):
        for persona in self.personas:
            persona.persona_fullname = f"{self.private_name}_{persona.private_name}"
            for input in persona.inputs_list:
                input.input_fullname = (
                    f"{self.private_name}_{persona.private_name}_{input.private_name}"
                )


@dataclass
class FormDefinition:
    form_name: str
    pillars: List[PillarDefinition]
