"""Display module for formatting and outputting tasks to console.

This module provides functions for displaying tasks, errors, and success
messages in a formatted table layout.
"""

import sys
from typing import List
from src.models.task import Task

# Handle Windows console encoding for emoji support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        # Python < 3.7 fallback
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")


def display_task(task: Task) -> None:
    """Display a single task's details.

    Args:
        task: The Task object to display.
    """
    status = "[✓]" if task.is_complete else "[ ]"
    print(f"\n{status} Task ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Status: {'Complete' if task.is_complete else 'Incomplete'}\n")


def display_task_list(tasks: List[Task]) -> None:
    """Display a formatted table of all tasks.

    Args:
        tasks: List of Task objects to display.
    """
    if not tasks:
        display_empty_list()
        return

    print("\n" + "=" * 80)
    print(" " * 30 + "YOUR TASKS")
    print("=" * 80)
    print(f"{'ID':<4} | {'Status':<6} | {'Title':<30} | {'Description':<30}")
    print("-" * 80)

    for task in tasks:
        status = "[✓]" if task.is_complete else "[ ]"
        # Truncate title and description if too long
        title_display = task.title[:27] + "..." if len(task.title) > 30 else task.title
        desc_display = (
            task.description[:27] + "..."
            if len(task.description) > 30
            else task.description
        )

        print(f"{task.id:<4} | {status:<6} | {title_display:<30} | {desc_display:<30}")

    print("=" * 80)
    print(f"Total: {len(tasks)} task(s)\n")


def display_error(message: str) -> None:
    """Display an error message.

    Args:
        message: The error message to display.
    """
    print(f"\n❌ ERROR: {message}\n")


def display_success(message: str) -> None:
    """Display a success message.

    Args:
        message: The success message to display.
    """
    print(f"\n✅ SUCCESS: {message}\n")


def display_empty_list() -> None:
    """Display a message when no tasks exist."""
    print("\n" + "=" * 80)
    print(" " * 25 + "NO TASKS FOUND")
    print("=" * 80)
    print("\nYou don't have any tasks yet. Add your first task to get started!\n")
