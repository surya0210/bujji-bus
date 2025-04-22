from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class OperatorSignupData(BaseModel):
    name: str
    email: EmailStr
    password: str


class OperatorTokenRequest(BaseModel):
    token: str


class OperatorTokenResponse(BaseModel):
    token: str


class SignupResponse(BaseModel):
    success: bool
    message: Optional[str] = None

    class Config:
        orm_mode = True


class OperatorLoginRequest(BaseModel):
    email: str
    password: str


class OperatorTokenLoginRequest(BaseModel):
    token: str


class OperatorLoginResponse(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    created_at: str

    @field_validator("created_at", mode="before")
    def format_created_at(cls, value):

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        return value

    class Config:
        orm_mode = True


class OperatorUpdate(BaseModel):
   is_active: Optional[bool] = None
   password: Optional[str] = None
   name:Optional[str]=None