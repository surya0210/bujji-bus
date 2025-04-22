from typing import List

from fastapi.exceptions import ValidationException
from app.entities.seat_entity import Seat
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.seat_schema import SeatBase, SeatResponse, SeatUpdate
from app.common.custom_exceptions import BusNotFoundException, SeatNotFoundException


def create_seat(bus_id: str, seat_data: SeatBase, uow: UnitOfWork) -> Seat:
    with uow:
        bus = uow.buses.get_by_id(bus_id)
        if not bus:
            raise BusNotFoundException(f"Bus {bus_id} not found")
        if uow.seats.get_by_id_and_number(bus_id, seat_data.seat_number):
            raise Exception(f"Seat {seat_data.seat_number} already exists in this bus")
        seat = Seat(
            bus_id=bus_id,
            seat_number=seat_data.seat_number,
            window=seat_data.window,
            has_charging_port=seat_data.has_charging_port,
            is_reclinable=seat_data.is_reclinable,
            row_number=seat_data.row_number,
        )
        uow.seats.add(seat)
        uow.commit()
        return None


def update_seat(seat_id: str, data: SeatUpdate, uow: UnitOfWork):
    with uow:
        seat = uow.seats.get_by_id(seat_id)
        if not seat:
            raise SeatNotFoundException("Seat not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(seat, key, value)
        uow.commit()
        return None


def delete_seat(seat_id: str, uow: UnitOfWork):
    with uow:
        seat = uow.seats.get_by_id(seat_id)
        print(seat)
        if not seat:
            raise SeatNotFoundException("Seat not found")
        uow.seats.delete(seat)
        uow.commit()


def list_seats_by_bus(operator_id: str, bus_id: str, uow: UnitOfWork):
    with uow:
        seats = uow.buses.get_by_id(bus_id)
        if not seats:
            raise BusNotFoundException(f"Seats with Bus ID {bus_id} not found")
        seats = uow.seats.get_by_bus_id(bus_id)
        return [
            SeatResponse(
                bus_id=seat.bus_id,
                has_charging_port=seat.has_charging_port,
                id=seat.id,
                is_active=seat.is_active,
                is_reclinable=seat.is_reclinable,
                row_number=seat.row_number,
                seat_number=seat.seat_number,
                window=seat.window,
            )
            for seat in seats
        ]


def bulk_create_seats(
   bus_id: str,
   seat_data_list: List[SeatBase],
   uow: UnitOfWork
) -> List[SeatResponse]:
   created = []
   with uow:

       bus = uow.buses.get_by_id(bus_id)
       if not bus:
           raise ValidationException(f"Bus {bus_id} not found")

       numbers = [s.seat_number for s in seat_data_list]
       if len(numbers) != len(set(numbers)):
           raise ValidationException("Duplicate seat_number in request payload")

       existing = {
           s.seat_number
           for s in uow.seats.get_by_bus_id(bus_id)
       }
       for data in seat_data_list:
           if data.seat_number in existing:
               continue 
           seat = Seat(
               bus_id=bus_id,
               seat_number=data.seat_number,
               window=data.window,
               is_reclinable=getattr(data, "is_reclinable", False),
               has_charging_port=getattr(data, "has_charging_port", False),
               row_number=getattr(data, "row_number", 0),
           )
           uow.seats.add(seat)
           created.append(seat)
       uow.commit()
       return [SeatResponse.model_validate(s, from_attributes=True) for s in created]