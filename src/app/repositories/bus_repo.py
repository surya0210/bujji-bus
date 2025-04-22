from app.repositories.base import BaseRepository
from app.entities.bus_entity import Bus
from sqlalchemy.orm import Session


class BusRepository(BaseRepository[Bus]):
    def __init__(self, session: Session):
        super().__init__(session, Bus)

    def add(self, bus: Bus):
        self.session.add(bus)

    def get_by_id(self, bus_id: str):
        return self.session.query(Bus).filter(Bus.id == bus_id).first()
    
    def get_by_operator_and_number(self, bus_number: str ,operator_id:str):
        return self.session.query(Bus).filter(Bus.bus_number == bus_number, Bus.operator_id==operator_id).first()

    def delete(self, bus: Bus):
        self.session.delete(bus)
        
    def list_by_operator(self, operator_id: str):
       return self.session.query(Bus).filter(Bus.operator_id == operator_id).all()
