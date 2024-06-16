from src.web.platform.core.definitions import (
    InputCluster,
    InputDefinition,
    PersonaDefinition,
)
from src.web.platform.core.types import FormattingType, Icon, InputType

caretaker_persona = PersonaDefinition(
    public_name="Zelador",
    private_name="caretaker",
    role="O Zelador é aquele que ",
    habit_description="Sobre o hábito de Cuidar",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                private_name="hygiene",
                type=InputType.MULTI,
                label="Higiene",
                options={"morning": "Manhã", "afternoon": "Tarde", "night": "Noite"},
            ),
            InputDefinition(
                private_name="relaxation",
                type=InputType.MULTI,
                label="Relaxamento",
                options={"morning": "Manhã", "afternoon": "Tarde", "night": "Noite"},
            ),
            InputDefinition(
                private_name="domestic_care",
                label="Cuidados Domésticos",
                type=InputType.SINGLE,
                options={"False": Icon.POWER_OFF, "True": Icon.EXCELENCE},
            ),
            InputDefinition(
                private_name="food_preparation",
                label="Preparo de Alimentos",
                type=InputType.SINGLE,
                options={"False": Icon.POWER_OFF, "True": Icon.EXCELENCE},
            ),
        ],
    ),
)

diplomat_persona = PersonaDefinition(
    public_name="Diplomata",
    private_name="diplomat",
    role="O Diplomata é aquele que ",
    habit_description="Sobre o hábito de Respeitar",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                private_name="respect",
                type=InputType.RANGE,
                columns={
                    "no_contact": "Sem Contato",
                    "disrespectful": "Desrespeitoso",
                    "respectful": "Respeitoso",
                },
                rows={
                    "family": "Família",
                    "meat": "Animais Abatidos",
                    "pet": "Animais Domésticos",
                    "society": "Sociedade",
                    "friends": "Amigos",
                    "contacts": "Conhecidos",
                    "work": "Trabalho",
                    "neighbors": "Vizinhos",
                    "relationship": "+1",
                },
            ),
        ],
    ),
)

citizen_persona = PersonaDefinition(
    public_name="Cidação",
    private_name="citizen",
    role="O Cidação é aquele que ",
    habit_description="Sobre o hábito de Conviver",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                private_name="known_groups",
                type=InputType.MULTI,
                label="Convívios Comuns",
                options={
                    "family": "Família",
                    "friends": "Amigos",
                    "yoga": "Yoga",
                    "calisthenics": "Calistenia",
                },
                optional=True,
            ),
            InputDefinition(
                private_name="new_groups",
                type=InputType.TEXT,
                label="Novo Convívio",
                optional=True,
            ),
            InputDefinition(
                private_name="experience",
                type=InputType.TEXTA_AREA,
                placeholder="Convivier com pessoas me faz...",
            ),
        ],
    ),
)


class KindnessPersonas:
    CARETAKER = caretaker_persona
    DIPLOMAT = diplomat_persona
    CITIZEN = citizen_persona
