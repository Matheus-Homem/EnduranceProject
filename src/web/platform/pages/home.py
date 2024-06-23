from src.web.platform.core.definitions import (
    BoxDefinition,
    PageDefinition,
    SectionDefinition,
)
from src.web.platform.core.enums import SectionType

home_page = PageDefinition(
    private_name="home_page",
    title="Home",
    header="Maarga Project",
    sections=[
        SectionDefinition(
            type=SectionType.BASIC,
            boxes=[],
        ),
    ],
)
