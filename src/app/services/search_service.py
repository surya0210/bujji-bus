from datetime import date
from typing import List
from app.schemas.search_schema import SearchRequest, SearchResponse
from app.common.helper import (
   calculate_duration_minutes,
   time_range_filter,
   get_available_seats,
   calculate_price,
)
from app.repositories.unit_of_work import UnitOfWork

import pprint
def search_routes(search: SearchRequest,uow: UnitOfWork, ) -> List[SearchResponse]:
   results = []
   with uow:
      routes =  uow.routes.get_active_routes_with_stops()
      for route in routes:
         route_stops = uow.route_stops.get_by_route_id(route.id)         
         ordered_stops = sorted(route_stops, key=lambda x: x.stop_order)
         origin_stop = next((s for s in ordered_stops if s.stop_name == search.origin), None)
         destination_stop = next((s for s in ordered_stops if s.stop_name == search.destination), None)
         if not origin_stop or not destination_stop:
            continue
         if origin_stop.stop_order >= destination_stop.stop_order:
            continue
         bus =  uow.buses.get_by_id(route.bus_id)
         if not bus or not bus.active:
            continue
         #   AC filter
         if search.ac is not None and bus.has_ac != search.ac:
            continue
    #        # Start time range filter
         if search.start_time_range and not time_range_filter(origin_stop.departure_time, search.start_time_range):
            continue
    #        # Fetch seats and bookings
         seats = uow.seats.get_by_bus_id(bus.id)
         
         bookings = uow.bookings.get_by_route_and_date(route.id, search.travel_date)
         
         available_seats = get_available_seats(seats, bookings, origin_stop.stop_order, destination_stop.stop_order)
         if not len(available_seats)>=search.no_of_seats:
            continue
         #   Price logic
         price = calculate_price(ordered_stops, search.origin, search.destination)
         
           # Max price filter
         if search.max_price is not None and price > search.max_price:
            continue
         duration = calculate_duration_minutes(
            origin_stop.departure_time, destination_stop.arrival_time
         )

         operator_data=uow.operators.get_by_id(route.operator_id)
         results.append(
               SearchResponse(
                   route_id=route.id,
                   bus_id=bus.id,
                   operator_id=route.operator_id,
                   operator_name=operator_data.name,
                   origin=search.origin,
                   destination=search.destination,
                   departure_time=origin_stop.departure_time,
                   arrival_time=destination_stop.arrival_time,
                   duration_minutes=duration,
                   price=price,
                   available_seats=len(available_seats),
                   bus_type=bus.bus_type,
                   has_ac=bus.has_ac,
                   has_wifi=bus.has_wifi,
                   has_toilet=bus.has_toilet,
                   bus_model=bus.model,
                   travel_date=search.travel_date,
                   origin_stop_order=origin_stop.stop_order, 
                   destination_stop_order=destination_stop.stop_order
               )
           )
   return results

# def get_seat_map_for_route(route_id: int, travel_date: date, uow: UnitOfWork):
#    # Get route details
#    route = uow.routes.get_by_id(route_id)
#    if not route:
#        raise ValueError("Route not found")

#    seats = uow.seats.get_by_bus_id(route.bus_id)
 
#    booked_seats = uow.bookings.get_by_route_and_date(route_id=route_id,travel_date=travel_date)
#    booked_seat_ids = {booking.seat_id for booking in booked_seats}
#    seat_map = []
#    for seat in seats:
#        seat_map.append({
#            "seat_id": seat.id,
#            "seat_number": seat.seat_number,
#            "status": "booked" if seat.id in booked_seat_ids else "available",
#        })
#    return seat_map



def get_seat_map_for_route(route_id: int, travel_date: date, start_order: int, end_order: int, uow: UnitOfWork):
   # Get route details
   route = uow.routes.get_by_id(route_id)
   if not route:
       raise ValueError("Route not found")
   seats = uow.seats.get_by_bus_id(route.bus_id)
   # Get all active bookings (not cancelled)
   bookings = uow.bookings.get_by_route_and_date(route_id=route_id, travel_date=travel_date)
   active_bookings = [b for b in bookings if not b.is_cancelled]
   # Determine seat availability
   seat_map = []
   for seat in seats:
       is_booked = False
       for booking in active_bookings:
           if booking.seat_id == seat.id:
               # Check for overlapping segment
               if not (booking.end_stop_order <= start_order or booking.start_stop_order >= end_order):
                   is_booked = True
                   break
       seat_map.append({
           "seat_id": seat.id,
           "seat_number": seat.seat_number,
           "status": "booked" if is_booked else "available",
       })
   return seat_map