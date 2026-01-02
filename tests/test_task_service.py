"""Unit tests for TaskService."""

import pytest
from src.services.task_service import TaskService, TaskNotFoundError
from src.models.task import ValidationError


class TestTaskServiceCreation:
    """Tests for creating tasks via TaskService."""

    @pytest.fixture
    def service(self):
        """Create a fresh TaskService instance for each test."""
        return TaskService()

    def test_create_task_assigns_id_1_to_first_task(self, service):
        """Test that the first task gets ID 1."""
        task = service.create_task("First Task", "First description")
        assert task.id == 1

    def test_create_task_increments_ids(self, service):
        """Test that task IDs increment sequentially."""
        task1 = service.create_task("Task 1", "Description 1")
        task2 = service.create_task("Task 2", "Description 2")
        task3 = service.create_task("Task 3", "Description 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_with_empty_title_raises_error(self, service):
        """Test that creating task with empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            service.create_task("", "Description")

    def test_create_task_with_long_title_raises_error(self, service):
        """Test that creating task with title >200 chars raises ValidationError."""
        long_title = "A" * 201
        with pytest.raises(
            ValidationError, match="Title must be 200 characters or less"
        ):
            service.create_task(long_title, "Description")


class TestTaskServiceRetrieval:
    """Tests for retrieving tasks via TaskService."""

    @pytest.fixture
    def service_with_tasks(self):
        """Create a TaskService with three sample tasks."""
        service = TaskService()
        service.create_task("Task 1", "Description 1")
        service.create_task("Task 2", "Description 2")
        service.create_task("Task 3", "Description 3")
        return service

    def test_get_task_returns_correct_task(self, service_with_tasks):
        """Test retrieving an existing task by ID."""
        task = service_with_tasks.get_task(2)
        assert task is not None
        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_task_returns_none_for_nonexistent_id(self, service_with_tasks):
        """Test that get_task returns None for non-existent ID."""
        task = service_with_tasks.get_task(999)
        assert task is None

    def test_get_all_tasks_returns_empty_list_initially(self):
        """Test that get_all_tasks returns empty list for new service."""
        service = TaskService()
        tasks = service.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_returns_all_tasks_sorted_by_id(self, service_with_tasks):
        """Test that get_all_tasks returns all tasks sorted by ID."""
        tasks = service_with_tasks.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_all_tasks_maintains_sort_after_deletion(self, service_with_tasks):
        """Test that get_all_tasks maintains sort order even with gaps in IDs."""
        service_with_tasks.delete_task(2)  # Delete middle task
        tasks = service_with_tasks.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 3


class TestTaskServiceUpdate:
    """Tests for updating tasks via TaskService."""

    @pytest.fixture
    def service_with_task(self):
        """Create a TaskService with one sample task."""
        service = TaskService()
        service.create_task("Original Title", "Original description")
        return service

    def test_update_task_modifies_title(self, service_with_task):
        """Test updating task title."""
        task = service_with_task.update_task(1, title="New Title")
        assert task.title == "New Title"
        assert task.description == "Original description"  # Unchanged

    def test_update_task_modifies_description(self, service_with_task):
        """Test updating task description."""
        task = service_with_task.update_task(1, description="New description")
        assert task.title == "Original Title"  # Unchanged
        assert task.description == "New description"

    def test_update_task_modifies_both_fields(self, service_with_task):
        """Test updating both title and description."""
        task = service_with_task.update_task(
            1, title="New Title", description="New description"
        )
        assert task.title == "New Title"
        assert task.description == "New description"

    def test_update_task_raises_error_for_invalid_id(self, service_with_task):
        """Test that updating non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            service_with_task.update_task(999, title="New Title")

    def test_update_task_with_empty_title_raises_error(self, service_with_task):
        """Test that updating with empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            service_with_task.update_task(1, title="")


class TestTaskServiceDeletion:
    """Tests for deleting tasks via TaskService."""

    @pytest.fixture
    def service_with_tasks(self):
        """Create a TaskService with three sample tasks."""
        service = TaskService()
        service.create_task("Task 1", "Description 1")
        service.create_task("Task 2", "Description 2")
        service.create_task("Task 3", "Description 3")
        return service

    def test_delete_task_removes_task(self, service_with_tasks):
        """Test that delete_task removes the task."""
        result = service_with_tasks.delete_task(2)
        assert result is True
        assert service_with_tasks.get_task(2) is None

    def test_delete_task_returns_true(self, service_with_tasks):
        """Test that delete_task returns True on success."""
        result = service_with_tasks.delete_task(1)
        assert result is True

    def test_delete_task_raises_error_for_invalid_id(self, service_with_tasks):
        """Test that deleting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            service_with_tasks.delete_task(999)

    def test_deleted_ids_are_not_reused(self, service_with_tasks):
        """Test that deleted task IDs are not reused."""
        service_with_tasks.delete_task(2)  # Delete task with ID 2
        new_task = service_with_tasks.create_task("Task 4", "Description 4")
        assert new_task.id == 4  # Next ID is 4, not 2
        assert service_with_tasks.get_task(2) is None  # ID 2 still doesn't exist


class TestTaskServiceToggleComplete:
    """Tests for toggling task completion status."""

    @pytest.fixture
    def service_with_task(self):
        """Create a TaskService with one sample task."""
        service = TaskService()
        service.create_task("Sample Task", "Sample description")
        return service

    def test_toggle_complete_sets_is_complete_to_true(self, service_with_task):
        """Test marking task as complete."""
        task = service_with_task.toggle_complete(1, is_complete=True)
        assert task.is_complete is True

    def test_toggle_complete_sets_is_complete_to_false(self, service_with_task):
        """Test marking task as incomplete."""
        # First mark it complete
        service_with_task.toggle_complete(1, is_complete=True)
        # Then mark it incomplete
        task = service_with_task.toggle_complete(1, is_complete=False)
        assert task.is_complete is False

    def test_toggle_complete_raises_error_for_invalid_id(self, service_with_task):
        """Test that toggling non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError, match="Task with ID 999 not found"):
            service_with_task.toggle_complete(999, is_complete=True)

    def test_toggle_complete_back_and_forth(self, service_with_task):
        """Test toggling completion status multiple times."""
        # Start incomplete
        task = service_with_task.get_task(1)
        assert task.is_complete is False

        # Toggle to complete
        service_with_task.toggle_complete(1, is_complete=True)
        task = service_with_task.get_task(1)
        assert task.is_complete is True

        # Toggle back to incomplete
        service_with_task.toggle_complete(1, is_complete=False)
        task = service_with_task.get_task(1)
        assert task.is_complete is False


class TestTaskServiceIntegration:
    """Integration tests for multiple TaskService operations."""

    def test_full_crud_workflow(self):
        """Test complete CRUD workflow."""
        service = TaskService()

        # Create
        task1 = service.create_task("Task 1", "Description 1")
        task2 = service.create_task("Task 2", "Description 2")
        assert len(service.get_all_tasks()) == 2

        # Read
        retrieved = service.get_task(task1.id)
        assert retrieved.title == "Task 1"

        # Update
        service.update_task(task1.id, title="Updated Task 1")
        updated = service.get_task(task1.id)
        assert updated.title == "Updated Task 1"

        # Delete
        service.delete_task(task2.id)
        assert len(service.get_all_tasks()) == 1
        assert service.get_task(task2.id) is None

    def test_id_gap_handling(self):
        """Test that ID gaps are handled correctly."""
        service = TaskService()

        # Create tasks 1, 2, 3
        service.create_task("Task 1", "Description 1")
        service.create_task("Task 2", "Description 2")
        service.create_task("Task 3", "Description 3")

        # Delete task 2
        service.delete_task(2)

        # Create task 4 (not 2)
        task4 = service.create_task("Task 4", "Description 4")
        assert task4.id == 4

        # Verify tasks 1, 3, 4 exist (but not 2)
        tasks = service.get_all_tasks()
        task_ids = [task.id for task in tasks]
        assert task_ids == [1, 3, 4]
