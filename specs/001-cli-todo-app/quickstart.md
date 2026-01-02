# Quickstart Guide: CLI Todo Application (Phase I)

**Feature**: CLI Todo Application
**Branch**: 001-cli-todo-app
**Date**: 2026-01-02
**Purpose**: Quick setup and usage guide for Phase I implementation

---

## Prerequisites

### System Requirements

- **Python**: 3.13+ (or 3.11+ as fallback)
- **UV**: Package manager (installation instructions below)
- **Operating System**:
  - Linux (native)
  - macOS (native)
  - Windows (via WSL 2 with Ubuntu 22.04)

### Windows Users: WSL 2 Setup

If you're on Windows, you must use WSL 2 with Ubuntu 22.04:

```powershell
# In PowerShell (as Administrator)
wsl --install -d Ubuntu-22.04

# Restart your computer

# Open Ubuntu terminal and update
sudo apt update && sudo apt upgrade -y
```

---

## Installation

### Step 1: Install Python 3.13

**Ubuntu/Debian (WSL 2)**:
```bash
sudo apt install python3.13 python3.13-venv python3-pip -y

# Verify installation
python3.13 --version
```

**macOS** (using Homebrew):
```bash
brew install python@3.13

# Verify installation
python3.13 --version
```

**If Python 3.13 is unavailable**: Use Python 3.11+ as fallback.

### Step 2: Install UV Package Manager

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed - restart terminal after)
source ~/.bashrc  # or ~/.zshrc for zsh

# Verify installation
uv --version
```

### Step 3: Clone Repository

```bash
# Navigate to your projects directory
cd ~/projects  # or your preferred location

# Clone the repository (replace with actual repo URL)
git clone <repository-url>
cd <repository-name>

# Checkout the feature branch
git checkout 001-cli-todo-app
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate  # Windows (PowerShell)

# Install development dependencies
uv pip install pytest pytest-cov black mypy
```

---

## Running the Application

### Start the Todo App

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Run the application
uv run python src/main.py

# OR (if in activated venv)
python src/main.py
```

### First Launch

You should see the main menu:

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

---

## Usage Examples

### Example 1: Create Your First Task

```
Enter choice (1-7): 1

Enter task title: Buy groceries
Enter task description: Milk, eggs, bread, coffee

✓ Task created successfully! (ID: 1)
```

### Example 2: View All Tasks

```
Enter choice (1-7): 2

=== Your Tasks ===
ID | Status | Title            | Description
---+--------+------------------+---------------------------
1  | [ ]    | Buy groceries    | Milk, eggs, bread, coffee

Total: 1 task(s)
```

### Example 3: Mark Task Complete

```
Enter choice (1-7): 5

Enter task ID: 1

✓ Task marked as complete!

=== Updated Task ===
ID | Status | Title            | Description
---+--------+------------------+---------------------------
1  | [✓]    | Buy groceries    | Milk, eggs, bread, coffee
```

### Example 4: Add Multiple Tasks

```
# Add Task 2
Enter choice (1-7): 1
Enter task title: Finish Q4 report
Enter task description: Complete revenue analysis and projections
✓ Task created successfully! (ID: 2)

# Add Task 3
Enter choice (1-7): 1
Enter task title: Call dentist
Enter task description: Schedule 6-month checkup
✓ Task created successfully! (ID: 3)

# View all tasks
Enter choice (1-7): 2

=== Your Tasks ===
ID | Status | Title            | Description
---+--------+------------------+------------------------------------
1  | [✓]    | Buy groceries    | Milk, eggs, bread, coffee
2  | [ ]    | Finish Q4 report | Complete revenue analysis...
3  | [ ]    | Call dentist     | Schedule 6-month checkup

Total: 3 task(s)
```

### Example 5: Update a Task

```
Enter choice (1-7): 3

Enter task ID: 2

Current task:
ID: 2
Title: Finish Q4 report
Description: Complete revenue analysis and projections
Status: Incomplete

Enter new title (press Enter to keep current): Q4 Financial Report
Enter new description (press Enter to keep current): Revenue, expenses, and Q1 projections

✓ Task updated successfully!
```

### Example 6: Delete a Task

```
Enter choice (1-7): 4

Enter task ID: 3

Current task:
ID: 3
Title: Call dentist
Description: Schedule 6-month checkup
Status: Incomplete

Are you sure you want to delete this task? (Y/N): Y

✓ Task deleted successfully!
```

### Example 7: Toggle Completion Status

```
# Mark task 2 as complete
Enter choice (1-7): 5
Enter task ID: 2
✓ Task marked as complete!

# Mark task 2 as incomplete again
Enter choice (1-7): 6
Enter task ID: 2
✓ Task marked as incomplete!
```

---

## Common Operations

### Full Workflow Example

Complete workflow demonstrating all features:

```bash
# 1. Start application
python src/main.py

# 2. Add 3 tasks
→ Option 1: Add "Write blog post" / "Tech tutorial on Python"
→ Option 1: Add "Review PR #42" / "Check code quality and tests"
→ Option 1: Add "Update documentation" / "Add API examples"

# 3. View all tasks
→ Option 2: View All Tasks
# Shows 3 incomplete tasks

# 4. Complete first task
→ Option 5: Mark Complete (ID: 1)

# 5. Update second task
→ Option 3: Update Task (ID: 2)
# New title: "Review and merge PR #42"

# 6. View updated list
→ Option 2: View All Tasks
# Shows 1 complete, 2 incomplete

# 7. Delete third task
→ Option 4: Delete Task (ID: 3)

# 8. View final list
→ Option 2: View All Tasks
# Shows tasks 1 and 2 only

# 9. Exit
→ Option 7: Exit
```

---

## Troubleshooting

### Problem: "Command not found: python3.13"

**Solution**: Python 3.13 not installed. Use Python 3.11+ as fallback:
```bash
python3.11 --version  # Check if 3.11 is available
python3 --version     # Check default Python version

# Update commands to use python3 instead of python3.13
uv run python3 src/main.py
```

### Problem: "Command not found: uv"

**Solution**: UV not installed or not in PATH:
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (restart terminal after)
source ~/.bashrc

# Verify
uv --version
```

### Problem: "ModuleNotFoundError: No module named 'src'"

**Solution**: Run from project root directory:
```bash
# Check current directory
pwd

# Navigate to project root (should contain src/ directory)
cd /path/to/project

# Verify src/ exists
ls src/
# Should show: main.py, models/, services/, ui/

# Run again
python src/main.py
```

### Problem: "Title cannot be empty" when adding task

**Solution**: Title is required and cannot be whitespace-only:
```bash
# Invalid entries:
Title: ""        # Empty
Title: "   "     # Whitespace only

# Valid entry:
Title: "My Task" # At least one non-whitespace character
```

### Problem: "Task with ID X not found"

**Solution**: Task was deleted or never existed. View all tasks first:
```bash
# View current tasks to see valid IDs
→ Option 2: View All Tasks

# Use an ID from the list (e.g., 1, 2, 4)
# Note: If task 3 was deleted, ID 3 no longer exists
```

### Problem: WSL 2 Performance Issues

**Solution**: Store project in Linux filesystem (not /mnt/c/):
```bash
# Slow (Windows filesystem mounted in WSL)
cd /mnt/c/Users/YourName/projects/todo-app

# Fast (Native Linux filesystem)
cd ~/projects/todo-app

# Move project to Linux filesystem
mv /mnt/c/Users/YourName/projects/todo-app ~/projects/
```

---

## Testing

### Run Unit Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_task.py

# Run with verbose output
pytest -v
```

### Expected Test Output

```
======================== test session starts ========================
collected 15 items

tests/test_task.py .....                                      [ 33%]
tests/test_task_service.py ..........                         [100%]

======================== 15 passed in 0.45s ========================

---------- coverage: platform linux, python 3.13.0 ----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/__init__.py                       0      0   100%
src/models/__init__.py                0      0   100%
src/models/task.py                   35      2    94%   45-46
src/services/__init__.py              0      0   100%
src/services/task_service.py         48      3    94%   78-80
---------------------------------------------------------------
TOTAL                                83      5    94%
```

---

## Code Quality Checks

### Format Code with Black

```bash
# Check formatting
black --check src/ tests/

# Apply formatting
black src/ tests/
```

### Type Checking with mypy (Optional)

```bash
# Run type checker
mypy src/

# Expected: No errors or type issues
```

---

## Development Tips

### Quick Development Loop

```bash
# 1. Make code changes in src/

# 2. Run tests to verify
pytest

# 3. Format code
black src/

# 4. Manual testing
python src/main.py

# 5. Commit changes
git add .
git commit -m "Implement feature X"
```

### VS Code Setup (Recommended)

1. Install "Remote - WSL" extension (Windows only)
2. Open project in WSL: `code .` from WSL terminal
3. Install Python extension
4. Select Python interpreter: `.venv/bin/python`
5. Configure pytest in Test Explorer

### Debugging

Add print statements or use Python debugger:

```python
# Add to any file for debugging
import pdb; pdb.set_trace()

# Or use print
print(f"Debug: task_id={task_id}, task={task}")
```

---

## Data Persistence Note

**IMPORTANT**: Phase I uses **in-memory storage only**. All tasks are lost when the application exits.

```bash
# Session 1
python src/main.py
→ Add tasks 1, 2, 3
→ Exit

# Session 2 (new run)
python src/main.py
→ View All Tasks
# Result: Empty list (tasks from Session 1 are gone)
```

**Phase II** will add database persistence (PostgreSQL).

---

## Next Steps

### After Completing Phase I

1. **Validate All Features**: Test all 5 CRUD operations manually
2. **Run Full Test Suite**: `pytest --cov=src`
3. **Review Code Quality**: Ensure 80%+ coverage, Black formatting applied
4. **Document Assumptions**: Note any limitations or edge cases
5. **Prepare for Phase II**: Database design, API endpoints

### Phase II Preview (Future Work)

- **Database**: PostgreSQL with SQLAlchemy ORM
- **API**: FastAPI REST endpoints
- **Frontend**: Next.js web interface
- **Auth**: JWT-based authentication
- **Persistence**: Tasks saved between sessions

---

## Support

### Getting Help

- **Documentation**: See `specs/001-cli-todo-app/` for detailed specs and plans
- **Issues**: Check GitHub Issues for known problems
- **Constitution**: Review `.specify/memory/constitution.md` for project principles

### Reporting Bugs

Create a GitHub issue with:
1. Python version (`python --version`)
2. UV version (`uv --version`)
3. Operating system
4. Steps to reproduce
5. Expected vs actual behavior
6. Error messages (if any)

---

**Quickstart Guide Status**: Complete
**Branch**: `001-cli-todo-app`
**Next Step**: Run `/sp.tasks` to generate detailed implementation tasks
