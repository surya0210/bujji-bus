from datetime import date
from typing import List
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.passenger_schema import BookingPNRResponse, SeatBookingRequest, PassengerDetails
import uuid
from app.entities.booking import Booking
from app.entities.passengers import Passenger
import random


def book_seats(uow: UnitOfWork, booking_request: SeatBookingRequest):
   if len(booking_request.seat_numbers) != len(booking_request.passenger_details):
       raise ValueError("Mismatch between seats and passenger details.")
   pnr = str(uuid.uuid4())[:8].upper()
   bookings_ = []
   with uow:
       route = uow.routes.get_by_id(booking_request.route_id)
       if not route:
           raise ValueError("Route not found.")
       for seat_number, passenger in zip(booking_request.seat_numbers, booking_request.passenger_details):
           
           seat = uow.seats.get_by_route_and_number(route.bus_id, seat_number)
           
           if not seat:
               raise ValueError(f"Seat {seat_number} not found.")
           if uow.bookings.is_seat_booked(seat.id, booking_request.travel_date,booking_request.origin_stop_order,booking_request.destination_stop_order):
                raise ValueError(f"Seat {seat_number} already booked.")
           
           new_passenger = Passenger(
               
               name=passenger.name,
               age=passenger.age,
               gender=passenger.gender
           )
           uow.passengers.add(new_passenger)
           uow.session.flush()
           print(new_passenger)
           booking = Booking(
               route_id=booking_request.route_id,
               seat_id=seat.id,
               travel_date=booking_request.travel_date,
               passenger_id=new_passenger.id,
               pnr=pnr,
               start_stop_order=booking_request.origin_stop_order,
               end_stop_order=booking_request.destination_stop_order,
               operator_id=route.operator_id,
               amount=booking_request.amount,
               origin=booking_request.origin,
               destination=booking_request.destination
           )
           uow.bookings.add(booking)
           bookings_.append(booking)
       uow.commit()
       return {"pnr": pnr, "total_booked": len(bookings_)}
   

def get_bookings_by_pnr(uow: UnitOfWork, pnr: str) -> List[BookingPNRResponse]:

    with uow:

        bookings = uow.bookings.get_by_pnr(pnr)

        result = []

        for booking in bookings:

            seat = uow.seats.get_by_id(booking.seat_id)

            passenger = uow.passengers.get_by_id(booking.passenger_id)
            result.append(BookingPNRResponse(

                booking_id=booking.id,
                seat_number=seat.seat_number,
                travel_date=booking.travel_date,
                is_cancelled=booking.is_cancelled,
                origin=booking.origin,
                destination=booking.destination,
                amount=booking.amount,
                passenger_details=PassengerDetails(
                    id=passenger.id,
                    name=passenger.name,
                    age=passenger.age,
                    gender=passenger.gender,
                    

                )

            ))

        return result


def cancel_booking_by_passenger(uow: UnitOfWork, pnr:str, passenger_id: int, travel_date: date) -> dict:

    with uow:

        bookings = uow.bookings.get_by_passenger_and_date(passenger_id, travel_date,pnr)

        cancelled_count = 0

        for booking in bookings:

            if not booking.is_cancelled:

                booking.is_cancelled = True

                cancelled_count += 1

        uow.commit()

        return {"cancelled_count": cancelled_count}


def cancel_booking_by_pnr(uow: UnitOfWork, pnr: str) -> dict:

    with uow:

        bookings = uow.bookings.get_by_pnr(pnr)

        cancelled_count = 0

        for booking in bookings:

            if not booking.is_cancelled:

                booking.is_cancelled = True

                cancelled_count += 1

        uow.commit()

        return {"cancelled_count": cancelled_count}
 