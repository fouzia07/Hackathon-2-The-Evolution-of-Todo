# Implementation Plan: CLI Todo Application (Phase I)

**Branch**: `001-cli-todo-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

**Note**: This plan covers Phase I (CLI with in-memory storage) of the Evolution of Todo project.

## Summary

Build a Python console-based Todo application that implements CRUD operations (Create, Read, Update, Delete) with in-memory task storage. The application will provide a menu-driven interface for managing tasks with titles, descriptions, and completion status. This Phase I implementation serves as the foundation for future phases (Web, AI Chatbot, K8s, Cloud).

**Primary Requirements**:
- Add tasks with title and description
- View all tasks with status indicators
- Update task title/description
- Delete tasks by ID
- Mark tasks complete/incomplete
- Menu-driven console interface
- In-memory storage only (no persistence)

**Technical Approach**:
- Clean architecture with separation of concerns (models, services, UI)
- Python 3.13+ with type hints
- UV for package management
- pytest for testing
- Single-file or modular structure based on complexity

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only for Phase I; pytest for testing)
**Storage**: In-memory (Python dict or list) - No database or file persistence
**Testing**: pytest with coverage tracking
**Target Platform**: Cross-platform (Windows via WSL 2 with Ubuntu 22.04, Linux, macOS)
**Project Type**: Single console application
**Performance Goals**: Instant response (<100ms) for all operations with up to 1000 tasks
**Constraints**:
  - No external dependencies for core app (stdlib only)
  - Console-only interface (no GUI/TUI frameworks)
  - Single-user, single-session execution
  - Task title max 200 chars, description max 1000 chars
**Scale/Scope**:
  - Single module application (~300-500 lines)
  - Support 1000+ tasks in memory
  - 5 core operations (CRUD + toggle status)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Compliance

✅ **Spec-First Development**: Specification completed at `specs/001-cli-todo-app/spec.md`
✅ **No Manual Coding**: All code will be AI-generated via Claude Code
✅ **Incremental Evolution**: Phase I scope limited to CLI + in-memory (foundation for Phase II)
✅ **Reproducibility**: All specs and plans stored in `specs/001-cli-todo-app/`
✅ **Technology Stack**: Python 3.13+ as specified in constitution
✅ **Phase-Specific Constraints**:
  - ✅ In-memory storage only (no database)
  - ✅ Command-line interface only
  - ✅ Transient state (lost on exit)
  - ✅ Unit tests for CLI commands

### Technical Standards Compliance

✅ **Code Quality**:
  - Black for code formatting
  - Type hints required (PEP 484)
  - Cyclomatic complexity <10 per function

✅ **Testing Requirements**:
  - Unit tests for all business logic
  - pytest as testing framework
  - Target 80%+ code coverage

✅ **Performance Requirements**:
  - <100ms response for all operations (Phase I target)

### Violations: None

All constitutional requirements satisfied for Phase I.

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technology research
├── data-model.md        # Phase 1: Data structures
├── quickstart.md        # Phase 1: Setup and usage guide
├── contracts/           # Phase 1: Not applicable for CLI (reserved for Phase II API)
└── checklists/
    └── requirements.md  # Spec quality checklist (complete)
```

### Source Code (repository root)

```text
/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point and menu loop
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py      # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic (CRUD operations)
│   └── ui/
│       ├── __init__.py
│       ├── menu.py      # Menu display and input handling
│       └── display.py   # Task formatting and output
│
├── tests/
│   ├── __init__.py
│   ├── test_task.py          # Task model tests
│   ├── test_task_service.py  # Service layer tests
│   └── test_ui.py            # UI component tests
│
├── pyproject.toml       # UV project configuration
├── README.md            # Setup and usage instructions
├── .gitignore           # Python-specific ignores
└── specs/               # Specifications (this directory)
```

**Structure Decision**: Single project structure selected. Console application with clear separation of concerns:
- **models/**: Data structures (Task class)
- **services/**: Business logic (TaskService for CRUD)
- **ui/**: User interface (menu, display, input handling)
- **main.py**: Application entry point and orchestration

This structure enables testability and prepares for Phase II evolution (where services can be reused with FastAPI).

## Complexity Tracking

No constitutional violations requiring justification.

## Phase 0: Research & Technology Decisions

### Research Questions

1. **Python 3.13+ Features**: Any new features beneficial for this project?
2. **In-Memory Storage Pattern**: Best practices for dict vs list storage?
3. **Input Validation**: Stdlib approaches for console input validation?
4. **Testing Strategy**: pytest patterns for console applications?
5. **Error Handling**: Best practices for user-friendly CLI error messages?

### Research Findings (to be documented in research.md)

**Decision**: Python 3.13+ with stdlib only
**Rationale**:
- No external dependencies needed for Phase I
- Python 3.13 provides improved error messages and performance
- Type hints (PEP 484) for better code clarity
- Dataclasses for Task model

**Alternatives Considered**:
- Click/Typer for CLI: Rejected (overkill for simple menu, violates stdlib-only constraint)
- Rich for formatting: Rejected (deferred to Phase II for enhanced UI)

## Phase 1: Design & Contracts

### Module Breakdown

#### Module 1: Task Model (`src/models/task.py`)

**Purpose**: Define the Task data structure with validation

**Attributes**:
- `id: int` - Unique identifier (auto-assigned)
- `title: str` - Task title (max 200 chars)
- `description: str` - Task description (max 1000 chars)
- `is_complete: bool` - Completion status (default: False)

**Methods**:
- `__init__(id, title, description)` - Constructor with validation
- `mark_complete()` - Set is_complete to True
- `mark_incomplete()` - Set is_complete to False
- `update(title, description)` - Update title/description with validation
- `to_dict()` - Serialize to dictionary
- `__str__()` - Human-readable representation

**Validation Rules**:
- Title: 1-200 characters, cannot be empty/whitespace-only
- Description: 0-1000 characters
- ID: Positive integer

**Dependencies**: None (stdlib only)

---

#### Module 2: Task Service (`src/services/task_service.py`)

**Purpose**: Business logic for CRUD operations and in-memory storage

**Storage**: Dictionary `{id: Task}` for O(1) lookups

**Methods**:
- `__init__()` - Initialize empty task storage and ID counter
- `create_task(title: str, description: str) -> Task` - Create and store new task
- `get_task(task_id: int) -> Optional[Task]` - Retrieve task by ID
- `get_all_tasks() -> List[Task]` - Get all tasks sorted by ID
- `update_task(task_id: int, title: str, description: str) -> Task` - Update existing task
- `delete_task(task_id: int) -> bool` - Remove task, return success status
- `toggle_complete(task_id: int, is_complete: bool) -> Task` - Mark complete/incomplete

**Error Handling**:
- `TaskNotFoundError` - When task ID doesn't exist
- `ValidationError` - When input validation fails

**State Management**:
- `_tasks: Dict[int, Task]` - Internal storage
- `_next_id: int` - Auto-increment counter (starts at 1)

**Dependencies**: Task model

---

#### Module 3: Display (`src/ui/display.py`)

**Purpose**: Format and display tasks to console

**Methods**:
- `display_task(task: Task)` - Show single task details
- `display_task_list(tasks: List[Task])` - Show all tasks in table format
- `display_error(message: str)` - Show error message in red/bold
- `display_success(message: str)` - Show success message
- `display_empty_list()` - Message when no tasks exist

**Output Format**:
```
ID | Status | Title            | Description
---+--------+------------------+---------------------------
1  | [ ]    | Buy groceries    | Milk, eggs, bread
2  | [✓]    | Finish report    | Complete Q4 analysis
```

**Status Indicators**:
- `[ ]` - Incomplete task
- `[✓]` - Complete task

**Dependencies**: Task model

---

#### Module 4: Menu (`src/ui/menu.py`)

**Purpose**: Handle user input and menu navigation

**Methods**:
- `display_main_menu()` - Show menu options
- `get_menu_choice() -> int` - Get and validate menu selection
- `prompt_task_input() -> Tuple[str, str]` - Get title and description
- `prompt_task_id() -> int` - Get and validate task ID
- `confirm_action(message: str) -> bool` - Yes/no confirmation

**Menu Options**:
```
=== Todo Application ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit
Enter choice (1-7):
```

**Input Validation**:
- Menu choice: 1-7
- Task ID: Positive integer
- Title: Non-empty after stripping whitespace
- Description: Any string (can be empty)

**Dependencies**: None

---

#### Module 5: Main Application (`src/main.py`)

**Purpose**: Application entry point and orchestration

**Flow**:
1. Initialize TaskService
2. Display menu
3. Get user choice
4. Route to appropriate handler
5. Display result
6. Loop until exit

**Methods**:
- `main()` - Entry point
- `handle_add_task(service)` - Add task flow
- `handle_view_tasks(service)` - View tasks flow
- `handle_update_task(service)` - Update task flow
- `handle_delete_task(service)` - Delete task flow
- `handle_toggle_complete(service, complete)` - Toggle status flow

**Error Handling**:
- Catch all exceptions from service layer
- Display user-friendly error messages
- Return to menu on error (don't crash)

**Dependencies**: All modules (TaskService, Menu, Display)

---

### Data Flow

```
User Input (menu.py)
    ↓
Main App (main.py) - Orchestration
    ↓
Task Service (task_service.py) - Business Logic
    ↓
Task Model (task.py) - Data Structure
    ↓
Display (display.py) - Output Formatting
    ↓
Console Output
```

### User Interaction Flows

**Flow 1: Add Task**
1. User selects "Add Task" from menu
2. System prompts for title (validates non-empty)
3. System prompts for description (optional)
4. System creates task with auto-generated ID
5. System displays success message with task ID
6. Return to main menu

**Flow 2: View Tasks**
1. User selects "View All Tasks"
2. System retrieves all tasks sorted by ID
3. System displays formatted table with status indicators
4. If empty, display "No tasks found" message
5. Return to main menu

**Flow 3: Update Task**
1. User selects "Update Task"
2. System prompts for task ID
3. System validates task exists (error if not)
4. System displays current task details
5. System prompts for new title (show current, allow keeping same)
6. System prompts for new description (show current, allow keeping same)
7. System updates task and displays success
8. Return to main menu

**Flow 4: Delete Task**
1. User selects "Delete Task"
2. System prompts for task ID
3. System validates task exists (error if not)
4. System displays task details
5. System prompts for confirmation ("Are you sure? Y/N")
6. If confirmed, delete task and display success
7. Return to main menu

**Flow 5: Mark Complete/Incomplete**
1. User selects "Mark Complete" or "Mark Incomplete"
2. System prompts for task ID
3. System validates task exists (error if not)
4. System toggles status
5. System displays success with updated status
6. Return to main menu

## Testing Strategy

### Unit Tests

**test_task.py** - Task model tests
- Test task creation with valid data
- Test validation errors (empty title, too long title/description)
- Test mark_complete/mark_incomplete
- Test update method
- Test to_dict serialization

**test_task_service.py** - Service layer tests
- Test create_task with ID auto-increment
- Test get_task (found and not found)
- Test get_all_tasks (empty, single, multiple)
- Test update_task (success and task not found)
- Test delete_task (success and task not found)
- Test toggle_complete (both directions)
- Test storage integrity after operations

**test_ui.py** - UI component tests (optional for Phase I)
- Test display formatting
- Test menu validation (mock user input)

### Integration Tests (Optional for Phase I)

- End-to-end flow: Create → View → Update → Complete → Delete
- Error handling: Invalid IDs, empty inputs, etc.

### Test Coverage Goal

- Minimum 80% code coverage
- Focus on models and services (business logic)
- UI tests lower priority for Phase I

## Implementation Order

### Sequential Tasks (for `/sp.tasks` command)

1. **Setup Phase**
   - T001: Initialize Python project with UV (pyproject.toml)
   - T002: Create directory structure (src/, tests/)
   - T003: Configure pytest and coverage tools

2. **Phase 1: Core Model**
   - T004: Implement Task model (src/models/task.py)
   - T005: Write Task model unit tests (tests/test_task.py)
   - T006: Verify tests pass (Red-Green-Refactor)

3. **Phase 2: Business Logic**
   - T007: Implement TaskService (src/services/task_service.py)
   - T008: Write TaskService unit tests (tests/test_task_service.py)
   - T009: Verify tests pass

4. **Phase 3: User Interface**
   - T010: Implement Display module (src/ui/display.py)
   - T011: Implement Menu module (src/ui/menu.py)
   - T012: Write UI unit tests (tests/test_ui.py) - optional

5. **Phase 4: Application Integration**
   - T013: Implement main application (src/main.py)
   - T014: Manual testing of all 5 CRUD operations
   - T015: Fix any integration issues

6. **Phase 5: Documentation**
   - T016: Write README.md (setup and usage instructions)
   - T017: Create quickstart.md (this phase)
   - T018: Document any assumptions or limitations

7. **Phase 6: Validation**
   - T019: Run full test suite with coverage report
   - T020: Verify all acceptance scenarios from spec.md
   - T021: User acceptance testing (manual walkthrough)

## Windows-Specific Instructions

### WSL 2 Setup (Ubuntu 22.04)

**Prerequisites**:
1. Windows 11 or Windows 10 (version 2004+)
2. WSL 2 enabled with Ubuntu 22.04 distribution

**Setup Steps**:
```bash
# 1. Update Ubuntu
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.13 (if not available, use 3.11+)
sudo apt install python3.13 python3.13-venv python3-pip -y

# 3. Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Verify installations
python3.13 --version
uv --version

# 5. Clone repository and navigate to project
cd /path/to/project

# 6. Initialize UV project
uv venv
source .venv/bin/activate

# 7. Install dev dependencies
uv pip install pytest pytest-cov black mypy

# 8. Run application
uv run python src/main.py

# 9. Run tests
uv run pytest
```

**Path Considerations**:
- WSL filesystem: `/mnt/c/Users/...` (slow)
- Native Linux filesystem: `/home/user/...` (fast, recommended)
- Store project in Linux filesystem for better performance

**VS Code Integration**:
- Install "Remote - WSL" extension
- Open project in WSL: `code .` from WSL terminal
- Python extension will detect WSL Python interpreter

## Risk Assessment

### High-Priority Risks

1. **Input Validation Complexity**
   - Risk: Edge cases (very long inputs, special characters)
   - Mitigation: Comprehensive validation in Task model
   - Fallback: Strict length limits and character filtering

2. **Memory Constraints**
   - Risk: Storing 1000+ tasks in memory
   - Mitigation: Python dict is efficient for this scale
   - Fallback: Document recommended max tasks (10,000)

### Medium-Priority Risks

3. **User Experience**
   - Risk: Confusing menu or error messages
   - Mitigation: Clear, numbered menus and descriptive errors
   - Fallback: User testing and iteration

4. **Test Coverage**
   - Risk: Insufficient test coverage
   - Mitigation: Write tests before implementation (TDD)
   - Fallback: Manual testing of all user scenarios

### Low-Priority Risks

5. **Cross-Platform Compatibility**
   - Risk: Windows-specific console issues
   - Mitigation: Use stdlib only (platform-agnostic)
   - Fallback: WSL 2 as primary Windows environment

## Success Metrics

### Functional Validation
- ✅ All 12 functional requirements from spec.md implemented
- ✅ All 4 user stories (P1-P4) functional
- ✅ All acceptance scenarios pass manual testing

### Quality Metrics
- ✅ 80%+ test coverage
- ✅ All tests passing
- ✅ Black formatting applied
- ✅ Type hints on all functions

### Performance Metrics
- ✅ <100ms response time for all operations
- ✅ Supports 1000+ tasks without degradation

### Documentation
- ✅ README.md with setup instructions
- ✅ quickstart.md with usage examples
- ✅ Code comments on complex logic

## Next Steps

1. **Immediate**: Generate `research.md` (Phase 0 research findings)
2. **Next**: Generate `data-model.md` (Phase 1 detailed data structures)
3. **Then**: Generate `quickstart.md` (Phase 1 user guide)
4. **Finally**: Run `/sp.tasks` to create detailed task breakdown

---

**Plan Status**: Complete and ready for task generation
**Branch**: `001-cli-todo-app`
**Last Updated**: 2026-01-02
