from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.route_stop_schema import RouteStopResponse

class RouteCreate(BaseModel):
   bus_id: str
   operator_id:str
   origin: str
   destination: str
   distance_km: int
   route_time: int
   is_active: Optional[bool] = True

class RouteUpdate(BaseModel):
   bus_id: Optional[str] = None
   origin: Optional[str] = None
   destination: Optional[str] = None
   distance_km: Optional[int] = None
   route_time: Optional[int] = None
   is_active: Optional[bool] = None

class RouteResponse(BaseModel):
   id: int
   operator_id: str
   bus_id: str
   origin: str
   destination: str
   distance_km: int
   route_time: int
   is_active: bool
   created_at: datetime
   stops: List[RouteStopResponse] = []
   class Config:
       orm_mode = True