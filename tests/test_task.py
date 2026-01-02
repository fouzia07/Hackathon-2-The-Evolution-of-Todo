"""Unit tests for Task model."""

import pytest
from src.models.task import Task, ValidationError


class TestTaskCreation:
    """Tests for Task instantiation and validation."""

    def test_valid_task_creation(self):
        """Test creating a task with valid data."""
        task = Task(id=1, title="Test Task", description="Test description")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.is_complete is False

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            Task(id=1, title="", description="Description")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            Task(id=1, title="   ", description="Description")

    def test_title_too_long_raises_error(self):
        """Test that title >200 chars raises ValidationError."""
        long_title = "A" * 201
        with pytest.raises(
            ValidationError, match="Title must be 200 characters or less"
        ):
            Task(id=1, title=long_title, description="Description")

    def test_title_exactly_200_chars_is_valid(self):
        """Test that title with exactly 200 chars is valid."""
        exact_title = "A" * 200
        task = Task(id=1, title=exact_title, description="Description")
        assert len(task.title) == 200

    def test_description_too_long_raises_error(self):
        """Test that description >1000 chars raises ValidationError."""
        long_description = "A" * 1001
        with pytest.raises(
            ValidationError, match="Description must be 1000 characters or less"
        ):
            Task(id=1, title="Title", description=long_description)

    def test_description_exactly_1000_chars_is_valid(self):
        """Test that description with exactly 1000 chars is valid."""
        exact_description = "A" * 1000
        task = Task(id=1, title="Title", description=exact_description)
        assert len(task.description) == 1000

    def test_empty_description_is_valid(self):
        """Test that empty description is allowed."""
        task = Task(id=1, title="Title", description="")
        assert task.description == ""

    def test_negative_id_raises_error(self):
        """Test that negative ID raises ValidationError."""
        with pytest.raises(ValidationError, match="Task ID must be a positive integer"):
            Task(id=-1, title="Title", description="Description")

    def test_zero_id_raises_error(self):
        """Test that zero ID raises ValidationError."""
        with pytest.raises(ValidationError, match="Task ID must be a positive integer"):
            Task(id=0, title="Title", description="Description")

    def test_title_whitespace_is_stripped(self):
        """Test that leading/trailing whitespace is stripped from title."""
        task = Task(id=1, title="  Title with spaces  ", description="Description")
        assert task.title == "Title with spaces"


class TestTaskMethods:
    """Tests for Task instance methods."""

    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing."""
        return Task(id=1, title="Sample Task", description="Sample description")

    def test_mark_complete(self, sample_task):
        """Test mark_complete() sets is_complete to True."""
        assert sample_task.is_complete is False
        sample_task.mark_complete()
        assert sample_task.is_complete is True

    def test_mark_incomplete(self, sample_task):
        """Test mark_incomplete() sets is_complete to False."""
        sample_task.mark_complete()
        assert sample_task.is_complete is True
        sample_task.mark_incomplete()
        assert sample_task.is_complete is False

    def test_update_title_only(self, sample_task):
        """Test updating only the title."""
        original_description = sample_task.description
        sample_task.update(title="New Title")
        assert sample_task.title == "New Title"
        assert sample_task.description == original_description

    def test_update_description_only(self, sample_task):
        """Test updating only the description."""
        original_title = sample_task.title
        sample_task.update(description="New description")
        assert sample_task.title == original_title
        assert sample_task.description == "New description"

    def test_update_both_title_and_description(self, sample_task):
        """Test updating both title and description."""
        sample_task.update(title="New Title", description="New description")
        assert sample_task.title == "New Title"
        assert sample_task.description == "New description"

    def test_update_with_empty_title_raises_error(self, sample_task):
        """Test that updating with empty title raises ValidationError."""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            sample_task.update(title="")

    def test_update_with_title_too_long_raises_error(self, sample_task):
        """Test that updating with title >200 chars raises ValidationError."""
        long_title = "A" * 201
        with pytest.raises(
            ValidationError, match="Title must be 200 characters or less"
        ):
            sample_task.update(title=long_title)

    def test_update_with_description_too_long_raises_error(self, sample_task):
        """Test that updating with description >1000 chars raises ValidationError."""
        long_description = "A" * 1001
        with pytest.raises(
            ValidationError, match="Description must be 1000 characters or less"
        ):
            sample_task.update(description=long_description)

    def test_to_dict(self, sample_task):
        """Test to_dict() returns correct dictionary."""
        task_dict = sample_task.to_dict()
        assert task_dict == {
            "id": 1,
            "title": "Sample Task",
            "description": "Sample description",
            "is_complete": False,
        }

    def test_to_dict_with_complete_task(self, sample_task):
        """Test to_dict() for completed task."""
        sample_task.mark_complete()
        task_dict = sample_task.to_dict()
        assert task_dict["is_complete"] is True

    def test_str_incomplete_task(self, sample_task):
        """Test __str__() for incomplete task."""
        result = str(sample_task)
        assert result == "[ ] 1. Sample Task"

    def test_str_complete_task(self, sample_task):
        """Test __str__() for complete task."""
        sample_task.mark_complete()
        result = str(sample_task)
        assert result == "[✓] 1. Sample Task"
