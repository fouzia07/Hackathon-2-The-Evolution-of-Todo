# CLI Todo Application - Phase I

A console-based todo application with in-memory task management, implementing CRUD operations through a menu-driven interface.

## Project Overview

This is Phase I of the Evolution of Todo project, focusing on fundamental task management operations in a CLI environment. Tasks are stored in memory and lost when the application exits (database persistence will be added in Phase II).

## Features

- ✅ **Add Task**: Create tasks with title and description
- ✅ **View Tasks**: Display all tasks in a formatted table with status indicators
- ✅ **Update Task**: Edit task title and/or description
- ✅ **Delete Task**: Remove tasks by ID with confirmation
- ✅ **Mark Complete/Incomplete**: Toggle task completion status

## Prerequisites

- **Python**: 3.11+ (3.13+ recommended)
- **UV**: Package manager for Python
- **OS**:
  - Linux (native)
  - macOS (native)
  - Windows (via WSL 2 with Ubuntu 22.04 recommended, or native with Git Bash/MINGW)

## Installation

### 1. Install Python

**Windows (if not already installed)**:
```bash
# Download from python.org or use winget
winget install Python.Python.3.12
```

**Linux/WSL 2**:
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip -y
```

**macOS**:
```bash
brew install python@3.12
```

### 2. Install UV Package Manager

```bash
# Linux/macOS/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 3. Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 4. Set Up Environment

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# Linux/macOS/WSL:
source .venv/bin/activate
# Windows (Git Bash/MINGW):
source .venv/Scripts/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install development dependencies (optional, for testing)
uv pip install pytest pytest-cov black mypy
```

## Usage

### Running the Application

```bash
# With UV (recommended)
uv run python src/main.py

# Or with activated venv
python src/main.py
```

### Main Menu

When you run the application, you'll see:

```
==================================================
               TODO APPLICATION
==================================================
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit
==================================================
Enter your choice (1-7):
```

### Example Workflow

1. **Add a task**:
   - Choose option 1
   - Enter title: "Buy groceries"
   - Enter description: "Milk, eggs, bread"

2. **View all tasks**:
   - Choose option 2
   - See your tasks in a formatted table

3. **Mark task complete**:
   - Choose option 5
   - Enter task ID (e.g., 1)
   - Task status changes to [✓]

4. **Update task**:
   - Choose option 3
   - Enter task ID
   - Enter new title/description (or press Enter to keep current)

5. **Delete task**:
   - Choose option 4
   - Enter task ID
   - Confirm deletion

## Testing

### Run All Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_task.py -v
uv run pytest tests/test_task_service.py -v
```

### Expected Test Results

- **Task model**: 23 tests covering validation, methods, edge cases
- **TaskService**: 24 tests covering CRUD operations, ID management
- **Coverage**: >90% for models and services

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic (CRUD)
│   └── ui/
│       ├── __init__.py
│       ├── display.py       # Output formatting
│       └── menu.py          # Input handling
│
├── tests/
│   ├── __init__.py
│   ├── test_task.py         # Task model tests
│   └── test_task_service.py # TaskService tests
│
├── specs/
│   └── 001-cli-todo-app/    # Feature specifications
│
├── specs_history/
│   └── phase1/              # Spec versions
│
├── pyproject.toml           # Project configuration
├── README.md                # This file
├── CLAUDE.md                # Claude Code instructions
└── .gitignore               # Git ignore patterns
```

## Phase I Scope & Constraints

### What's Included
- ✅ In-memory task storage (Dict-based)
- ✅ CLI menu-driven interface
- ✅ Full CRUD operations
- ✅ Task validation (title 1-200 chars, description 0-1000 chars)
- ✅ Auto-incremented task IDs (never reused)
- ✅ Completion status tracking

### What's NOT Included (Future Phases)
- ❌ Data persistence (database)
- ❌ Web interface
- ❌ Multi-user support
- ❌ Authentication
- ❌ AI/NLP features
- ❌ Cloud deployment
- ❌ Advanced search/filtering

## Code Quality

### Formatting

```bash
# Format code with Black
uv run black src/ tests/

# Check formatting
uv run black --check src/ tests/
```

### Type Checking

```bash
# Run mypy (optional)
uv run mypy src/
```

## Troubleshooting

### Python not found

**Error**: `python: command not found`

**Solution**: Install Python or use `python3`:
```bash
python3 --version
python3 src/main.py
```

### UV not found

**Error**: `uv: command not found`

**Solution**: Reinstall UV and ensure it's in PATH:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart terminal
```

### Module not found errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from project root:
```bash
pwd  # Should show project root
ls   # Should show src/ directory
uv run python src/main.py
```

### WSL 2 performance issues (Windows)

**Solution**: Store project in Linux filesystem, not /mnt/c/:
```bash
# Good (fast):
cd ~/projects/todo-cli

# Bad (slow):
cd /mnt/c/Users/YourName/projects/todo-cli
```

## Development

### Contributing

1. Follow spec-driven development workflow (see CLAUDE.md)
2. Write tests before implementation (TDD)
3. Run `black` for formatting
4. Ensure all tests pass before committing
5. Maintain >80% code coverage

### Next Steps (Phase II)

Phase II will add:
- PostgreSQL database persistence
- FastAPI REST API
- JWT authentication
- Next.js web UI

## Constitutional Compliance

This project follows the AI-Native Spec-Driven Development principles:

- ✅ **Spec-First**: All code traceable to spec.md
- ✅ **No Manual Coding**: Code generated via Claude Code
- ✅ **Reproducibility**: Specs and prompts preserved
- ✅ **Phase I Constraints**: In-memory, CLI-only, transient state

See `.specify/memory/constitution.md` for full project constitution.

## License

[Add your license here]

## Contact

[Add contact information]

---

**Phase**: I (CLI)
**Version**: 0.1.0
**Last Updated**: 2026-01-02
