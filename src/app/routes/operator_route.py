from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.operator_schema import (
    OperatorSignupData,
    OperatorTokenResponse,
    SignupResponse,
    OperatorLoginRequest,
    OperatorTokenLoginRequest,
    OperatorLoginResponse,
    OperatorUpdate
)
from app.common.security import create_access_token
from app.repositories.unit_of_work import UnitOfWork
from app.services.operator_service import create_operator, login_operator, update_operator
from app.common.error_messages import ErrorMessages
from app.common.custom_exceptions import (
    InvalidCredentialsException,
    OperatorAlreadyExistsException,
    OperatorNotFoundException,
)
from app.common.session_maker import get_session
from app.common.success_messages import SuccessMessages


operator_router = APIRouter(prefix="/operator", tags=["operator"])


@operator_router.post("/token-signup-generate", response_model=OperatorTokenResponse)
def generate_token(data: OperatorSignupData) -> OperatorTokenResponse:
    try:
        token = create_access_token(data.model_dump())
        return OperatorTokenResponse(token=token)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something Went Wrong")


@operator_router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Conflict"},
        "400": {"description": "Bad Request"},
        "500": {"description": "Internal Server Error"},
    },
)
def operator_signup(
    payload: OperatorTokenResponse, session: Session = Depends(get_session)
):
    try:
        uow = UnitOfWork(session)
        return create_operator(payload, uow)
    except OperatorAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.SOMETHING_WENT_WRONG,
        )
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.INTERNAL_SERVER_ERROR,
        )


@operator_router.post("/token-login-generate", response_model=OperatorTokenResponse)
def generate_login_token(data: OperatorLoginRequest) -> OperatorTokenResponse:
    try:
        token = create_access_token(data.model_dump())
        return OperatorTokenResponse(token=token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.BAD_REQUEST
        )


@operator_router.post(
    "/login",
    response_model=OperatorLoginResponse,
    status_code=status.HTTP_200_OK,
    responses={401: {"description": "Unauthorized"}},
)
def operator_login_endpoint(
    payload: OperatorTokenLoginRequest, session: Session = Depends(get_session)
):
    try:
        uow = UnitOfWork(session)
        return login_operator(payload, uow)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    except SQLAlchemyError as e:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.INTERNAL_SERVER_ERROR,
        )


@operator_router.patch("/update/{operator_id}",
                       response_model=None,
                       status_code=status.HTTP_204_NO_CONTENT,
                       responses={
       204: {"description": SuccessMessages.UPDATED_SUCCESSFULLY},
       400: {"description": ErrorMessages.BAD_REQUEST},
       404: {"description": ErrorMessages.OPERATOR_NOT_FOUND},
       500: {"description": ErrorMessages.INTERNAL_SERVER_ERROR},
   },
                       )
def update_operator_endpoint(
   operator_id: str,
   update_data: OperatorUpdate,
   session: Session = Depends(get_session),
):
   try:
       uow = UnitOfWork(session)
       updated_operator = update_operator(operator_id, update_data, uow)
       return {"message": SuccessMessages.UPDATED_SUCCESSFULLY, "operator": updated_operator}
   except OperatorNotFoundException:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=ErrorMessages.OPERATOR_NOT_FOUND
       )