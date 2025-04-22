from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.common.session_maker import get_session
from app.schemas.search_schema import SearchRequest, SearchResponse, SeatMapResponse
from app.services.search_service import get_seat_map_for_route, search_routes
from app.repositories.unit_of_work import UnitOfWork

search_router = APIRouter(prefix="/search", tags=["search"])


@search_router.post("/")
def search_routes_endpoint(
   req: SearchRequest,
   session: Session = Depends(get_session)
):
   
   try:
       
       uow=UnitOfWork(session)
       return search_routes(req,uow)  
   except Exception as e:
       print(e)
       raise HTTPException(status_code=500, detail=str(e))
   
@search_router.get("/routes/{route_id}/seats", response_model=List[SeatMapResponse])
def get_seat_map(
   route_id: int, travel_date: date, start_order: int, end_order: int, session: Session = Depends(get_session)
):
   try:
       uow=UnitOfWork(session)
       seat_map = get_seat_map_for_route(route_id, travel_date, start_order,end_order,uow)
       return seat_map
   except ValueError:
       raise HTTPException(status_code=404, detail="Route not found")
   