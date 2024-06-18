from src.web.platform.core.definitions import FormDefinition, PillarDefinition
from src.web.platform.pillars.wisdom import WisdomPersonas
from src.web.platform.pillars.stability import StabilityPersonas
from src.web.platform.pillars.strength import StrengthPersonas
from src.web.platform.pillars.kindness import KindnessPersonas
from src.web.platform.pillars.devotion import DevotionPersonas

night_form = FormDefinition(
    form_name="night_form",
    pillars=[
        PillarDefinition(
            public_name="Sabedoria",
            private_name="wisdom",
            description="A Sabedoria é...",
            personas=[
                WisdomPersonas.NAVIGATOR,
                WisdomPersonas.ALCHEMIST,
            ],
        ),
        PillarDefinition(
            public_name="Estabilidade",
            private_name="stability",
            description="A Estabilidade é...",
            personas=[
                StabilityPersonas.SPONSOR,
                StabilityPersonas.PATRON,
            ],
        ),
        PillarDefinition(
            public_name="Força",
            private_name="strength",
            description="A Força é...",
            personas=[
                StrengthPersonas.VANGUARD,
                StrengthPersonas.SCOUT,
                StrengthPersonas.NIGHT_COOK,
            ],
        ),
        PillarDefinition(
            public_name="Gentiliza",
            private_name="kindness",
            description="A Gentiliza é...",
            personas=[
                KindnessPersonas.CARETAKER,
                KindnessPersonas.DIPLOMAT,
                KindnessPersonas.CITIZEN,
            ],
        ),
    ],
)
