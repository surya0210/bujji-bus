from app.schemas.operator_schema import (
    OperatorTokenRequest,
    OperatorUpdate,
    SignupResponse,
    OperatorTokenResponse,
    OperatorLoginResponse,
)
from app.repositories.unit_of_work import UnitOfWork
from app.common.security import decode_access_token, hash_password, verify_password
from app.entities.operator_entity import Operator
from app.common.custom_exceptions import (
    OperatorAlreadyExistsException,
    InvalidCredentialsException,
    OperatorNotFoundException,
)
from app.common.error_messages import ErrorMessages


def create_operator(payload: OperatorTokenRequest, uow: UnitOfWork) -> SignupResponse:

    token_data = decode_access_token(payload.token)

    email = token_data["email"]

    name = token_data["name"]

    with uow:

        if uow.operators.get_by_email(email):

            raise OperatorAlreadyExistsException(email)

        hashed_password = hash_password(token_data["password"])

        operator = Operator(name=name, email=email, password_hash=hashed_password)

        uow.operators.add(operator)
        print(operator)
        uow.commit()

        return SignupResponse(success=True, message="Operator registered successfully")


def login_operator(
    token_data: OperatorTokenResponse, uow: UnitOfWork
) -> OperatorLoginResponse:
    
    data = decode_access_token(token_data.token)
    email = data.get("email")
    password = data.get("password")
    with uow:
        operator = uow.operators.get_by_email(email)
        if not operator or not verify_password(password, operator.password_hash):
            raise InvalidCredentialsException(ErrorMessages.INVALID_CREDENTIALS)
        return OperatorLoginResponse(
            id=operator.id,
            name=operator.name,
            email=operator.email,
            is_active=operator.is_active,
            created_at=operator.created_at
        )
    
def update_operator(operator_id: int, update_data: OperatorUpdate, uow: UnitOfWork):
   operator = uow.session.query(Operator).filter(Operator.id == operator_id).first()
   if not operator:
       raise OperatorNotFoundException(f"Operator with ID {operator_id} not found")
   
   if update_data.is_active is not None:
       operator.is_active = update_data.is_active
   if update_data.password:
       operator.password_hash = hash_password(update_data.password)

   if update_data.name:
       operator.name=update_data.name

   uow.commit()
   return operator