from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
import uuid

class SeatBase(BaseModel):
   seat_number: int
   window: bool = False
   has_charging_port: bool = False
   is_reclinable: bool = False
   row_number: int
   class Config:
       orm_mode = True  

class SeatResponse(SeatBase):
   bus_id: str
   id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
   # created_at: datetime = Field(default_factory=datetime.now)
   is_active:bool=True
   class Config:
       orm_mode = True 



class SeatUpdate(BaseModel):
   seat_number: Optional[str]=None
   has_charging_port: Optional[bool]=None
   is_reclinable: Optional[bool]=None