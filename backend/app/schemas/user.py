from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    disabled: bool = False

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties to return via API
class User(UserBase):
    id: str
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties stored in DB
class UserInDB(User):
    hashed_password: str

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token payload
class TokenPayload(BaseModel):
    sub: str
    exp: datetime 