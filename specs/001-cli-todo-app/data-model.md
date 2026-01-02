# Data Model: CLI Todo Application (Phase I)

**Feature**: CLI Todo Application
**Branch**: 001-cli-todo-app
**Date**: 2026-01-02
**Purpose**: Define data structures, relationships, and validation rules for Phase I

## Overview

Phase I uses a single entity (Task) with in-memory storage. No relationships, foreign keys, or database schema required. This document defines the Task data structure and validation rules that will be implemented in Python.

---

## Entity: Task

### Purpose

Represents a single todo item with a title, description, and completion status.

### Attributes

| Attribute      | Type   | Required | Default    | Constraints                          |
|----------------|--------|----------|------------|--------------------------------------|
| `id`           | int    | Yes      | Auto       | Unique, positive, auto-incremented   |
| `title`        | str    | Yes      | None       | 1-200 chars, non-empty after strip   |
| `description`  | str    | No       | ""         | 0-1000 chars, can be empty           |
| `is_complete`  | bool   | Yes      | False      | Boolean (True/False)                 |

### Attribute Details

#### `id` (Unique Identifier)

- **Type**: Positive integer
- **Assignment**: Auto-incremented by TaskService (starts at 1)
- **Uniqueness**: Guaranteed unique within a session
- **Immutability**: Cannot be changed after creation
- **Deletion Behavior**: Deleted IDs are NOT reused in the same session

**Example Sequence**:
```
Create Task 1 → id=1
Create Task 2 → id=2
Delete Task 1 → (ID 1 removed)
Create Task 3 → id=3 (NOT id=1)
```

#### `title` (Task Title)

- **Type**: String
- **Required**: Yes
- **Length**: 1-200 characters
- **Validation**:
  - Must not be empty or whitespace-only after `strip()`
  - Leading/trailing whitespace is automatically stripped
  - Internal whitespace preserved
- **Use Case**: Short summary of the task (e.g., "Buy groceries")

**Valid Examples**:
```
"Buy groceries"
"Finish Q4 report"
"Call dentist for appointment"
"  Fix bug #42  " → Stored as "Fix bug #42"
```

**Invalid Examples**:
```
"" → Error: Title cannot be empty
"   " → Error: Title cannot be empty (stripped to "")
"A" * 201 → Error: Title must be 200 characters or less
```

#### `description` (Task Description)

- **Type**: String
- **Required**: No (can be empty)
- **Length**: 0-1000 characters
- **Validation**:
  - Empty string allowed
  - Whitespace-only strings allowed (not stripped)
  - Newlines and special characters allowed
- **Use Case**: Detailed notes about the task

**Valid Examples**:
```
""  → Empty description (valid)
"Buy milk, eggs, and bread from store"
"Deadline: Friday\nNeed to review sections 1-3"
"🎯 Priority task"
```

**Invalid Examples**:
```
"A" * 1001 → Error: Description must be 1000 characters or less
```

#### `is_complete` (Completion Status)

- **Type**: Boolean
- **Required**: Yes
- **Default**: `False` (incomplete)
- **Values**: `True` (complete) or `False` (incomplete)
- **Mutability**: Can be toggled via `mark_complete()` / `mark_incomplete()` methods
- **Display**: Shown as `[✓]` (complete) or `[ ]` (incomplete) in UI

---

## Data Structure (Python Implementation)

### Task Class Definition

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    is_complete: bool = False

    def __post_init__(self):
        """Validate task data after initialization"""
        # Validate and clean title
        self.title = self.title.strip()
        if not self.title:
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError(f"Title must be 200 characters or less (got {len(self.title)})")

        # Validate description
        if len(self.description) > 1000:
            raise ValidationError(f"Description must be 1000 characters or less (got {len(self.description)})")

        # Validate ID
        if self.id < 1:
            raise ValidationError("Task ID must be a positive integer")

    def mark_complete(self) -> None:
        """Mark task as complete"""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark task as incomplete"""
        self.is_complete = False

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update task title and/or description"""
        if title is not None:
            self.title = title.strip()
            if not self.title:
                raise ValidationError("Title cannot be empty")
            if len(self.title) > 200:
                raise ValidationError(f"Title must be 200 characters or less")

        if description is not None:
            if len(description) > 1000:
                raise ValidationError(f"Description must be 1000 characters or less")
            self.description = description

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }

    def __str__(self) -> str:
        """Human-readable string representation"""
        status = "✓" if self.is_complete else " "
        return f"[{status}] {self.id}. {self.title}"
```

---

## Storage Model

### In-Memory Storage Structure

**Type**: Python Dictionary
**Structure**: `Dict[int, Task]`
**Location**: TaskService._tasks (private attribute)

```python
# Example storage state
_tasks = {
    1: Task(id=1, title="Buy groceries", description="Milk, eggs", is_complete=False),
    2: Task(id=2, title="Finish report", description="Q4 analysis", is_complete=True),
    4: Task(id=4, title="Call dentist", description="", is_complete=False)
}
# Note: ID 3 was deleted (gap in sequence)
```

### Storage Operations

| Operation       | Method                     | Complexity | Notes                              |
|-----------------|----------------------------|------------|------------------------------------|
| Create          | `_tasks[new_id] = task`    | O(1)       | Auto-increment _next_id           |
| Read (by ID)    | `_tasks.get(id)`           | O(1)       | Returns None if not found         |
| Read (all)      | `list(_tasks.values())`    | O(n)       | Convert to list, sort by ID       |
| Update          | `_tasks[id].update(...)`   | O(1)       | Must exist (check first)          |
| Delete          | `del _tasks[id]`           | O(1)       | Must exist (check first)          |
| Toggle Complete | `_tasks[id].mark_complete()`| O(1)       | Must exist (check first)          |

### ID Management

```python
class TaskService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: str) -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task
```

**ID Guarantees**:
- IDs start at 1
- IDs increment sequentially (1, 2, 3, 4, ...)
- Deleted IDs create gaps (1, 2, 4, 5 if ID 3 deleted)
- IDs never reused within a session
- IDs reset to 1 on application restart (in-memory storage)

---

## Validation Rules

### Title Validation

| Rule                  | Check                              | Error Message                                   |
|-----------------------|------------------------------------|-------------------------------------------------|
| Non-empty             | `len(title.strip()) > 0`          | "Title cannot be empty"                        |
| Max length            | `len(title) <= 200`               | "Title must be 200 characters or less"         |
| Auto-trim whitespace  | `title = title.strip()`           | (automatic, no error)                          |

### Description Validation

| Rule         | Check                      | Error Message                                    |
|--------------|----------------------------|--------------------------------------------------|
| Max length   | `len(description) <= 1000` | "Description must be 1000 characters or less"   |
| Allow empty  | No check                   | (empty string is valid)                         |

### ID Validation

| Rule              | Check        | Error Message                                |
|-------------------|--------------|----------------------------------------------|
| Positive integer  | `id >= 1`    | "Task ID must be a positive integer"        |
| Existence check   | `id in _tasks` | "Task with ID {id} not found"               |

### Completion Status Validation

| Rule         | Check           | Error Message  |
|--------------|-----------------|----------------|
| Boolean type | `isinstance(is_complete, bool)` | (type hint enforced by Python) |

---

## State Transitions

### Task Lifecycle

```
[Created] → is_complete=False
    ↓
[Can be updated] → title, description modified
    ↓
[Can be marked complete] → is_complete=True
    ↓
[Can be marked incomplete] → is_complete=False
    ↓
[Can be deleted] → removed from storage
```

### Allowed Transitions

| Current State    | Action             | New State        | Validation                  |
|------------------|--------------------|------------------|-----------------------------|
| Not exists       | Create             | Incomplete       | Title valid                |
| Incomplete       | Mark Complete      | Complete         | Task exists                |
| Complete         | Mark Incomplete    | Incomplete       | Task exists                |
| Any              | Update             | Any (same status)| Task exists, title valid   |
| Any              | Delete             | Not exists       | Task exists                |

### Disallowed Operations

- Cannot update a non-existent task (must check existence first)
- Cannot delete a non-existent task
- Cannot toggle status of non-existent task
- Cannot create task with existing ID (ID is auto-assigned)

---

## Validation Error Handling

### Custom Exception Classes

```python
class TodoAppError(Exception):
    """Base exception for todo application"""
    pass

class ValidationError(TodoAppError):
    """Raised when input validation fails"""
    pass

class TaskNotFoundError(TodoAppError):
    """Raised when task ID doesn't exist"""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")
```

### Where Validation Occurs

1. **Task.__post_init__()**: Title/description length, ID validity
2. **Task.update()**: Title/description length when updating
3. **TaskService methods**: Task existence before operations

### Error Propagation

```
UI Layer (menu.py)
    ↓ (user input)
TaskService (task_service.py)
    ↓ (validates existence)
Task Model (task.py)
    ↓ (validates data)
    ↓ (raises ValidationError if invalid)
TaskService catches → raises TaskNotFoundError if not found
    ↓
Main App (main.py) catches all exceptions
    ↓
Display error to user (display.py)
    ↓
Return to menu (don't crash)
```

---

## Data Examples

### Example 1: Simple Task

```python
task = Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    is_complete=False
)

# Display
print(task)  # Output: [ ] 1. Buy groceries
```

### Example 2: Complete Task with Multiline Description

```python
task = Task(
    id=5,
    title="Finish Q4 report",
    description="Complete sections:\n1. Revenue analysis\n2. Expense breakdown\n3. Projections",
    is_complete=True
)

# Display
print(task)  # Output: [✓] 5. Finish Q4 report
```

### Example 3: Task with Empty Description

```python
task = Task(
    id=10,
    title="Call dentist",
    description="",
    is_complete=False
)

# to_dict()
print(task.to_dict())
# Output: {'id': 10, 'title': 'Call dentist', 'description': '', 'is_complete': False}
```

### Example 4: Validation Error

```python
try:
    task = Task(
        id=1,
        title="",  # Empty title
        description="This will fail",
        is_complete=False
    )
except ValidationError as e:
    print(f"Error: {e}")
    # Output: Error: Title cannot be empty
```

---

## Phase II Evolution Preview

### Changes in Phase II (Database Storage)

**From (Phase I)**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    is_complete: bool = False
```

**To (Phase II)**:
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False, default="")
    is_complete = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
```

**New Attributes in Phase II**:
- `created_at`: Timestamp of task creation
- `updated_at`: Timestamp of last modification
- `user_id`: Foreign key to User table (multi-user support)

**Storage Changes**:
- Dict → PostgreSQL database
- In-memory → Persistent storage
- Auto-increment via database sequence
- Relationships (Task belongs to User)

---

## Conclusion

The Task data model for Phase I is intentionally simple:
- **Single entity** (Task)
- **Four attributes** (id, title, description, is_complete)
- **In-memory storage** (Python dict)
- **Comprehensive validation** (title/description length, ID validity)
- **Clear state transitions** (incomplete ↔ complete, create → delete)

This design satisfies all Phase I requirements while preparing for Phase II database migration (same business logic, different storage mechanism).

---

**Data Model Status**: Complete
**Next Step**: Create `quickstart.md` (Phase 1 user guide)
