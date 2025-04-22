from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

class SearchRequest(BaseModel):
   origin: str
   destination: str
   travel_date: date
   ac: Optional[bool] = None
   wifi: Optional[bool] = None
   toilet: Optional[bool] = None
   start_time_range: Optional[str] = None  # morning, afternoon, evening, night
   max_price: Optional[int] = None
   sort_by: Optional[str] = None  # 'price', 'departure_time'
   page: Optional[int] = 1
   page_size: Optional[int] = 10
   include_seat_map: Optional[bool] = False  # If True, seat map is included in results
   no_of_seats:Optional[int]=1

class SearchResponse(BaseModel):
   route_id: int
   bus_id: str
   operator_id: str
   operator_name:str
   origin: str
   destination: str
   departure_time: time
   arrival_time: time
   duration_minutes: int
   price: int
   available_seats: int
   bus_type: str
   has_ac: bool
   has_wifi: bool
   has_toilet: bool
   bus_model: str
   travel_date:date
   origin_stop_order:int
   destination_stop_order:int
   seat_map: Optional[List[dict]] = None  # If requested


class SeatMapResponse(BaseModel):
   seat_id: str
   seat_number: int
   status: str  # 'available' or 'booked'
class PassengerDetails(BaseModel):
   seat_id: int
   passenger_name: str
   age: int
   gender: str

class BookingRequest(BaseModel):
   route_id: int
   travel_date: date
   seats: List[PassengerDetails]

class BookingResponse(BaseModel):
   booking_id: int
   route_id: int
   seat_id: int
   passenger_name: str
   travel_date: date
   status: str  # 'confirmed' or 'pending'