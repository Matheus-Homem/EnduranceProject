from dataclasses import dataclass, field
from typing import List, Dict

class InputType:
    TEXT = "text"
    TEXTA_AREA = "text-area"
    SINGLE = "single-choice"
    MULTI = "multi-choice"
    TOGGLE = "toggle"
    RANGE = "range"

class RecursivityType:
    RECURSIVE = "recursive"
    LINEAR = "linear"

@dataclass
class InputDefinition:
    name: str
    type: InputType
    placeholder: str = field(default=None)
    options: List[Dict] = field(default_factory=list)

@dataclass
class InputClusters:
    recursivity: RecursivityType
    inputs_list: List[InputDefinition]

@dataclass
class HabitDefinition:
    description: str
    input_clusters: List[InputClusters]

@dataclass
class ModuleDefinition:
    module_name: str
    module_role: str
    habit_sets: List[HabitDefinition]

@dataclass
class SegmentDefinition:
    segment_name: str
    segment_description: str
    modules: List[ModuleDefinition]

@dataclass
class FormDefinition:
    form_name: str
    segments: List[SegmentDefinition]

navigator_module = ModuleDefinition(
    module_name = "Navegador",
    module_role = "O Navegador é aquele que busca experiência de outras vidas para trazer a Sabedoria à Expedição",
    habit_sets = [
        HabitDefinition(
            description = "Sobre o hábito da Leitura",
            input_clusters = [
                InputClusters(
                    recursivity = RecursivityType.RECURSIVE,
                    inputs_list = [
                        InputDefinition(
                            name = "book",
                            type = InputType.TEXT,
                            placeholder = "Nome do Livro",
                        ),
                        InputDefinition(
                            name = "mode",
                            type = InputType.SINGLE,
                            options = [
                                {"pill": "fa-solid fa-pill"},
                                {"session": "fa-solid fa-session"},
                            ],
                        ),
                        InputDefinition(
                            name = "notes",
                            type = InputType.TOGGLE,
                            options = [
                                {False: "fa-solid fa-power-off"},
                                {True: "fa-solid fa-notes"},
                            ],
                        ),
                    ]
                )
            ]
        )
    ]
)

alchemist_module = ModuleDefinition()

sentinel_module = ModuleDefinition()


general_segment = SegmentDefinition(
    segment_name = "Informações Gerais",

)



wisdom_segment = SegmentDefinition(
    segment_name = "Sabedoria",
    segment_description = "A Sabedoria é...",
    modules = [
        navigator_module,
        alchemist_module,
        sentinel_module,
    ]
)
estability_segment = SegmentDefinition()

strength_segment = SegmentDefinition()

kindness_segment = SegmentDefinition()

devotion_segment = SegmentDefinition()


form = FormDefinition(
    form_name = "Bússola Lunar",
    segments = [
        general_segment,
        wisdom_segment,
        estability_segment,
        strength_segment,
        kindness_segment,
        devotion_segment,
    ]
)