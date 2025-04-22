from app.repositories.base import BaseRepository
from app.entities.route_entity import Route
from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select
from typing import List


class RouteRepository(BaseRepository[Route]):
    def __init__(self,session:Session):
        super().__init__(session,Route)
    def add(self, route):
       self.session.add(route)
    def get_by_id(self, route_id: int):
        
        return self.session.query(Route).filter_by(id=route_id).first()
    def list_by_operator(self, operator_id: int):
        return self.session.query(Route).filter_by(operator_id=operator_id).all()
    def delete(self, route):
        self.session.delete(route)
    def get_by_origin_and_destination(self, operator_id:str,bus_id:str,origin: str, destination: str) -> Route:
        return self.session.query(Route).filter(Route.operator_id==operator_id,Route.bus_id == bus_id,Route.origin == origin, Route.destination == destination).first()
    def get_by_bus_and_operator(self,bus_id: int, operator_id: int) -> Route:
        return self.session.query(Route).filter(Route.bus_id == bus_id, Route.operator_id == operator_id).first()
    
    def get_active_routes_with_stops(self) -> List[Route]:
       stmt = select(Route).where(Route.is_active == True).options(selectinload(Route.stops))
       return self.session.execute(stmt).scalars().all()
