from src.web.platform.core.definitions import PageDefinition, SectionDefinition
from src.web.platform.pillars.devotion import DevotionBoxes
from src.web.platform.pillars.kindness import KindnessBoxes
from src.web.platform.pillars.stability import StabilityBoxes
from src.web.platform.pillars.strength import StrengthBoxes
from src.web.platform.pillars.wisdom import WisdomBoxes

morning_form = PageDefinition(
    private_name="morning_form",
    title="Manhã",
    header="Manhã",
    sections=[
        SectionDefinition(
            public_name="Sabedoria",
            private_name="wisdom",
            description="A Sabedoria é...",
            boxes=[
                WisdomBoxes.SENTINEL,
            ],
        ),
        SectionDefinition(
            public_name="Estabilidade",
            private_name="stability",
            description="A Estabilidade é...",
            boxes=[
                StabilityBoxes.TREASURER,
            ],
        ),
        SectionDefinition(
            public_name="Força",
            private_name="strength",
            description="A Força é...",
            boxes=[
                StrengthBoxes.MORNING_COOK,
            ],
        ),
    ],
)
