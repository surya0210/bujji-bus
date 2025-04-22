from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from app.entities.bus_entity import Bus
from app.entities.route_entity import Route
import uuid

@dataclass
class Operator:
   id: str = field(init=False, default_factory=lambda:str(uuid.uuid4()))
   name: str = ""
   email: str = ""
   password_hash: str = ""
   is_active: bool =False
   created_at: datetime = field(default_factory=datetime.now)
   buses: List["Bus"] = field(default_factory=list)
   routes: List["Route"] = field(default_factory=list)
   
