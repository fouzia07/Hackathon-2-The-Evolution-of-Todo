"""
API utility functions for the Full-Stack Web Todo Application.

This module provides common helper functions for API operations.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from ..models.task import Task
from ..models.user import User


def format_task_response(task: Task) -> Dict[str, Any]:
    """
    Format a task object for API response.

    Args:
        task (Task): The task object to format

    Returns:
        Dict[str, Any]: Formatted task data for API response
    """
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None
    }


def format_user_response(user: User, include_sensitive: bool = False) -> Dict[str, Any]:
    """
    Format a user object for API response.

    Args:
        user (User): The user object to format
        include_sensitive (bool): Whether to include sensitive information

    Returns:
        Dict[str, Any]: Formatted user data for API response
    """
    response = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }

    if include_sensitive:
        response["hashed_password"] = user.hashed_password

    return response


def filter_tasks_by_user(tasks: List[Task], user_id: int) -> List[Task]:
    """
    Filter a list of tasks to only include tasks belonging to a specific user.

    Args:
        tasks (List[Task]): List of tasks to filter
        user_id (int): User ID to filter by

    Returns:
        List[Task]: Filtered list of tasks
    """
    return [task for task in tasks if task.user_id == user_id]


def validate_task_input(title: Optional[str], description: Optional[str] = None) -> Dict[str, str]:
    """
    Validate task input data.

    Args:
        title (Optional[str]): Task title
        description (Optional[str]): Task description

    Returns:
        Dict[str, str]: Dictionary of validation errors, empty if valid
    """
    errors = {}

    if title is None or not title.strip():
        errors["title"] = "Title is required"
    elif len(title.strip()) < 1:
        errors["title"] = "Title must be at least 1 character"
    elif len(title.strip()) > 200:
        errors["title"] = "Title must be 200 characters or less"

    if description and len(description) > 1000:
        errors["description"] = "Description must be 1000 characters or less"

    return errors


def validate_user_input(
    email: Optional[str],
    password: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> Dict[str, str]:
    """
    Validate user input data.

    Args:
        email (Optional[str]): User email
        password (Optional[str]): User password
        first_name (Optional[str]): User first name
        last_name (Optional[str]): User last name

    Returns:
        Dict[str, str]: Dictionary of validation errors, empty if valid
    """
    errors = {}

    if email is None or not email.strip():
        errors["email"] = "Email is required"
    elif "@" not in email or "." not in email.split("@")[1]:
        errors["email"] = "Invalid email format"

    if password:
        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters"
        # Additional password validation could go here

    if first_name and len(first_name) > 100:
        errors["first_name"] = "First name must be 100 characters or less"

    if last_name and len(last_name) > 100:
        errors["last_name"] = "Last name must be 100 characters or less"

    return errors


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and other injection attacks.

    Args:
        text (str): Input text to sanitize

    Returns:
        str: Sanitized text
    """
    # Basic sanitization - in a real app, use a dedicated library like bleach
    if not isinstance(text, str):
        return ""

    # Remove basic HTML tags (simple approach)
    sanitized = text.replace("<script", "&lt;script").replace(">", "&gt;")
    sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")

    return sanitized.strip()


def build_pagination_response(
    items: List[Any],
    total_count: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """
    Build a pagination response for API endpoints.

    Args:
        items (List[Any]): List of items to return
        total_count (int): Total number of items available
        page (int): Current page number
        page_size (int): Size of each page

    Returns:
        Dict[str, Any]: Pagination response
    """
    total_pages = (total_count + page_size - 1) // page_size  # Ceiling division

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }