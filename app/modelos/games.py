from typing import Any

from pydantic import BaseModel
from enum import Enum

class Gender(str, Enum):
    action = "action"
    adventure =  "adventure"
    rpg = "rpg"

    @classmethod
    def _missing_(cls, value: Any):
        """Converte entrada para lowercase e tenta encontrar o enum"""
        if isinstance(value, str):
            value_lower = value.lower()
            for member in cls:
                if member.value.lower() == value_lower:
                    return member
        raise ValueError(f"'{value}' não é um gênero válido. Use: action, adventure, rpg")

class Games(BaseModel):
    id_: int
    name: str
    gender: Gender

class GamesMakeUpdate(BaseModel):
    name: str
    gender: Gender



