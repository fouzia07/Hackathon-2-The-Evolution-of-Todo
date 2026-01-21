"""
Task model for the Full-Stack Web Todo Application.

This module defines the Task database model using SQLModel.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime
from .user import User


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str
    description: Optional[str] = None
    is_complete: bool = False


class Task(TaskBase, table=True):
    """
    Task database model.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")

    # Relationship to user
    user: User = Relationship(back_populates="tasks")

    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TaskUpdate(SQLModel):
    """
    Schema for updating task data.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None