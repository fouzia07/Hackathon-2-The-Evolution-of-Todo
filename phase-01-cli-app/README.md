# Phase I - CLI Todo Application

This folder contains the original Phase I implementation - a command-line interface (CLI) todo application with in-memory storage.

## Contents

- `src/` - Phase I source code
  - `main.py` - CLI entry point with menu loop
  - `models/` - Task dataclass with validation
  - `services/` - TaskService (in-memory CRUD)
  - `ui/` - Display and menu modules

- `tests/` - Phase I test suite
  - `test_task.py` - Task model tests (23 tests)
  - `test_task_service.py` - TaskService tests (24 tests)

- `pyproject.toml` - Phase I project configuration
- `uv.lock` - UV lock file for dependencies

## Running Phase I CLI

```bash
# From project root
cd phase1-cli
uv run python src/main.py

# Or with activated venv
python src/main.py
```

## Running Tests

```bash
cd phase1-cli
uv run pytest
uv run pytest --cov=src --cov-report=term-missing
```

## Features

- ✅ Add tasks with title and description
- ✅ View all tasks in formatted table
- ✅ Update task details
- ✅ Delete tasks with confirmation
- ✅ Mark tasks as complete/incomplete
- ✅ In-memory storage (no persistence)

## Specifications

See `../specs/001-cli-todo-app/` for detailed specifications, plan, and tasks.

## Evolution

This CLI application was the foundation for Phase II (full-stack web application). It demonstrates the project's evolution from a simple console app to a complete web-based system.

---

**Phase**: I (CLI)
**Status**: Complete
**Next Phase**: Phase II (Full-Stack Web) - See `../backend/` and `../frontend/`
