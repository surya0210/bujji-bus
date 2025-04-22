from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.services.route_stop_service import bulk_create_route_stops, create_route_stop, update_route_stop, delete_route_stop, get_route_stop
from app.schemas.route_stop_schema import RouteStopCreate, RouteStopResponse
from app.repositories.unit_of_work import UnitOfWork
from app.common.custom_exceptions import  RouteNotFoundException
from sqlalchemy.orm import Session
from app.common.session_maker import get_session

route_stop_router = APIRouter(prefix="/operator/route-stop", tags=['route-stop'])

@route_stop_router.post("/create/{route_id}", response_model=RouteStopResponse, status_code=status.HTTP_201_CREATED)
def create_route_stop_endpoint(route_id: int, stop_data: RouteStopCreate, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       return create_route_stop(route_id, stop_data, uow)
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))


@route_stop_router.post("/bulk_create/{route_id}",response_model=List[RouteStopResponse], status_code=status.HTTP_201_CREATED)
def create_seats_bulk(
   route_id: int,
   stop_data: List[RouteStopCreate],
   session: Session = Depends(get_session)
):
   uow = UnitOfWork(session)
   try:
       
       return bulk_create_route_stops(route_id, stop_data, uow)
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))
   


@route_stop_router.put("/update/{route_stop_id}", response_model=RouteStopResponse)
def update_route_stop_endpoint(route_stop_id: int, stop_data: RouteStopCreate, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       return update_route_stop(route_stop_id, stop_data, uow)
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route stop not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))

@route_stop_router.delete("/delete/{route_stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route_stop_endpoint(route_stop_id: int, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       delete_route_stop(route_stop_id, uow)
       return {"detail": "Route stop deleted successfully"}
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route stop not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))

@route_stop_router.get("/get/{route_stop_id}", response_model=RouteStopResponse)
def get_route_stop_endpoint(route_stop_id: int, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       return get_route_stop(route_stop_id, uow)
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route stop not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))