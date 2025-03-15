from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_active_user
from app.core.security import get_password_hash
from app.db.mongodb import db
from app.models.user import UserInDB
from app.schemas.user import User, UserUpdate

router = APIRouter()

@router.get("/me", response_model=User)
async def read_user_me(
    current_user: UserInDB = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_in: UserUpdate,
    current_user: UserInDB = Depends(get_current_active_user),
) -> Any:
    """
    Update current user.
    """
    update_data = user_in.dict(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data.pop("password"))
        update_data["hashed_password"] = hashed_password
    
    # Add updated_at timestamp
    from datetime import datetime
    update_data["updated_at"] = datetime.utcnow()
    
    # Update user in database
    await db.db.users.update_one(
        {"_id": current_user.id},
        {"$set": update_data}
    )
    
    # Get updated user
    updated_user = await db.db.users.find_one({"_id": current_user.id})
    
    return UserInDB(**updated_user) 