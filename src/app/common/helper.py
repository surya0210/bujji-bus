from datetime import date, datetime, time
from typing import List, Optional
from app.entities.seat_entity import Seat
from app.entities.booking import Booking
import pprint
def time_range_filter(departure_time: time, window: Optional[str]) -> bool:
   if not window:
       return True
   time_windows = {
       "morning": (time(5, 0), time(12, 0)),
       "afternoon": (time(12, 0), time(17, 0)),
       "evening": (time(17, 0), time(21, 0)),
       "night": (time(21, 0), time(23, 59)),
   }
   start, end = time_windows.get(window.lower(), (None, None))
   if not start or not end:
       return True
   print(start <= departure_time,start <= departure_time<=end)
   return start <= departure_time <= end

def calculate_duration_minutes(start: time, end: time) -> int:
   
   start_dt = datetime.combine(datetime.today(), start)
   end_dt = datetime.combine(datetime.today(), end)
   if end_dt < start_dt:
       end_dt = end_dt.replace(day=end_dt.day + 1)  # next day arrival
   return int((end_dt - start_dt).total_seconds() // 60)

def get_available_seats(seats: List[Seat], bookings: List[Booking], start_order: int, end_order: int) -> List[Seat]:
   available_seats = []
   for seat in seats:
       booked = False
       for booking in bookings:
           if booking.is_cancelled:
               continue
           if booking.seat_id == seat.id:
               # If overlapping segments
               if not (booking.end_stop_order <= start_order or booking.start_stop_order >= end_order):
                   booked = True
                   break
       if not booked:
           available_seats.append(seat)
   return available_seats

def calculate_price(
   route_stops, origin: str, destination: str, price_per_km: float = 1.0
) -> int:
   start = next((s for s in route_stops if s.stop_name == origin), None)
   end = next((s for s in route_stops if s.stop_name == destination), None)
   if not start or not end:
       return 0
   return max(1, int(end.price - start.price))

