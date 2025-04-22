from fastapi import APIRouter, HTTPException, Depends, status
from app.services.route_service import create_route, update_route, delete_route, get_route
from app.schemas.route_schema import RouteCreate, RouteResponse
from app.repositories.unit_of_work import UnitOfWork
from app.common.custom_exceptions import RouteNotFoundException
from sqlalchemy.orm import Session
from app.common.session_maker import get_session
route_router = APIRouter(prefix="/operator/route", tags=['route'])

@route_router.post("/create", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route_endpoint(route_data: RouteCreate, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       return create_route(route_data, uow)
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))

@route_router.put("/update/{route_id}", response_model=RouteResponse)
def update_route_endpoint(route_id: int, route_data: RouteCreate, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       return update_route(route_id, route_data, uow)
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))

@route_router.delete("/delete/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route_endpoint(route_id: int, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       delete_route(route_id, uow)
       return {"detail": "Route deleted successfully"}
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))

@route_router.get("/get/{route_id}", response_model=RouteResponse)
def get_route_endpoint(route_id: int, session: Session = Depends(get_session)):
   try:
       uow = UnitOfWork(session)
       return get_route(route_id, uow)
   except RouteNotFoundException as e:
       raise HTTPException(status_code=404, detail="Route not found")
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))