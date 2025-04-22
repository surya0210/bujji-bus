from dataclasses import dataclass, field
from datetime import time
from typing import Optional

@dataclass
class RouteStop:
   id: Optional[int] = field(init=False, default=None)
   route_id: int
   stop_name: str
   stop_order: int
   arrival_time: Optional[time] = None
   departure_time: Optional[time] = None
   distance_from_start: int = 0
   price:float=0.0