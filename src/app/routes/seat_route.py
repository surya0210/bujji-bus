from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.common.session_maker import get_session
from app.repositories.unit_of_work import UnitOfWork
from app.schemas.seat_schema import SeatBase, SeatResponse, SeatUpdate
from app.services.seat_service import bulk_create_seats, create_seat, delete_seat, list_seats_by_bus, update_seat
from app.common.custom_exceptions import BusNotFoundException, SeatNotFoundException
from app.common.error_messages import ErrorMessages

seat_router = APIRouter(prefix="/operator/bus/{bus_id}/seat", tags=["seat"])
@seat_router.post("/add",status_code=status.HTTP_201_CREATED)
def create_seat_endpoint(bus_id: str, seat_data: SeatBase, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       create_seat(bus_id, seat_data, uow)
       return {"deatil":"Seat Created"}
   except BusNotFoundException as e:
       raise HTTPException(status_code=404, detail=str(e))
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))


@seat_router.post("/bulk", response_model=List[SeatResponse], status_code=status.HTTP_201_CREATED)
def create_seats_bulk(
   bus_id: str,
   seats: List[SeatBase],
   session: Session = Depends(get_session)
):
   uow = UnitOfWork(session)
   try:
       return bulk_create_seats(bus_id, seats, uow)
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))
   
@seat_router.patch("/update/{seat_id}",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
def patch_seat(bus_id:str,seat_id: str, data: SeatUpdate, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       update_seat(seat_id, data, uow)
   except SeatNotFoundException as e:
       raise HTTPException(status_code=404, detail=str(e))
   
@seat_router.delete("/delete/{seat_id}",status_code=status.HTTP_204_NO_CONTENT,response_model=None)
def remove_seat(bus_id:str,seat_id: str, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       delete_seat(seat_id, uow)
       return {"detail": "Seat deleted successfully"}
   except SeatNotFoundException as e:
       print(e)
       raise HTTPException(status_code=404, detail=ErrorMessages.INTERNAL_SERVER_ERROR)
   

@seat_router.get("/get-all", response_model=List[SeatResponse])
def get_operator_buses(operator_id: str, bus_id:str,session: Session = Depends(get_session)):
    try:
        uow = UnitOfWork(session)
        return list_seats_by_bus(operator_id, bus_id,uow)
    except BusNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=ErrorMessages.INTERNAL_SERVER_ERROR)


