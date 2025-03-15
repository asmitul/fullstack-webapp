from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserInDB(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 