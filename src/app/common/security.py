from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCES_TOKEN_EXPIRE_MINUTES
from app.common.error_messages import ErrorMessages
from app.common.custom_exceptions import InvalidCredentialsException

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)


def decode_access_token(token:str):
    try:
        return jwt.decode(token,JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM])  
    except JWTError:
        raise InvalidCredentialsException(ErrorMessages.INVALID_OR_EXPIRED_TOKEN)