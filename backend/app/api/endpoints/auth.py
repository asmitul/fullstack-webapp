from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.mongodb import db
from app.models.user import UserInDB
from app.schemas.user import Token, User, UserCreate

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_in: UserCreate) -> Any:
    """
    Register a new user.
    """
    # Check if user with this email already exists
    user = await db.db.users.find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    # Check if user with this username already exists
    user = await db.db.users.find_one({"username": user_in.username})
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    
    # Create new user
    user_dict = user_in.model_dump()
    hashed_password = get_password_hash(user_dict.pop("password"))
    
    user_db = UserInDB(
        **user_dict,
        hashed_password=hashed_password,
    )
    
    # Insert user into database
    result = await db.db.users.insert_one(user_db.model_dump(exclude={"id"}))
    
    # Update user with the generated ID
    user_db.id = str(result.inserted_id)
    
    # Update the document with the ID
    await db.db.users.update_one(
        {"_id": result.inserted_id},
        {"$set": {"id": str(result.inserted_id)}}
    )
    
    return user_db

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Try to find user by username
    user = await db.db.users.find_one({"username": form_data.username})
    
    # If not found, try by email
    if not user:
        user = await db.db.users.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user["_id"]), expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"} 