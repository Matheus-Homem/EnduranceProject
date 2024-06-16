from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    PersonaDefinition,
)
from src.web.platform.core.types import FormattingType, Icon, InputType

navigator_persona = PersonaDefinition(
    public_name="Navegador",
    private_name="navigator",
    role="O Navegador é aquele que busca experiência de outras vidas para trazer a Sabedoria à Expedição",
    habit_description="Sobre o hábito da Leitura",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                private_name="book", type=InputType.TEXT, placeholder="Nome do Livro"
            ),
            InputDefinition(
                private_name="notes",
                type=InputType.TOGGLE,
                options={"False": Icon.POWER_OFF, "True": Icon.NOTES},
            ),
        ],
    ),
)

alchemist_persona = PersonaDefinition(
    public_name="Alquimista",
    private_name="alchemist",
    role="O Alquimista é aquele que transforma as inpurezas adquiridas durante a Expedição em Sabedoria",
    habit_description="Sobre o hábito de Mudar",
    inputs=[
        InputDefinition(
            private_name="emotion",
            type=InputType.MULTI,
            options={
                "anger": "Raiva",
                "frustration": "Frustação",
                "anhedonia": "Anedonia",
                "sadness": "Tristeza",
                "fear": "Medo",
                "resentment": "Ressentimento",
            },
        ),
        InputDefinition(
            private_name="feeling",
            type=InputType.TEXTA_AREA,
            placeholder="Hoje senti [] na situação []\nE graças a isso, []",
        ),
    ],
)

sentinel_persona = PersonaDefinition(
    public_name="Sentinela",
    private_name="sentinel",
    role="O Sentinela é aquele que através do descanso é capaz de proteger a Sabedoria durante toda a Expedição",
    habit_description="Sobre o hábito de Dormir",
    inputs=[
        InputDefinition(
            private_name="screen_time",
            label="Tempo de Tela",
            type=InputType.NUMBER,
            min_length=3,
            max_length=4,
            output_formatting=FormattingType.TIME,
        ),
        InputDefinition(
            private_name="bed_time", label="Início do Sono", type=InputType.DATETIME
        ),
        InputDefinition(
            private_name="wakeup_time", label="Fim do Sono", type=InputType.DATETIME
        ),
    ],
)


class WisdomPersonas:
    NAVIGATOR = navigator_persona
    ALCHEMIST = alchemist_persona
    SENTINEL = sentinel_persona
