from enum import StrEnum, auto

class Destruction(StrEnum):
    DESTRUCTIBLE_SOFT = auto()
    DESTRUCTIBLE_HARD = auto()
    SOLID = auto()
    PASSTHROUGH = auto()
    TOP_LAYER = auto()