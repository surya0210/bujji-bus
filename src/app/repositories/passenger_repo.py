from app.repositories.base import BaseRepository
from app.entities.passengers import Passenger
from sqlalchemy.orm import Session


class PassengerRepository(BaseRepository[Passenger]):
    def __init__(self,session:Session):
        super().__init__(session,Passenger)

    def get_by_id(self, id: str) -> Passenger | None:
        return self.session.query(Passenger).filter(Passenger.id == id).first()