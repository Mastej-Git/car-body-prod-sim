from enum import Enum

class CupMaterial(Enum):
    ALUMINUM = "Aluminum"
    STAINLESS_STEEL = "Stainless steel"
    POLICARBONATE = "Policarbonate"

class ScreenTypes(Enum):
    RESISTIVE = "Resistive"
    CAPACITIVE = "Capacitive"
    PROJECTED_CAPACITIVE = "Projected capacitive"