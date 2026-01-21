"""
Task service for the Full-Stack Web Todo Application.

This module provides business logic for task-related operations.
"""
from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException


class TaskService:
    """
    Service class for task-related business logic.
    """

    @staticmethod
    def create_task(db: Session, task_create: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for a user.

        Args:
            db (Session): Database session
            task_create (TaskCreate): Task creation data
            user_id (int): ID of the user creating the task

        Returns:
            Task: The created task
        """
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            is_complete=task_create.is_complete,
            user_id=user_id
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Get a task by ID for a specific user.

        Args:
            db (Session): Database session
            task_id (int): Task ID
            user_id (int): User ID

        Returns:
            Optional[Task]: The task if found and belongs to the user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = db.exec(statement).first()
        return task

    @staticmethod
    def get_tasks_by_user(db: Session, user_id: int) -> List[Task]:
        """
        Get all tasks for a specific user.

        Args:
            db (Session): Database session
            user_id (int): User ID

        Returns:
            List[Task]: List of tasks belonging to the user
        """
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.id)
        tasks = db.exec(statement).all()
        return tasks

    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
        """
        Update a task for a user.

        Args:
            db (Session): Database session
            task_id (int): Task ID to update
            task_update (TaskUpdate): Update data
            user_id (int): User ID

        Returns:
            Optional[Task]: Updated task if found and belongs to the user, None otherwise

        Raises:
            UnauthorizedAccessException: If task doesn't belong to the user
        """
        # First get the existing task to check if it belongs to the user
        db_task = TaskService.get_task_by_id(db, task_id, user_id)
        if not db_task:
            raise UnauthorizedAccessException()

        # Update the task with provided data
        for field, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, field, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a task for a user.

        Args:
            db (Session): Database session
            task_id (int): Task ID to delete
            user_id (int): User ID

        Returns:
            bool: True if task was deleted, False if not found or not authorized

        Raises:
            UnauthorizedAccessException: If task doesn't belong to the user
        """
        # First get the existing task to check if it belongs to the user
        db_task = TaskService.get_task_by_id(db, task_id, user_id)
        if not db_task:
            raise UnauthorizedAccessException()

        db.delete(db_task)
        db.commit()

        return True