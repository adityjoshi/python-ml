from pydantic import BaseModel, ConfigDict, Field
from typing import List

class LotCreate(BaseModel):
    name: str = Field(...,min_length=1)
    zone: str = Field(...,min_length=1)


class LotOut(BaseModel):
    id: int
    name: str
    zone: str

class SlipCreate(BaseModel):
    ticket_code: str = Field(...,min_length=1)
    vehicle_class: str = Field(...,min_length=1)
    parked_minutes: int = Field(...,ge=1)

class SlipTransfer(BaseModel):
    target_lot_id: int

class SlipOut(BaseModel):
    id: int
    ticket_code: str
    vehicle_class: str
    parked_minutes: int
    
class LotWithSlips(BaseModel):
    id: int
    name: str
    zone: str
    slips: List[SlipOut]



