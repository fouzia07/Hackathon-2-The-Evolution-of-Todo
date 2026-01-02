"""Main application entry point for CLI Todo Application.

This module provides the main menu loop and orchestrates all CRUD operations
using the TaskService, Display, and Menu modules.
"""

from src.services.task_service import TaskService, TaskNotFoundError
from src.models.task import ValidationError
from src.ui.display import (
    display_task,
    display_task_list,
    display_error,
    display_success,
)
from src.ui.menu import (
    display_main_menu,
    get_menu_choice,
    prompt_task_input,
    prompt_task_id,
    confirm_action,
    prompt_update_fields,
)


def handle_add_task(service: TaskService) -> None:
    """Handle adding a new task.

    Args:
        service: The TaskService instance to use.
    """
    title, description = prompt_task_input()

    if not title:  # User cancelled or entered empty title
        if title == "":  # Empty title (not cancelled)
            display_error("Title cannot be empty. Task not created.")
        return

    try:
        task = service.create_task(title, description)
        display_success(f"Task created successfully! (ID: {task.id})")
        display_task(task)
    except ValidationError as e:
        display_error(str(e))


def handle_view_tasks(service: TaskService) -> None:
    """Handle viewing all tasks.

    Args:
        service: The TaskService instance to use.
    """
    tasks = service.get_all_tasks()
    display_task_list(tasks)


def handle_update_task(service: TaskService) -> None:
    """Handle updating a task.

    Args:
        service: The TaskService instance to use.
    """
    task_id = prompt_task_id()
    if task_id == -1:  # User cancelled
        return

    try:
        task = service.get_task(task_id)
        if task is None:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Show current task
        print("\nCurrent task:")
        display_task(task)

        # Get new values
        new_title, new_description = prompt_update_fields(task.title, task.description)

        # Only update if user provided new values
        title_to_update = new_title if new_title else None
        desc_to_update = new_description if new_description else None

        if title_to_update is None and desc_to_update is None:
            print("No changes made.")
            return

        service.update_task(task_id, title=title_to_update, description=desc_to_update)
        display_success("Task updated successfully!")

        # Show updated task
        updated_task = service.get_task(task_id)
        display_task(updated_task)

    except TaskNotFoundError as e:
        display_error(str(e))
    except ValidationError as e:
        display_error(str(e))


def handle_delete_task(service: TaskService) -> None:
    """Handle deleting a task.

    Args:
        service: The TaskService instance to use.
    """
    task_id = prompt_task_id()
    if task_id == -1:  # User cancelled
        return

    try:
        task = service.get_task(task_id)
        if task is None:
            display_error(f"Task with ID {task_id} not found.")
            return

        # Show task to be deleted
        print("\nTask to delete:")
        display_task(task)

        # Confirm deletion
        if confirm_action("Are you sure you want to delete this task?"):
            service.delete_task(task_id)
            display_success(f"Task {task_id} deleted successfully!")
        else:
            print("Deletion cancelled.")

    except TaskNotFoundError as e:
        display_error(str(e))


def handle_toggle_complete(service: TaskService, is_complete: bool) -> None:
    """Handle marking a task as complete or incomplete.

    Args:
        service: The TaskService instance to use.
        is_complete: True to mark complete, False to mark incomplete.
    """
    task_id = prompt_task_id()
    if task_id == -1:  # User cancelled
        return

    try:
        service.toggle_complete(task_id, is_complete)
        status_str = "complete" if is_complete else "incomplete"
        display_success(f"Task {task_id} marked as {status_str}!")

        # Show updated task
        task = service.get_task(task_id)
        display_task(task)

    except TaskNotFoundError as e:
        display_error(str(e))


def main() -> None:
    """Main application entry point."""
    service = TaskService()

    print("\n" + "=" * 50)
    print(" " * 10 + "Welcome to Todo CLI")
    print(" " * 7 + "Phase I: In-Memory Todo App")
    print("=" * 50)

    while True:
        try:
            display_main_menu()
            choice = get_menu_choice()

            if choice == 1:
                handle_add_task(service)
            elif choice == 2:
                handle_view_tasks(service)
            elif choice == 3:
                handle_update_task(service)
            elif choice == 4:
                handle_delete_task(service)
            elif choice == 5:
                handle_toggle_complete(service, is_complete=True)
            elif choice == 6:
                handle_toggle_complete(service, is_complete=False)
            elif choice == 7:
                print("\n" + "=" * 50)
                print(" " * 15 + "Goodbye!")
                print(" " * 5 + "Thank you for using Todo CLI")
                print("=" * 50 + "\n")
                break

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            display_error(f"Unexpected error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
