from typing import List
from app.entities.bus_entity import Bus
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.bus_schema import BusCreate, BusCreateResponse, BusResponse, BusUpdate
from app.common.custom_exceptions import (
    BusNotFoundException,
    OperatorNotFoundException,
    BusAlreadyExistsException,
)
from datetime import datetime


def create_bus(
    operator_id: str, bus_data: BusCreate, uow: UnitOfWork
) -> BusCreateResponse:

    with uow:

        operator = uow.operators.get(operator_id)

        if not operator:

            raise OperatorNotFoundException(f"Operator with ID {operator_id} not found")

        existing_bus = uow.buses.get_by_operator_and_number(
           bus_data.bus_number, operator_id, 
        )

        print(existing_bus)

        if existing_bus:

            raise BusAlreadyExistsException(bus_data.bus_number)

        new_bus = Bus(
            operator_id=operator_id,
            bus_number=bus_data.bus_number,
            total_seats=bus_data.total_seats,
            bus_type=bus_data.bus_type,
            model=bus_data.model,
            has_wifi=bus_data.has_wifi,
            has_ac=bus_data.has_ac,
            has_toilet=bus_data.has_toilet,
            last_service_date=bus_data.last_service_date,
            next_service_due=bus_data.next_service_due,
        )

        uow.buses.add(new_bus)

        uow.commit()

        return BusCreateResponse(
            id=new_bus.id,
            operator_id=new_bus.operator_id,
            bus_number=new_bus.bus_number,
            total_seats=new_bus.total_seats,
            active=new_bus.active,
            created_at=new_bus.created_at,
        )


def list_buses_by_operator(operator_id: str, uow: UnitOfWork) -> List[BusResponse]:
    with uow:
        operator = uow.operators.get(operator_id)
        if not operator:
            raise OperatorNotFoundException(f"Operator with ID {operator_id} not found")
        buses = uow.buses.list_by_operator(operator_id)
        return [
            BusResponse(
                id=bus.id,
                operator_id=bus.operator_id,
                bus_number=bus.bus_number,
                total_seats=bus.total_seats,
                bus_type=bus.bus_type,
                model=bus.model,
                has_wifi=bus.has_wifi,
                has_ac=bus.has_ac,
                has_toilet=bus.has_toilet,
                last_service_date=bus.last_service_date,
                next_service_due=bus.next_service_due,
                active=bus.active,
                created_at=bus.created_at,
            )
            for bus in buses
        ]


def update_bus(operator_id: str, bus_id: str, update_data: BusUpdate, uow: UnitOfWork):
    with uow:
        bus = uow.buses.get_by_id(bus_id)
        if not bus or bus.operator_id != operator_id:
            raise BusNotFoundException(bus_id)
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(bus, field, value)
        uow.commit()

        return None
        

def delete_bus(operator_id: str, bus_id: str, uow: UnitOfWork):
   with uow:
       bus = uow.buses.get_by_id(bus_id)
       if not bus or bus.operator_id != operator_id:
           raise BusNotFoundException(bus_id)
       uow.session.delete(bus)
       uow.commit()