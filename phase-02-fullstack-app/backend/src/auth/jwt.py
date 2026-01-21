"""
JWT token utilities for the Full-Stack Web Todo Application.

This module provides functions for creating and validating JWT tokens.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from fastapi import HTTPException, status
from sqlmodel import Session
from ..models.user import User
from ..config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the token
        expires_delta (Optional[timedelta]): Token expiration time. Defaults to 30 minutes.

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, db: Session) -> Optional[User]:
    """
    Verify a JWT token and return the associated user.

    Args:
        token (str): JWT token to verify
        db (Session): Database session

    Returns:
        Optional[User]: User associated with the token, or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        token_data = {"user_id": user_id}
    except jwt.PyJWTError:
        return None

    user = db.get(User, user_id)
    return user