from src.web.platform.core.types import FormattingType, InputType
from src.web.platform.core.functions import datetime_difference
from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    ModuleDefinition,
    SegmentDefinition,
)

sponsor_module = ModuleDefinition(
    public_name="Patrocinador",
    private_name="sponsor",
    role="O Patrocinador é aquele que busca ser útil para a sociedade, trazendo Estabilidade para a Expedição",
    habit_description="Sobre o hábito de Trabalhar",
    inputs=[
        InputDefinition(
            private_name="action",
            public_name="Ação",
            type=InputType.TOGGLE,
        ),
        InputDefinition(
            private_name="satisfaction",
            public_name="Satisfação",
            type=InputType.TOGGLE,
        ),
        InputDefinition(
            private_name="contribution",
            public_name="Contribuição",
            type=InputType.TOGGLE,
        ),
    ],
)

patron_module = ModuleDefinition(
    public_name="Mecenas",
    private_name="patron",
    role="O Mecenas é aquele que se dedica à algo que traga mais Estabilidade para a Expedição",
    habit_description="Sobre o hábito de Estudar",
    inputs=[
        InputDefinition(
            private_name="subject",
            type=InputType.MULTI,
            options=[
                {"Ofício", "profession"},
                {"Neurociências", "neurocience"},
            ],
        ),
        InputDefinition(
            private_name="other_subject",
            placeholder="Outro Assunto",
            type=InputType.TEXT,
        ),
    ],
)