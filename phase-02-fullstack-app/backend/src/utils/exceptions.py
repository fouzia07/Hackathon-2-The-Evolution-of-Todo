"""
Custom exceptions for the Full-Stack Web Todo Application.

This module defines custom exception classes for the application.
"""
from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    """
    Exception raised when trying to create a user that already exists.
    """
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {email} already exists"
        )


class UserNotFoundException(HTTPException):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, user_id: int = None, email: str = None):
        if user_id:
            detail = f"User with ID {user_id} not found"
        elif email:
            detail = f"User with email {email} not found"
        else:
            detail = "User not found"

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class InvalidCredentialsException(HTTPException):
    """
    Exception raised when invalid credentials are provided.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TaskNotFoundException(HTTPException):
    """
    Exception raised when a task is not found.
    """
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


class UnauthorizedAccessException(HTTPException):
    """
    Exception raised when a user tries to access a resource they don't own.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )