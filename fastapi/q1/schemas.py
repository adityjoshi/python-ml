from pydantic import BaseModel, ConfigDict, Field
from typing import List


class DepotCreate(BaseModel):
    name: str = Field(..., min_length=1)
    region: str = Field(..., min_length=1)


class DepotOut(BaseModel):
    id: int
    name: str
    region: str

    model_config = ConfigDict(from_attributes=True)


class VehicleCreate(BaseModel):
    plate_number: str = Field(..., min_length=1)
    vehicle_type: str = Field(..., min_length=1)
    mileage: int = Field(..., ge=0)


class VehicleOut(BaseModel):
    id: int
    plate_number: str
    vehicle_type: str
    mileage: int
    model_config = ConfigDict(from_attributes=True)


class DepotWithVehicles(BaseModel):
    id: int
    name: str
    region: str
    vehicles: List[VehicleOut]
    model_config = ConfigDict(from_attributes=True)
