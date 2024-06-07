from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union

class InputType:
    TEXT = "text"
    DATE = "date"
    RANGE = "range"
    NUMBER = "number"
    TOGGLE = "toggle"
    MULTI = "multi-choice"
    SINGLE = "single-choice"
    TEXTA_AREA = "text-area"
    DATETIME = "datetime-local"

class FormattingType:
    RAW = "raw"
    TIME = "time"
    WEIGHT = "weight"
    CALORIES = "calories"
    MONETARY = "monetary"
    PERCENTAGE = "percentage"

class CalculationFunctions:
    SLEEP_TIME_DIFFERENCE = "calculateSleepTimeDifference"

@dataclass
class InputDefinition:
    name: str
    type: InputType
    placeholder: Optional[str] = None
    options: Optional[List[Dict]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    label: Optional[str] = None
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
    outputs: Optional[List[CalculationFunctions]] = None

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