from pydantic import BaseModel

from typing import Optional

from datetime import time


class RouteStopCreate(BaseModel):

    stop_name: str

    stop_order: int

    arrival_time: Optional[time] = None

    departure_time: Optional[time] = None

    distance_from_start: Optional[int] = 0
    price:float


class RouteStopUpdate(BaseModel):

    stop_name: Optional[str] = None

    stop_order: Optional[int] = None

    arrival_time: Optional[time] = None

    departure_time: Optional[time] = None

    distance_from_start: Optional[int] = None
    price:Optional[float]=0.0

class RouteStopResponse(BaseModel):

    id: int

    route_id: int

    stop_name: str

    stop_order: int

    arrival_time: Optional[time] = None

    departure_time: Optional[time] = None

    distance_from_start: int
    price:float

    class Config:

        orm_mode = True 