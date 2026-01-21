"""
Task API endpoints for the Full-Stack Web Todo Application.

This module provides API endpoints for task management with user isolation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any, List
from ...database.session import get_session
from ...models.task import Task
from ...schemas.task import TaskCreate, TaskRead, TaskUpdate
from ...services.task_service import TaskService
from ...auth.jwt import verify_token
from ...utils.exceptions import TaskNotFoundException, UnauthorizedAccessException


router = APIRouter()


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
):
    """
    Get the current user from the JWT token.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials
        db (Session): Database session

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    from ...auth.jwt import verify_token
    user = verify_token(credentials.credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
) -> Any:
    """
    Get all tasks for the authenticated user.

    Args:
        current_user: The authenticated user (from token)
        db (Session): Database session

    Returns:
        List[TaskRead]: List of tasks belonging to the user
    """
    tasks = TaskService.get_tasks_by_user(db, current_user.id)
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
) -> Any:
    """
    Create a new task for the authenticated user.

    Args:
        task_create (TaskCreate): Task creation data
        current_user: The authenticated user (from token)
        db (Session): Database session

    Returns:
        TaskRead: The created task
    """
    task = TaskService.create_task(db, task_create, current_user.id)
    return task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
) -> Any:
    """
    Get a specific task for the authenticated user.

    Args:
        task_id (int): Task ID
        current_user: The authenticated user (from token)
        db (Session): Database session

    Returns:
        TaskRead: The requested task

    Raises:
        HTTPException: If task is not found or doesn't belong to the user
    """
    task = TaskService.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
) -> Any:
    """
    Update a specific task for the authenticated user.

    Args:
        task_id (int): Task ID to update
        task_update (TaskUpdate): Update data
        current_user: The authenticated user (from token)
        db (Session): Database session

    Returns:
        TaskRead: The updated task

    Raises:
        HTTPException: If task is not found or doesn't belong to the user
    """
    try:
        task = TaskService.update_task(db, task_id, task_update, current_user.id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except UnauthorizedAccessException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
) -> None:
    """
    Delete a specific task for the authenticated user.

    Args:
        task_id (int): Task ID to delete
        current_user: The authenticated user (from token)
        db (Session): Database session

    Raises:
        HTTPException: If task is not found or doesn't belong to the user
    """
    try:
        success = TaskService.delete_task(db, task_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
    except UnauthorizedAccessException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )