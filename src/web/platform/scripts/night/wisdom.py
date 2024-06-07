from src.web.platform.core.definitions import (
    CalculationFunctions,
    FormattingType,
    InputCluster,
    InputDefinition,
    InputType,
    ModuleDefinition,
    SegmentDefinition,
)

navigator_module = ModuleDefinition(
    public_name="Navegador",
    private_name="navigator",
    role="O Navegador é aquele que busca experiência de outras vidas para trazer a Sabedoria à Expedição",
    habit_description="Sobre o hábito da Leitura",
    inputs=InputCluster(
        is_recursive=True,
        inputs_list=[
            InputDefinition(
                name="book", type=InputType.TEXT, placeholder="Nome do Livro"
            ),
            InputDefinition(
                name="mode",
                type=InputType.SINGLE,
                options=[
                    {"pill": "fa-solid fa-pills"},
                    {"session": "fa-regular fa-calendar-check"},
                ],
            ),
            InputDefinition(
                name="notes",
                type=InputType.TOGGLE,
                options=[
                    {False: "fa-solid fa-power-off"},
                    {True: "fa-solid fa-notes"},
                ],
            ),
        ],
    ),
)


alchemist_module = ModuleDefinition(
    public_name="Alquimista",
    private_name="alchemist",
    role="O Alquimista é aquele que transforma as inpurezas adquiridas durante a Expedição em Sabedoria",
    habit_description="Sobre o hábito de Mudar",
    inputs=[
        InputDefinition(
            name="emotion",
            type=InputType.MULTI,
            options=[
                {"Raiva", "anger"},
                {"Frustação", "frustration"},
                {"Anedonia", "anhedonia"},
                {"Tristeza", "sadness"},
                {"Medo", "fear"},
                {"Ressentimento", "resentment"},
            ],
        ),
        InputDefinition(
            name="feeling",
            type=InputType.TEXTA_AREA,
            placeholder="Hoje senti [] na situação []\nE graças a isso, []",
        ),
    ],
)

sentinel_module = ModuleDefinition(
    public_name="Sentinela",
    private_name="sentinel",
    role="O Sentinela é aquele que através do descanso é capaz de proteger a Sabedoria durante toda a Expedição",
    habit_description="Sobre o hábito de Dormir",
    inputs=[
        InputDefinition(
            name="screen_time",
            label="Tempo de Tela",
            type=InputType.NUMBER,
            min_length=3,
            max_length=4,
            output_formatting=FormattingType.TIME,
        ),
        InputDefinition(
            name="bed_time", label="Início do Sono", type=InputType.DATETIME
        ),
        InputDefinition(
            name="wakeup_time", label="Fim do Sono", type=InputType.DATETIME
        ),
    ],
    outputs=CalculationFunctions.SLEEP_TIME_DIFFERENCE,
)

wisdom_segment = SegmentDefinition(
    public_name="Sabedoria",
    private_name="wisdom",
    description="A Sabedoria é...",
    modules=[
        navigator_module,
        alchemist_module,
        sentinel_module,
    ],
)
