"""
Task schemas for the Full-Stack Web Todo Application.

This module provides Pydantic schemas for task-related request/response validation.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base schema for task data.
    """
    title: str
    description: Optional[str] = None
    is_complete: bool = False


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None

    class Config:
        """
        Pydantic configuration for TaskCreate schema.
        """
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Need to buy milk, bread, and eggs",
                "is_complete": False
            }
        }


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """
        Pydantic configuration for TaskRead schema.
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Need to buy milk, bread, and eggs",
                "is_complete": False,
                "user_id": 1,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for updating task data.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None

    class Config:
        """
        Pydantic configuration for TaskUpdate schema.
        """
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "is_complete": True
            }
        }