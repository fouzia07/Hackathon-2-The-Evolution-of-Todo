"""
User schemas for the Full-Stack Web Todo Application.

This module provides Pydantic schemas for user-related request/response validation.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

    class Config:
        """
        Pydantic configuration for UserCreate schema.
        """
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """
        Pydantic configuration for UserRead schema.
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str

    class Config:
        """
        Pydantic configuration for UserLogin schema.
        """
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123"
            }
        }


class Token(BaseModel):
    """
    Schema for authentication token response.
    """
    access_token: str
    token_type: str

    class Config:
        """
        Pydantic configuration for Token schema.
        """
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """
    Schema for token data.
    """
    user_id: Optional[int] = None