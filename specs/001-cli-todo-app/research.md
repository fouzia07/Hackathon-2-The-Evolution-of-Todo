# Research: CLI Todo Application (Phase I)

**Feature**: CLI Todo Application
**Branch**: 001-cli-todo-app
**Date**: 2026-01-02
**Purpose**: Document technology decisions and research findings for Phase I implementation

## Research Questions

### 1. Python 3.13+ Features

**Question**: What Python 3.13+ features would benefit this project?

**Research Findings**:
- **Improved Error Messages**: Python 3.11+ provides better error messages with context
- **Type Hints**: Full support for PEP 484 type annotations (available since 3.5, mature in 3.13)
- **Dataclasses**: Built-in dataclass decorator for clean model definitions (Python 3.7+)
- **Pattern Matching**: Structural pattern matching (Python 3.10+) - could simplify menu routing
- **Performance**: General performance improvements in Python 3.11+ (10-60% faster)

**Decision**: Use Python 3.13+ with dataclasses for Task model

**Rationale**:
- Type hints improve code clarity and enable static analysis
- Dataclasses reduce boilerplate for Task model (auto __init__, __repr__, etc.)
- Improved error messages aid debugging during development
- Pattern matching could simplify menu handling (optional enhancement)

---

### 2. In-Memory Storage Pattern

**Question**: Dict vs List for in-memory task storage?

**Research Findings**:

**Option A: Dictionary Storage** `{id: Task}`
- Pros: O(1) lookup by ID, natural key-value mapping, efficient updates/deletes
- Cons: Requires manual ID management, slightly more memory overhead

**Option B: List Storage** `[Task, Task, ...]`
- Pros: Simpler implementation, auto-indexing, natural ordering
- Cons: O(n) lookup by ID, inefficient deletes (requires rebuilding list or gaps)

**Decision**: Use Dictionary storage `Dict[int, Task]`

**Rationale**:
- Fast lookups critical for update/delete/toggle operations
- ID management is simple (auto-increment counter)
- Spec requires stable IDs (don't reuse after delete) - dict supports this naturally
- Memory overhead negligible for 1000+ tasks

**Implementation**:
```python
class TaskService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
```

---

### 3. Input Validation

**Question**: Best stdlib approaches for console input validation?

**Research Findings**:

**Validation Layers**:
1. **Model-Level**: Task class validates title/description lengths
2. **Service-Level**: TaskService validates task existence before operations
3. **UI-Level**: Menu validates numeric input, handles non-integer input gracefully

**Techniques**:
- `str.strip()` for removing whitespace
- `len()` checks for string length constraints
- `try/except ValueError` for integer parsing
- Regular expressions (re module) for complex patterns (not needed for Phase I)

**Decision**: Multi-layer validation with custom exceptions

**Rationale**:
- Model validation prevents invalid Task objects
- Service validation ensures business rule compliance
- UI validation provides immediate user feedback
- Custom exceptions (ValidationError, TaskNotFoundError) enable clear error messages

**Example**:
```python
class Task:
    def __init__(self, id: int, title: str, description: str):
        title = title.strip()
        if not title:
            raise ValidationError("Title cannot be empty")
        if len(title) > 200:
            raise ValidationError("Title must be 200 characters or less")
        # ... similar for description
```

---

### 4. Testing Strategy

**Question**: pytest patterns for console applications?

**Research Findings**:

**Testing Approaches**:
1. **Unit Tests**: Test models and services in isolation
2. **Mock stdout/stdin**: Use `monkeypatch` or `unittest.mock` for UI testing
3. **Fixtures**: pytest fixtures for common test data (sample tasks)
4. **Parametrize**: Test multiple inputs with `@pytest.mark.parametrize`

**Best Practices**:
- Test business logic (models, services) thoroughly
- UI tests optional for Phase I (manual testing acceptable)
- Focus on edge cases (empty input, invalid IDs, boundary values)
- Use coverage.py to track test coverage

**Decision**: Unit tests for models and services, manual UI testing

**Rationale**:
- Models and services are the core business logic
- UI is straightforward (input/output) - manual testing sufficient
- Mocking console I/O adds complexity without high value for Phase I
- Can add UI tests in future phases if needed

**Test Structure**:
```python
# tests/test_task_service.py
import pytest
from src.services.task_service import TaskService

@pytest.fixture
def service():
    return TaskService()

def test_create_task(service):
    task = service.create_task("Test", "Description")
    assert task.id == 1
    assert task.title == "Test"
```

---

### 5. Error Handling

**Question**: Best practices for user-friendly CLI error messages?

**Research Findings**:

**Error Categories**:
1. **User Input Errors**: Invalid menu choice, empty title, non-numeric ID
2. **Business Logic Errors**: Task not found, validation failures
3. **System Errors**: Unexpected exceptions (should not crash app)

**Best Practices**:
- Clear, actionable error messages (tell user what went wrong and how to fix)
- Consistent error format across application
- No stack traces shown to user (log internally if needed)
- Graceful error recovery (return to menu, don't exit)

**Decision**: Custom exception classes with user-friendly messages

**Rationale**:
- Custom exceptions enable type-safe error handling
- Exception messages designed for end-user consumption
- Try/except blocks in main.py catch and display errors gracefully

**Exception Hierarchy**:
```python
class TodoAppError(Exception):
    """Base exception for todo app"""
    pass

class ValidationError(TodoAppError):
    """Raised when input validation fails"""
    pass

class TaskNotFoundError(TodoAppError):
    """Raised when task ID doesn't exist"""
    pass
```

**Error Display Example**:
```
Error: Task with ID 999 not found.
Please enter a valid task ID from the list above.
```

---

## Technology Stack Summary

### Core Dependencies
- **Python**: 3.13+ (3.11+ acceptable if 3.13 unavailable)
- **Standard Library**: Only (no external runtime dependencies)
- **Package Manager**: UV (for project management and virtual environments)

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting (PEP 8 compliant)
- **mypy**: Static type checking (optional, recommended)

### Rationale for Stdlib-Only Approach
- Simplifies deployment (no dependency installation needed)
- Reduces maintenance burden (no security updates for deps)
- Aligns with Phase I constraints (lightweight CLI)
- Demonstrates Python capabilities without external crutches
- Faster startup time (no imports of large libraries)

---

## Design Patterns

### 1. Repository Pattern (Simplified)

TaskService acts as an in-memory repository for Task entities.

**Benefits**:
- Abstracts storage mechanism (easy to swap dict for DB in Phase II)
- Centralizes business logic
- Enables testing without actual storage

### 2. Separation of Concerns

Three-layer architecture:
- **Models**: Data structures (Task)
- **Services**: Business logic (TaskService)
- **UI**: User interaction (Menu, Display)

**Benefits**:
- Each module has single responsibility
- Easy to test in isolation
- Prepares for Phase II (FastAPI can reuse models/services)

### 3. Fail-Fast Validation

Validate inputs immediately when received:
- Task constructor validates title/description
- UI validates menu choices before routing
- Service validates task existence before operations

**Benefits**:
- Errors detected early (better UX)
- Clear error messages at failure point
- Prevents propagation of invalid data

---

## Performance Considerations

### Memory Usage

**Task Object Size** (approximate):
- `id`: 28 bytes (Python int object)
- `title`: 50-250 bytes (typical string overhead + data)
- `description`: 50-1050 bytes
- `is_complete`: 28 bytes (bool)
- **Total per task**: ~150-1400 bytes (average ~500 bytes)

**Storage Overhead**:
- 1000 tasks: ~500 KB
- 10,000 tasks: ~5 MB
- Dict overhead: ~33% additional memory

**Conclusion**: Memory is not a constraint for expected use (1000-10,000 tasks)

### Response Time

**Expected Performance**:
- Dict lookup: O(1) - instant (<1ms)
- Display 1000 tasks: O(n) - ~10-50ms (depending on console speed)
- User input: Blocking (waits for user, no timeout needed)

**Conclusion**: All operations well under 100ms target

---

## Alternatives Considered and Rejected

### 1. Click/Typer CLI Framework

**Why Considered**: Professional CLI features (auto help, validation, colors)

**Why Rejected**:
- Violates stdlib-only constraint for Phase I
- Overkill for simple menu-driven interface
- Learning curve for AI code generation
- Can revisit in Phase II+ if needed

### 2. Rich Terminal Library

**Why Considered**: Beautiful formatting (tables, colors, progress bars)

**Why Rejected**:
- External dependency (not stdlib)
- Phase I focuses on functionality, not aesthetics
- Can add in Phase II for enhanced UX
- Stdlib `print()` sufficient for basic tables

### 3. JSON/Pickle for Session Persistence

**Why Considered**: Save tasks between sessions

**Why Rejected**:
- Phase I explicitly requires in-memory only (constitutional constraint)
- Phase II will add proper database persistence
- Temporary file persistence violates Phase I scope

### 4. Asyncio for Concurrent Operations

**Why Considered**: Handle multiple operations concurrently

**Why Rejected**:
- Single-user, single-session app (no concurrency needed)
- Adds complexity without benefit
- Console I/O is inherently synchronous

---

## Phase II Preview

### Technologies to Add in Phase II

- **FastAPI**: REST API framework
- **PostgreSQL**: Database via SQLAlchemy ORM
- **Pydantic**: API validation and serialization
- **JWT**: Authentication tokens
- **Next.js**: Frontend (separate repository or monorepo structure)

### Code Reuse from Phase I

- **Task model**: Adapt to SQLAlchemy ORM model
- **TaskService**: Refactor for database operations (same interface)
- **Business logic**: CRUD operations remain similar, storage changes

---

## Conclusion

Phase I research validates the chosen approach:
- **Python 3.13+ with stdlib-only** is sufficient and appropriate
- **Dict storage with dataclass model** provides clean, efficient implementation
- **Multi-layer validation** ensures data integrity and user-friendly errors
- **pytest for unit testing** covers business logic adequately
- **Simple design patterns** prepare for Phase II evolution

All research questions resolved. Ready to proceed with Phase 1 (Design & Contracts).

---

**Research Status**: Complete
**Next Step**: Create `data-model.md` (Phase 1 detailed data structures)
