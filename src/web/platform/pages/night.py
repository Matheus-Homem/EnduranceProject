from src.web.platform.core.definitions import FormDefinition, SectionDefinition
from src.web.platform.pillars.devotion import DevotionBoxes
from src.web.platform.pillars.kindness import KindnessBoxes
from src.web.platform.pillars.stability import StabilityBoxes
from src.web.platform.pillars.strength import StrengthBoxes
from src.web.platform.pillars.wisdom import WisdomBoxes

night_form = FormDefinition(
    form_name="night_form",
    pillars=[
        SectionDefinition(
            public_name="Sabedoria",
            private_name="wisdom",
            description="A Sabedoria é...",
            boxes=[
                WisdomBoxes.NAVIGATOR,
                WisdomBoxes.ALCHEMIST,
            ],
        ),
        SectionDefinition(
            public_name="Estabilidade",
            private_name="stability",
            description="A Estabilidade é...",
            boxes=[
                StabilityBoxes.SPONSOR,
                StabilityBoxes.PATRON,
            ],
        ),
        SectionDefinition(
            public_name="Força",
            private_name="strength",
            description="A Força é...",
            boxes=[
                StrengthBoxes.VANGUARD,
                StrengthBoxes.SCOUT,
                StrengthBoxes.NIGHT_COOK,
            ],
        ),
        SectionDefinition(
            public_name="Gentiliza",
            private_name="kindness",
            description="A Gentiliza é...",
            boxes=[
                KindnessBoxes.CARETAKER,
                KindnessBoxes.DIPLOMAT,
                KindnessBoxes.CITIZEN,
            ],
        ),
    ],
)
