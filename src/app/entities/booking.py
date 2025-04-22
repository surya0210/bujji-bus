from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from datetime import date

@dataclass
class Booking:
    id: Optional[int] = field(init=False, default=None)
    pnr: str
    passenger_id: int
    operator_id :int
    route_id: int
    origin:str
    destination:str
    seat_id: str
    start_stop_order: int
    end_stop_order: int
    travel_date:date
    amount:float=0.0
    booking_time: datetime = field(default_factory=datetime.now)
    status: bool = True
    is_cancelled:bool=False
    cancelled_reason:str=""
    
    