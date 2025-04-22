from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BusCreate(BaseModel):
   
   bus_number: str
   total_seats: int
   bus_type: str
   model: str
   has_wifi: bool = False
   has_ac: bool = False
   has_toilet: bool = False
   last_service_date: Optional[datetime] = Field(default_factory=datetime.now)
   next_service_due: Optional[datetime] = Field(default_factory=datetime.now)
   active: bool = True
   
   class Config:
       orm_mode = True


class BusCreateResponse(BaseModel):
    operator_id: str
    id: str
    created_at: datetime



class BusResponse(BaseModel):
   id: str
   operator_id: str
   bus_number: str
   total_seats: int
   bus_type: str
   model: str
   has_wifi: bool
   has_ac: bool
   has_toilet: bool
   last_service_date: datetime
   next_service_due: datetime
   active: bool
   created_at: datetime
   class Config:
       orm_mode = True




class BusUpdate(BaseModel):
    bus_number: Optional[str] = None
    total_seats: Optional[int] = None
    bus_type: Optional[str] = None
    model: Optional[str] = None
    has_wifi: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_toilet: Optional[bool] = None
    last_service_date: Optional[datetime] = None
    next_service_due: Optional[datetime] = None
    active: Optional[bool] = None 