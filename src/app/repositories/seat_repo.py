from typing import Optional
from app.repositories.base import BaseRepository
from app.entities.seat_entity import Seat
from sqlalchemy.orm import Session


class SeatRepository(BaseRepository[Seat]):
    def __init__(self,session:Session):
        super().__init__(session,Seat)
    def add(self, seat: Seat):
        self.session.add(seat)
    def get_by_bus_id(self, bus_id: str) -> list[Seat]:
        return self.session.query(Seat).filter(Seat.bus_id == bus_id).all()
    def get_by_id(self, seat_id: str) -> Seat | None:
        return self.session.query(Seat).filter(Seat.id == seat_id).first()
    def delete(self, seat: Seat):
        self.session.delete(seat)
    def get_by_id_and_number(self,bus_id:str,seat_number: str) -> Seat | None:
        return self.session.query(Seat).filter(Seat.bus_id==bus_id ,Seat.seat_number == seat_number).first()
    def get_by_route_and_number(self, bus_id: str, seat_number: str) -> Optional[Seat]:
       return self.session.query(Seat).filter(
           Seat.bus_id == bus_id,
           Seat.seat_number == seat_number
       ).first()