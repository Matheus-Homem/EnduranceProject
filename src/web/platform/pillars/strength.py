from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    PersonaDefinition,
)
from src.web.platform.core.enums import FormattingType, Icon, InputType

vanguard_persona = PersonaDefinition(
    public_name="Vanguarda",
    private_name="vanguard",
    role="O Vanguarda é aquele que constrói uma estrutura capaz de prover Força à Expedição e aos outros",
    habit_description="Sobre o hábito de Resistir",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                private_name="exercise",
                type=InputType.MULTI,
                options={"yoga": "Yoga", "calisthenics": "Calistenia"},
            ),
            InputDefinition(
                private_name="mode",
                type=InputType.SINGLE,
                options={"pill": Icon.PILLS, "session": Icon.CALENDAR_CHECK},
            ),
            InputDefinition(
                private_name="excelence",
                type=InputType.TOGGLE,
                options={"False": Icon.POWER_OFF, "True": Icon.EXCELENCE},
            ),
        ],
    ),
)

scout_persona = PersonaDefinition(
    public_name="Batedor",
    private_name="scout",
    role="O Batedor é aquele que aumenta a durabilidade da Expedição, trazendo Força à cada um dos membros",
    habit_description="Sobre o hábito de Durar",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                private_name="activity",
                type=InputType.MULTI,
                options={
                    "running": "Corrida",
                    "cycling": "Ciclismo",
                    "swimming": "Natação",
                },
            ),
            InputDefinition(
                private_name="mode",
                type=InputType.SINGLE,
                options={"pill": Icon.PILLS, "session": Icon.CALENDAR_CHECK},
            ),
            InputDefinition(
                private_name="excelence",
                type=InputType.TOGGLE,
                options={"False": Icon.POWER_OFF, "True": Icon.EXCELENCE},
            ),
            InputDefinition(
                private_name="distance",
                label="Distância",
                type=InputType.NUMBER,
                optional=True,
                min_length=3,
                max_length=4,
                output_formatting=FormattingType.DISTANCE,
            ),
            InputDefinition(
                private_name="time",
                label="Duração",
                type=InputType.NUMBER,
                optional=True,
                min_length=3,
                max_length=4,
                output_formatting=FormattingType.TIME,
            ),
            InputDefinition(
                private_name="calories",
                label="Calorias",
                type=InputType.NUMBER,
                optional=True,
                output_formatting=FormattingType.CALORIES,
            ),
        ],
    ),
)

cook_persona_morning = PersonaDefinition(
    public_name="Cozinheiro",
    private_name="cook",
    role="O Cozinheiro é aquele que mantém a Força da Expedição através do equilíbrio entre prazer e necessidade",
    habit_description="Sobre o hábito de Alimentar-se",
    inputs=[
        InputDefinition(
            private_name="weight",
            label="Peso",
            type=InputType.NUMBER,
            min_length=3,
            max_length=4,
            output_formatting=FormattingType.WEIGHT,
        ),
        InputDefinition(
            private_name="calories",
            label="Calorias de Ontem",
            type=InputType.NUMBER,
            output_formatting=FormattingType.CALORIES,
        ),
        InputDefinition(
            private_name="satisfaction",
            type=InputType.SINGLE,
            options={"False": "Insatisfeito", "True": "Satisfeito"},
        ),
    ],
)

cook_persona_night = PersonaDefinition(
    public_name="Cozinheiro",
    private_name="cook",
    role="O Cozinheiro é aquele que mantém a Força da Expedição através do equilíbrio entre prazer e necessidade",
    habit_description="Sobre o hábito de Alimentar-se",
    inputs=[
        InputDefinition(
            private_name="meals",
            type=InputType.RANGE,
            columns={
                "nonexistent": "Inexistente",
                "bad": "Ruim",
                "average": "Razoável",
                "excellent": "Excelente",
            },
            rows={
                "breakfast": "Café da Manhã",
                "morning_snack": "Lanche Matutino",
                "lunch": "Almoço",
                "dessert": "Sobremesa",
                "afternoon_snack": "Lanche Vespertino",
                "dinner": "Janta",
                "supper": "Ceia",
            },
        ),
        InputDefinition(
            private_name="water",
            type=InputType.RANGE,
            columns={
                "0": "-1",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4+",
            },
            rows={
                "water": "Água",
            },
        ),
    ],
)


class StrengthPersonas:
    VANGUARD = vanguard_persona
    SCOUT = scout_persona
    MORNING_COOK = cook_persona_morning
    NIGHT_COOK = cook_persona_night
