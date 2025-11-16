from pydantic import BaseModel
from enum import StrEnum


class ResidentType(StrEnum):
    LIBERTI = "liberti"
    PLEBEIAN = "plebeian"
    EQUITES = "equites"
    PATRICIAN = "patrician"


class Workers(BaseModel):
    type: ResidentType
    count: int


class Resource(BaseModel):
    name: str
    production_ratio: float
    needs: list[str]
    workforce: list[Workers] = []


type ProductionChain = dict[str, float]
