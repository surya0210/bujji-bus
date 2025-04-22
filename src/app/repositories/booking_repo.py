from datetime import date
from typing import List
from app.repositories.base import BaseRepository
from app.entities.booking import Booking
from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select,or_


class BookingRepository(BaseRepository[Booking]):
    def __init__(self,session:Session):
        super().__init__(session,Booking)
    
    def add(self, booking: Booking):
       self.session.add(booking)

    def get_by_route_and_date(self, route_id: int, travel_date: date) -> List[Booking]:
        stmt = (
            select(Booking)
            .where(
                
            )
        )
        result = self.session.query(Booking).filter_by(route_id = route_id,
                travel_date = travel_date).all()
        return result

    def is_seat_booked(self, seat_id: int, travel_date: date,start_order:int,end_order:int) -> bool:
       return self.session.query(Booking).filter(
        Booking.seat_id == seat_id,
        Booking.travel_date == travel_date,
        Booking.is_cancelled==False,
        Booking.end_stop_order > start_order,
        Booking.start_stop_order < end_order
    ).first() is not None

    def get_by_pnr(self, pnr: str) -> List[Booking]:
        return self.session.query(Booking).filter(Booking.pnr == pnr).all()

    def get_by_passenger_and_date(self, passenger_id: int, travel_date: date,pnr:str) -> List[Booking]:
        return (
            self.session.query(Booking)
            .filter(Booking.passenger_id == passenger_id, Booking.travel_date == travel_date,Booking.pnr==pnr)
            .all()
        )