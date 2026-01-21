"""TaskService for managing tasks with in-memory storage.

This module provides CRUD operations for tasks using a dictionary-based
in-memory storage system. Task IDs are auto-incremented and never reused.
"""

from typing import Dict, List, Optional
from src.models.task import Task, ValidationError, TodoAppError


class TaskNotFoundError(TodoAppError):
    """Raised when a task with the specified ID doesn't exist."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class TaskService:
    """Service for managing tasks with CRUD operations.

    Uses in-memory dictionary storage for tasks. Task IDs are auto-incremented
    starting from 1 and are never reused, even after deletion.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for the next task ID to assign
    """

    def __init__(self) -> None:
        """Initialize empty task storage and ID counter."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: str) -> Task:
        """Create a new task with auto-assigned ID.

        Args:
            title: Task title (1-200 characters)
            description: Task description (0-1000 characters)

        Returns:
            The newly created Task object.

        Raises:
            ValidationError: If title or description validation fails.
        """
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task object if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks sorted by ID.

        Returns:
            List of all Task objects sorted by ID in ascending order.
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title for the task (optional).
            description: New description for the task (optional).

        Returns:
            The updated Task object.

        Raises:
            TaskNotFoundError: If task with the specified ID doesn't exist.
            ValidationError: If new title or description validation fails.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        task.update(title=title, description=description)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was successfully deleted.

        Raises:
            TaskNotFoundError: If task with the specified ID doesn't exist.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        return True

    def toggle_complete(self, task_id: int, is_complete: bool) -> Task:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle.
            is_complete: True to mark complete, False to mark incomplete.

        Returns:
            The updated Task object.

        Raises:
            TaskNotFoundError: If task with the specified ID doesn't exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        if is_complete:
            task.mark_complete()
        else:
            task.mark_incomplete()

        return task
