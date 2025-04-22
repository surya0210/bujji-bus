from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from app.entities.seat_entity import Seat
import uuid

@dataclass
class Bus:
   id: Optional[str] = field(init=False, default_factory=lambda:str(uuid.uuid4()))
   operator_id: str = ""
   bus_number: str = ""
   total_seats: int = 0
   bus_type: str = ""
   model: str = ""
   has_wifi: bool = False
   has_ac: bool = False
   has_toilet: bool = False
   last_service_date: datetime = field(default_factory=datetime.now)
   next_service_due: datetime =field(default_factory=datetime.now) 
   active: bool = True
   created_at: datetime = field(default_factory=datetime.now)
   seats: List["Seat"] = field(default_factory=list)