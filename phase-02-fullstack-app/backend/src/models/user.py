"""
User model for the Full-Stack Web Todo Application.

This module defines the User database model using SQLModel.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, DateTime


class UserBase(SQLModel):
    """
    Base class for User model with common fields.
    """
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User database model.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]