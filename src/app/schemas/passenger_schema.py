from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class PassengerDetailsInput(BaseModel):
   name: str
   age: int
   gender: str

class PassengerDetails(PassengerDetailsInput):
   id:Optional[int]=0



class SeatBookingRequest(BaseModel):
   route_id: int
   travel_date: date
   origin:str
   destination:str
   origin_stop_order:int
   destination_stop_order:int
   seat_numbers: List[str]
   amount:float
   passenger_details: List[PassengerDetailsInput]

class SeatBookingResponse(BaseModel):
   pnr:str
   total_booked:int


class BookingPNRResponse(BaseModel):
   booking_id: int
   seat_number: int
   travel_date: date
   origin:str
   destination:str
   amount:float
   is_cancelled: bool=False
   passenger_details: PassengerDetails

class CancelPassengerRequest(BaseModel):
   pnr:str
   passenger_id: int
   travel_date: date