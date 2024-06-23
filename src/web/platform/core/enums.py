class InputType:
    TEXT = "text"
    DATE = "date"
    RANGE = "range"
    NUMBER = "number"
    TOGGLE = "toggle"
    MULTI = "multiple-alternative"
    SINGLE = "single-alternative"
    TEXTA_AREA = "text-area"
    DATETIME = "datetime-local"


class FormattingType:
    RAW = "raw"
    TIME = "time"
    WEIGHT = "weight"
    DISTANCE = "distance"
    CALORIES = "calories"
    MONETARY = "monetary"
    PERCENTAGE = "percentage"


class SectionType:
    BASIC = "basic"
    WISDOM = "wisdom"
    STABILITY = "stability"
    STRENGTH = "strength"
    KINDNESS = "kindness"
    DEVOTION = "devotion"


class DefinitionType:
    PAGE = "page"
    SECTION = "section"
    BOX = "box"
    INPUT = "input"
    BUTTON = "button"

    @classmethod
    def get_all(cls):
        return [value for name, value in vars(cls).items() if not name.startswith("__")]


class Icon:
    PILLS = "fa-solid fa-pills"
    NOTES = "fa-solid fa-notes"
    EXCELENCE = "fa-solid fa-star"
    POWER_OFF = "fa-solid fa-power-off"
    CALENDAR_CHECK = "fa-regular fa-calendar-check"
