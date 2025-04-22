from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from app.entities.booking import Booking
@dataclass
class Passenger:
   id: Optional[int] = field(init=False, default=None)
   name: str = ""
   gender: str = ""
   age:int=0
   # phone_number: str = ""
   # password_hash: str = ""
   # created_at: datetime = field(default_factory=datetime.now())
   # bookings: List["Booking"] = field(default_factory=list)
   # last_login_time:datetime = field(default_factory=datetime.now())