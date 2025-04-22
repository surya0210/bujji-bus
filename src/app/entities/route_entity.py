from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from app.entities.route_stop_entity import RouteStop


@dataclass
class Route:
    id: Optional[int] = field(init=False, default=None)
    operator_id: Optional[str] = ""
    bus_id: Optional[str] = ""
    origin: str = ""
    destination: str = ""
    distance_km: int = 0
    route_time: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    stops: List["RouteStop"] = field(default_factory=list)
