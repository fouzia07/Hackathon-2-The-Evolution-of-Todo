"""Menu module for handling user input and menu navigation.

This module provides functions for displaying menus and prompting users
for input with validation.
"""

from typing import Tuple


def display_main_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print(" " * 15 + "TODO APPLICATION")
    print("=" * 50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Mark Incomplete")
    print("7. Exit")
    print("=" * 50)


def get_menu_choice() -> int:
    """Get and validate menu selection from user.

    Returns:
        The validated menu choice (1-7).
    """
    while True:
        try:
            choice = input("Enter your choice (1-7): ").strip()
            choice_int = int(choice)
            if 1 <= choice_int <= 7:
                return choice_int
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1 and 7.")
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting...")
            return 7  # Return exit choice


def prompt_task_input() -> Tuple[str, str]:
    """Prompt user for task title and description.

    Returns:
        Tuple of (title, description).
    """
    print("\n--- Add New Task ---")
    try:
        title = input("Enter task title: ").strip()
        description = input("Enter task description (optional): ").strip()
        return (title, description)
    except (EOFError, KeyboardInterrupt):
        print("\n\nOperation cancelled.")
        return ("", "")


def prompt_task_id() -> int:
    """Prompt user for a task ID and validate it's a positive integer.

    Returns:
        The validated task ID (positive integer).
    """
    while True:
        try:
            task_id_str = input("Enter task ID: ").strip()
            task_id = int(task_id_str)
            if task_id >= 1:
                return task_id
            else:
                print("❌ Task ID must be a positive integer.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid task ID (positive integer).")
        except (EOFError, KeyboardInterrupt):
            print("\n\nOperation cancelled.")
            return -1  # Return invalid ID to signal cancellation


def confirm_action(message: str) -> bool:
    """Prompt user for yes/no confirmation.

    Args:
        message: The confirmation message to display.

    Returns:
        True if user confirms, False otherwise.
    """
    try:
        response = input(f"{message} (Y/N): ").strip().lower()
        return response in ["y", "yes"]
    except (EOFError, KeyboardInterrupt):
        print("\n\nOperation cancelled.")
        return False


def prompt_update_fields(
    current_title: str, current_description: str
) -> Tuple[str, str]:
    """Prompt user for updated task fields.

    Args:
        current_title: The current title of the task.
        current_description: The current description of the task.

    Returns:
        Tuple of (new_title, new_description). Empty string means keep current value.
    """
    print("\n--- Update Task ---")
    print(f"Current title: {current_title}")
    print(f"Current description: {current_description}")
    print("\n(Press Enter to keep current value)")

    try:
        new_title = input("Enter new title: ").strip()
        new_description = input("Enter new description: ").strip()
        return (new_title, new_description)
    except (EOFError, KeyboardInterrupt):
        print("\n\nOperation cancelled.")
        return ("", "")
