from app.repositories.unit_of_work import UnitOfWork
from app.schemas.route_schema import RouteCreate, RouteResponse
from app.entities.route_entity import Route
from app.common.custom_exceptions import RouteNotFoundException
from datetime import datetime


def create_route(route_data: RouteCreate, uow: UnitOfWork) -> RouteResponse:
    existing_route = uow.routes.get_by_bus_and_operator(
        route_data.operator_id,route_data.bus_id,
    )
    if existing_route:
        raise Exception("Route already exists.")

    route = Route(
        operator_id=route_data.operator_id,
        bus_id=route_data.bus_id,
        origin=route_data.origin,
        destination=route_data.destination,
        distance_km=route_data.distance_km,
        route_time=route_data.route_time,
        is_active=route_data.is_active,
    )


    uow.routes.add(route)
    uow.commit()


    return RouteResponse.model_validate(route, from_attributes=True)

def update_route(route_id: int, route_data: RouteCreate, uow: UnitOfWork) -> RouteResponse:
    route = uow.routes.get_by_id(route_id)
    if not route:
        raise RouteNotFoundException(f"Route with ID {route_id} not found.")

    route.operator_id = route_data.operator_id
    route.bus_id = route_data.bus_id
    route.origin = route_data.origin
    route.destination = route_data.destination
    route.distance_km = route_data.distance_km
    route.route_time = route_data.route_time
    route.is_active = route_data.is_active
    uow.commit()
    return RouteResponse.model_validate(route, from_attributes=True)



def delete_route(route_id: int, uow: UnitOfWork) -> None:
    route = uow.routes.get_by_id(route_id)
    if not route:
        raise RouteNotFoundException(f"Route with ID {route_id} not found.")
    uow.routes.delete(route)
    uow.commit()


def get_route(route_id: int, uow: UnitOfWork) -> RouteResponse:
    route = uow.routes.get_by_id(route_id)
    if not route:
        raise RouteNotFoundException(f"Route with ID {route_id} not found.")
    return RouteResponse.model_validate(route, from_attributes=True)


def get_routes_for_bus(bus_id: int, uow: UnitOfWork) -> list:
   routes = uow.routes.get_all_by_bus_id(bus_id)
   return [RouteResponse.model_validate(route, from_attributes=True) for route in routes]
