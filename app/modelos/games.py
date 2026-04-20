from pydantic import BaseModel
from enum import Enum

class Gender(str, Enum):
    action = "action"
    adventure =  "adventure"
    rpg = "rpg"

class Games(BaseModel):
    id_: int
    name: str
    gender: Gender

class GamesMakeUpdate(BaseModel):
    name: str
    gender: Gender



