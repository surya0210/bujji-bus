from dataclasses import asdict
from typing import List

from fastapi.exceptions import ValidationException
from app.schemas.route_stop_schema import RouteStopCreate, RouteStopResponse
from app.entities.route_stop_entity import RouteStop
from app.repositories.unit_of_work import UnitOfWork
from app.common.custom_exceptions import RouteNotFoundException
from datetime import datetime


def create_route_stop(route_id: int, stop_data: RouteStopCreate, uow: UnitOfWork) -> RouteStop:
    route = uow.routes.get_by_id(route_id)
    if not route:
        raise RouteNotFoundException(f"Route with ID {route_id} not found.")

    existing_stop = uow.route_stops.get_by_route_and_order(route_id, stop_data.stop_order)

    if existing_stop:

        raise Exception("Stop with this order already exists in the route.")


    route_stop = RouteStop(
        route_id=route_id,
        stop_name=stop_data.stop_name,
        stop_order=stop_data.stop_order,
        arrival_time=stop_data.arrival_time,
        departure_time=stop_data.departure_time,
        distance_from_start=stop_data.distance_from_start,
        price=stop_data.price

    )


    uow.route_stops.add(route_stop)

    uow.commit()

    return route_stop


def bulk_create_route_stops(

    route_id: int,

    stop_data_list: List[RouteStopCreate],

    uow: UnitOfWork

) -> List[RouteStopResponse]:

    created = []

    with uow:



        route = uow.routes.get_by_id(route_id)

        if not route:

            raise RouteNotFoundException(f"Route {route_id} not found")



        orders = [s.stop_order for s in stop_data_list]

        if len(orders) != len(set(orders)):

            raise ValidationException("Duplicate stop_order in request payload")



        existing_orders = {

            s.stop_order

            for s in uow.route_stops.list_by_route(route_id)

        }

        for data in stop_data_list:

            if data.stop_order in existing_orders:

                continue  

            stop = RouteStop(

                route_id=route_id,

                stop_name=data.stop_name,

                stop_order=data.stop_order,

                arrival_time=data.arrival_time,

                departure_time=data.departure_time,

                distance_from_start=data.distance_from_start,

                price=getattr(data, "price", 0.0)

            )

            uow.route_stops.add(stop)
            uow.session.flush()
            print(stop)
            created.append(RouteStopResponse(**asdict(stop)))

        uow.commit()

        return created

def update_route_stop(route_stop_id: int, stop_data: RouteStopCreate, uow: UnitOfWork) -> RouteStop:

    route_stop = uow.route_stops.get_by_id(route_stop_id)

    if not route_stop:

        raise RouteNotFoundException(f"Route stop with ID {route_stop_id} not found.")

    # Update fields

    route_stop.stop_name = stop_data.stop_name

    route_stop.stop_order = stop_data.stop_order

    route_stop.arrival_time = stop_data.arrival_time

    route_stop.departure_time = stop_data.departure_time

    route_stop.distance_from_start = stop_data.distance_from_start



    uow.commit()

    return route_stop



def delete_route_stop(route_stop_id: int, uow: UnitOfWork) -> None:

    route_stop = uow.route_stops.get_by_id(route_stop_id)

    if not route_stop:

        raise RouteNotFoundException(f"Route stop with ID {route_stop_id} not found.")


    uow.route_stops.delete(route_stop)

    uow.commit()



def get_route_stop(route_stop_id: int, uow: UnitOfWork) -> RouteStop:

    route_stop = uow.route_stops.get_by_id(route_stop_id)

    if not route_stop:

        raise RouteNotFoundException(f"Route stop with ID {route_stop_id} not found.")

    return route_stop 