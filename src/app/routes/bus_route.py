from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.bus_schema import BusCreate, BusCreateResponse, BusResponse, BusUpdate
from app.services.bus_service import (
    create_bus,
    delete_bus,
    list_buses_by_operator,
    update_bus,
)
from app.common.session_maker import get_session
from app.repositories.unit_of_work import UnitOfWork
from app.common.security import decode_access_token
from app.schemas.operator_schema import OperatorTokenResponse
from sqlalchemy.orm import Session

from app.common.custom_exceptions import (
    BusAlreadyExistsException,
    BusNotFoundException,
    OperatorNotFoundException,
)
from app.common.error_messages import ErrorMessages

bus_router = APIRouter(prefix="/operator/bus", tags=["bus"])


@bus_router.post(
    "/add", response_model=BusCreateResponse, status_code=status.HTTP_201_CREATED
)
def create_bus_endpoint(
    operator_id: str, bus_data: BusCreate, session: Session = Depends(get_session)
):
    try:
        uow = UnitOfWork(session)
        return create_bus(operator_id, bus_data, uow)
    except OperatorNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:

        raise HTTPException(status_code=500, detail=ErrorMessages.INTERNAL_SERVER_ERROR)


@bus_router.get("/{operator_id}/buses", response_model=List[BusResponse])
def get_operator_buses(operator_id: str, session: Session = Depends(get_session)):
    try:
        uow = UnitOfWork(session)
        return list_buses_by_operator(operator_id, uow)
    except OperatorNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:

        raise HTTPException(status_code=500, detail=ErrorMessages.INTERNAL_SERVER_ERROR)


@bus_router.patch(
    "/{operator_id}/update/{bus_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_bus_endpoint(
    operator_id: str,
    bus_id: str,
    bus_data: BusUpdate,
    session: Session = Depends(get_session),
):
    try:
        uow = UnitOfWork(session)
        return update_bus(operator_id, bus_id, bus_data, uow)
    except BusNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorMessages.INTERNAL_SERVER_ERROR)


@bus_router.delete(
    "/{operator_id}/delete/{bus_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_bus_endpoint(
    operator_id: str, bus_id: str, session: Session = Depends(get_session)
):
    try:
        uow = UnitOfWork(session)
        delete_bus(operator_id, bus_id, uow)
    except BusNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail=ErrorMessages.INTERNAL_SERVER_ERROR)
