from app.repositories.base import BaseRepository
from app.entities.route_stop_entity import RouteStop
from sqlalchemy.orm import Session


class RouteStopRepository(BaseRepository[RouteStop]):
    def __init__(self,session:Session):
        super().__init__(session,RouteStop)
    def add(self, stop):
        self.session.add(stop)
    def get_by_id(self, stop_id: int):
        return self.session.query(RouteStop).filter_by(id=stop_id).first()
    def list_by_route(self, route_id: int):
        return self.session.query(RouteStop).filter_by(route_id=route_id).order_by(RouteStop.stop_order).all()  
    def get_by_route_id(self, route_id: int) -> list:
       return self.session.query(RouteStop).filter(RouteStop.route_id == route_id).all()
    def get_by_route_and_order(self, route_id: int, stop_order: int) -> RouteStop:
        return self.session.query(RouteStop).filter(RouteStop.route_id == route_id, RouteStop.stop_order == stop_order).first()
    def get_all(self) -> list:
        return self.session.query(RouteStop).all()
    def delete(self, stop):
        self.session.delete(stop)