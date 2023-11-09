from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date, datetime
from typing import Optional
from fastapi import Query


class ContactBaseModel(BaseModel):
    name: str = Field(min_length=2, max_length=50, examples=["Name"])
    surname: str = Field(min_length=2, max_length=50, examples=["Surname"])
    email: EmailStr = Field(min_length=5, max_length=50)
    phone: str = Field(max_length=50, examples=["1234567890"])
    birthday: date

    @validator("name", "surname", pre=True)
    def check_name(cls, value):
        if value == None:
            return value
        elif not value.isalpha():
            raise ValueError("Name and surname must contain only letters")
        return value

    @validator("phone", pre=True)
    def check_phone(cls, value):
        if value == None:
            return value
        elif not value.isdigit():
            raise ValueError("Phone must contain only digits")
        return value


class ContactSearchUpdateModel(ContactBaseModel):
    name: Optional[str] = Field(
        default=None, min_length=2, max_length=50, examples=["Name"]
    )
    surname: Optional[str] = Field(
        default=None, min_length=2, max_length=50, examples=["Surname"]
    )
    email: Optional[EmailStr] = Field(default=None, min_length=5, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=50, examples=["1234567890"])
    birthday: Optional[date] = Field(default=None)


class CommonQueryParams(BaseModel):
    offset: int = Query(0, ge=0)
    limit: int = Query(10, le=100)


class ResponseContactModel(ContactBaseModel):
    id: int = 1
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
