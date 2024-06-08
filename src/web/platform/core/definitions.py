from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Union, Callable
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

@dataclass
class InputCluster:
    inputs_list: List[InputDefinition]
    is_recursive: Optional[bool] = False

@dataclass
class ModuleDefinition:
    public_name: str
    private_name: str
    role: str
    habit_description: str
    inputs: Union[InputCluster, List[InputDefinition]]
    outputs: Optional[Callable] = None

    def asdict(self):
        return asdict(self)

@dataclass
class SegmentDefinition:
    public_name: str
    private_name: str
    description: str
    modules: List[ModuleDefinition]

@dataclass
class FormDefinition:
    form_name: str
    segments: List[SegmentDefinition]