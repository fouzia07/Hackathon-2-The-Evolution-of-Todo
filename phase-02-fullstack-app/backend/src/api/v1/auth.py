"""
Authentication API endpoints for the Full-Stack Web Todo Application.

This module provides API endpoints for user authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any
from datetime import timedelta
from ...database.session import get_session
from ...models.user import User
from ...schemas.user import UserCreate, UserRead, UserLogin, Token
from ...services.user_service import UserService
from ...auth.jwt import create_access_token
from ...auth.hashing import verify_password
from ...config import settings
from ...utils.exceptions import InvalidCredentialsException, UserAlreadyExistsException


router = APIRouter()


@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_session)) -> Any:
    """
    Register a new user.

    Args:
        user_create (UserCreate): User registration data
        db (Session): Database session

    Returns:
        UserRead: The created user data

    Raises:
        HTTPException: If user already exists
    """
    try:
        db_user = UserService.create_user(db, user_create)
        return db_user
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_create.email} already exists"
        )


@router.post("/auth/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_session)) -> Any:
    """
    Authenticate a user and return a JWT token.

    Args:
        user_login (UserLogin): User login credentials
        db (Session): Database session

    Returns:
        Token: JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    user = UserService.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise InvalidCredentialsException()

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/logout")
def logout() -> Any:
    """
    Logout endpoint (currently just a placeholder).

    In a real application, you might implement token invalidation here.
    """
    return {"message": "Successfully logged out"}