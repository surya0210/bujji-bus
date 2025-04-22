from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class Seat:
    id: Optional[str] = field(init=False, default_factory=lambda:str(uuid.uuid4()))
    bus_id: str = ""
    seat_number: int = 0
    window: bool = False
    has_charging_port: bool = False
    is_reclinable: bool = False
    row_number: int = 0
    is_active:bool=True
    created_at: datetime = field(default_factory=datetime.now)
