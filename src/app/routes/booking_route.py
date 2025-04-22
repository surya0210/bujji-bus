from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.passenger_schema import BookingPNRResponse, CancelPassengerRequest, SeatBookingRequest, SeatBookingResponse
from app.services.booking_service import book_seats, cancel_booking_by_passenger, cancel_booking_by_pnr, get_bookings_by_pnr
from app.repositories.unit_of_work import UnitOfWork
from app.common.session_maker import get_session
from sqlalchemy.orm import Session

booking_router = APIRouter(prefix="/booking", tags=["booking"])
@booking_router.post("/create", response_model=SeatBookingResponse)
def create_booking(request: SeatBookingRequest,session: Session = Depends(get_session)):
   try:
       uow=UnitOfWork(session)
       result = book_seats(uow, request)
       return SeatBookingResponse(**result)
   except ValueError as ve:
       raise HTTPException(status_code=400, detail=str(ve))
   except Exception as e:
       print(e)
       raise HTTPException(status_code=500, detail="Internal Server Error")
   

@booking_router.get("/pnr-details/{pnr}", response_model=List[BookingPNRResponse])
def fetch_booking_by_pnr(pnr: str, session: Session = Depends(get_session)):
   uow=UnitOfWork(session)
   bookings = get_bookings_by_pnr(uow, pnr)
   if not bookings:
       raise HTTPException(status_code=404, detail="No bookings found for PNR")
   return bookings

@booking_router.post("/cancel-passenger")
def cancel_by_passenger(req: CancelPassengerRequest, session: Session = Depends(get_session)):
   uow=UnitOfWork(session)
   result = cancel_booking_by_passenger(uow,req.pnr, req.passenger_id, req.travel_date)
   if result["cancelled_count"] == 0:
       raise HTTPException(status_code=404, detail="No active bookings found for this passenger and date")
   return {"message": f"{result['cancelled_count']} seat(s) cancelled"}

@booking_router.post("/cancel-pnr/{pnr}")
def cancel_by_pnr(pnr: str, session: Session = Depends(get_session)):
   uow=UnitOfWork(session)
   result = cancel_booking_by_pnr(uow, pnr)
   if result["cancelled_count"] == 0:
       raise HTTPException(status_code=404, detail="No active bookings found for this PNR")
   return {"message": f"{result['cancelled_count']} seat(s) cancelled for PNR {pnr}"}