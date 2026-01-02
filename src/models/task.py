"""Task model for CLI Todo Application.

This module defines the Task data structure with validation rules for
title and description fields. Tasks are used throughout the application
to represent individual todo items.
"""

from dataclasses import dataclass
from typing import Optional


class TodoAppError(Exception):
    """Base exception for todo application."""

    pass


class ValidationError(TodoAppError):
    """Raised when input validation fails."""

    pass


@dataclass
class Task:
    """Represents a single todo item with title, description, and completion status.

    Attributes:
        id: Unique numeric identifier (auto-assigned by TaskService)
        title: Short text summarizing the task (1-200 characters)
        description: Detailed text explaining the task (0-1000 characters)
        is_complete: Boolean indicating whether the task is complete
    """

    id: int
    title: str
    description: str
    is_complete: bool = False

    def __post_init__(self) -> None:
        """Validate task data after initialization.

        Raises:
            ValidationError: If title or description validation fails.
        """
        # Validate and clean title
        self.title = self.title.strip()
        if not self.title:
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError(
                f"Title must be 200 characters or less (got {len(self.title)})"
            )

        # Validate description
        if len(self.description) > 1000:
            raise ValidationError(
                f"Description must be 1000 characters or less (got {len(self.description)})"
            )

        # Validate ID
        if self.id < 1:
            raise ValidationError("Task ID must be a positive integer")

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.is_complete = False

    def update(
        self, title: Optional[str] = None, description: Optional[str] = None
    ) -> None:
        """Update task title and/or description.

        Args:
            title: New title for the task (optional)
            description: New description for the task (optional)

        Raises:
            ValidationError: If new title or description validation fails.
        """
        if title is not None:
            title = title.strip()
            if not title:
                raise ValidationError("Title cannot be empty")
            if len(title) > 200:
                raise ValidationError(
                    f"Title must be 200 characters or less (got {len(title)})"
                )
            self.title = title

        if description is not None:
            if len(description) > 1000:
                raise ValidationError(
                    f"Description must be 1000 characters or less (got {len(description)})"
                )
            self.description = description

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization.

        Returns:
            Dictionary containing task attributes.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete,
        }

    def __str__(self) -> str:
        """Human-readable string representation.

        Returns:
            String showing task status and basic info.
        """
        status = "✓" if self.is_complete else " "
        return f"[{status}] {self.id}. {self.title}"
