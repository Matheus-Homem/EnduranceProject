from src.web.platform.core.definitions import FormDefinition, PillarDefinition
from src.web.platform.pillars.wisdom import WisdomPersonas
from src.web.platform.pillars.stability import StabilityPersonas

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
    ]
)