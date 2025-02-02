from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from src.core.auth import (
    verify_password,
    create_access_token,
    get_current_active_user,
    get_password_hash
)
from src.database import get_db
from src.models.user import User
from src.config.settings import Settings

router = APIRouter()
settings = Settings()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "is_superuser": user.is_superuser
        }
    }

@router.post("/register")
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Check if user already exists
    if db.query(User).filter(User.email == form_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=form_data.username,
        hashed_password=get_password_hash(form_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "is_superuser": user.is_superuser
        }
    }

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {
        "email": current_user.email,
        "is_superuser": current_user.is_superuser
    } 