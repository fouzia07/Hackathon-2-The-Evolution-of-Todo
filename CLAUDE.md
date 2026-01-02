# Claude Code Instructions

This file provides guidance for Claude Code when working with the CLI Todo Application project.

## Purpose

This document ensures Claude Code follows the project's constitutional principles and development workflow when making changes or adding features to the Todo CLI application.

## Project Context

**Project Name**: CLI Todo Application - Phase I
**Type**: Console-based task management system
**Version**: 0.1.0
**Phase**: I (CLI with in-memory storage)
**Constitutional Framework**: AI-Native Spec-Driven Development

### Core Principles

This project follows 8 constitutional principles defined in `.specify/memory/constitution.md`:

1. **Spec-First Development**: All code changes must originate from specifications
2. **No Manual Coding**: All code generation via Claude Code (AI-native)
3. **Agentic Execution**: Sequential workflow: Spec → Plan → Tasks → Implement
4. **Incremental Evolution**: Phase-based evolution (CLI → API → Web → AI)
5. **Reproducibility**: All specs, prompts, and artifacts preserved
6. **Cloud-Native Architecture**: Containerized, stateless, API-first (future phases)
7. **Technology Stack Consistency**: Python, FastAPI, PostgreSQL, Next.js
8. **Phase-Specific Constraints**: Phase I = CLI-only, in-memory, no persistence

## Architecture Overview

### Current State (Phase I)

```
src/
├── models/task.py          # Task dataclass with validation
├── services/task_service.py # Business logic (CRUD operations)
├── ui/
│   ├── display.py          # Output formatting
│   └── menu.py             # Input handling
└── main.py                 # Application entry point

tests/
├── test_task.py            # Task model tests (23 tests)
└── test_task_service.py    # TaskService tests (24 tests)
```

### Technology Stack

- **Language**: Python 3.12+ (3.11+ acceptable)
- **Package Manager**: UV (Astral)
- **Testing**: pytest, pytest-cov
- **Code Quality**: Black (formatting), mypy (type checking)
- **Storage**: In-memory Dict[int, Task] (no persistence)
- **Dependencies**: Standard library only (no external packages for core functionality)

### Design Patterns

1. **Clean Architecture**: Models → Services → UI → Main
2. **Separation of Concerns**: Business logic isolated from UI
3. **Test-Driven Development**: Tests written before implementation
4. **Type Safety**: Full type hints (PEP 484)
5. **Dataclass Pattern**: Immutable-by-convention with validation in `__post_init__`

## Development Workflow

### For New Features

1. **Specify** (`/sp.specify`):
   - Create or update `specs/<feature-name>/spec.md`
   - Define user stories, functional requirements, success criteria
   - Archive versions in `specs_history/phase<N>/`

2. **Plan** (`/sp.plan`):
   - Create `specs/<feature-name>/plan.md`
   - Define architecture, modules, technical decisions
   - Identify dependencies and risks

3. **Tasks** (`/sp.tasks`):
   - Create `specs/<feature-name>/tasks.md`
   - Break down into testable tasks with acceptance criteria
   - Mark dependencies and parallel opportunities

4. **Implement** (`/sp.implement`):
   - Execute tasks sequentially following TDD
   - Run tests after each change
   - Update task status as work progresses

### For Bug Fixes

1. Write a failing test that reproduces the bug
2. Fix the code to make the test pass
3. Run full test suite to ensure no regressions
4. Format code with Black

### For Code Changes

**ALWAYS:**
- Write tests before implementation (TDD)
- Run `uv run pytest` after changes
- Maintain type hints on all functions
- Follow existing code structure and patterns
- Preserve validation logic (title 1-200 chars, description 0-1000 chars)

**NEVER:**
- Add database persistence (Phase II feature)
- Add web interface (Phase III feature)
- Add authentication (Phase II feature)
- Add external dependencies for core functionality
- Bypass validation in Task model
- Reuse deleted task IDs

## Task Context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent and project constitution
- Prompt History Records (PHRs) are created for significant work
- Architectural Decision Record (ADR) suggestions are made for significant decisions
- All changes are small, testable, and reference code precisely
- Tests pass and coverage remains ≥80%

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Code Generation Guidelines

### Task Model (`src/models/task.py`)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    is_complete: bool = False

    def __post_init__(self) -> None:
        # Validation logic here
        pass
```

**Rules:**
- Title: 1-200 characters (stripped, non-empty)
- Description: 0-1000 characters
- ID: Positive integer, auto-assigned, never reused
- Use `ValidationError` for validation failures

### TaskService (`src/services/task_service.py`)

```python
class TaskService:
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
```

**Rules:**
- Use `Dict[int, Task]` for O(1) lookups
- Increment `_next_id` after creation (never decrement)
- Raise `TaskNotFoundError` for missing tasks
- Return sorted lists by ID for `get_all_tasks()`

### UI Modules (`src/ui/`)

**Display (`display.py`)**:
- Use emoji indicators: [✓] for complete, [ ] for incomplete
- Use ✅ for success messages, ❌ for errors
- Format tables with 80-character width
- Truncate long text with "..." suffix

**Menu (`menu.py`)**:
- Validate all user input with try-except
- Handle EOFError and KeyboardInterrupt gracefully
- Return -1 or empty strings to signal cancellation
- Show current values when updating tasks

### Main Application (`src/main.py`)

- Wrap main loop in try-except for KeyboardInterrupt
- Call handler functions for each menu option
- Display welcome message on startup
- Show goodbye message on exit (option 7)

## Testing Standards

### Test Structure

```python
class TestFeatureName:
    """Tests for specific feature."""

    @pytest.fixture
    def service(self):
        """Create fresh instance for each test."""
        return TaskService()

    def test_behavior_description(self, service):
        """Test that X does Y when Z."""
        # Arrange
        # Act
        # Assert
```

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Target**: 90%+ for models and services
- **Run**: `uv run pytest --cov=src --cov-report=term-missing`

### Test Categories

1. **Unit Tests**: Test individual methods in isolation
2. **Integration Tests**: Test workflows across multiple components
3. **Edge Cases**: Empty inputs, length limits, invalid IDs
4. **Error Handling**: ValidationError, TaskNotFoundError

## File Locations

### Specifications
- Current spec: `specs/001-cli-todo-app/spec.md`
- Implementation plan: `specs/001-cli-todo-app/plan.md`
- Task breakdown: `specs/001-cli-todo-app/tasks.md`
- Archived versions: `specs_history/phase1/`

### Constitution
- Project principles: `.specify/memory/constitution.md`

### Source Code
- Models: `src/models/`
- Services: `src/services/`
- UI: `src/ui/`
- Main: `src/main.py`

### Tests
- Unit tests: `tests/test_*.py`
- Test fixtures: `tests/conftest.py` (if needed)

### Configuration
- Project config: `pyproject.toml`
- Git ignore: `.gitignore`
- Environment: `.env` (not used in Phase I)

## Running the Application

### Development

```bash
# Run the application
uv run python src/main.py

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_task.py -v

# Format code
uv run black src/ tests/

# Type check (optional)
uv run mypy src/
```

### Testing Workflow

When making changes:

1. Write failing test first
2. Implement the feature
3. Run tests: `uv run pytest`
4. Format code: `uv run black src/ tests/`
5. Verify coverage: `uv run pytest --cov=src`

## Phase-Specific Constraints

### Phase I (Current)

**What's Allowed:**
- CLI menu-driven interface
- In-memory storage (Dict-based)
- Full CRUD operations
- Task validation and status tracking
- Standard library usage

**What's Forbidden:**
- Database persistence (PostgreSQL, SQLite, files)
- Web interface (FastAPI, Flask)
- Authentication/authorization
- Multi-user support
- External API calls
- File-based storage
- Configuration files for data

### Future Phases

**Phase II** (not yet implemented):
- PostgreSQL database with SQLAlchemy
- FastAPI REST API
- JWT authentication
- Docker containerization

**Phase III** (not yet implemented):
- Next.js web interface
- React components
- TailwindCSS styling

**Phase IV** (not yet implemented):
- AI/NLP features
- Smart scheduling
- Natural language input

## Default Policies (Must Follow)

- Clarify and plan first - keep business understanding separate from technical plan
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing
- Never hardcode secrets or tokens; use `.env` and docs
- Prefer the smallest viable diff; do not refactor unrelated code
- Cite existing code with code references (file_path:line_number)
- Keep reasoning private; output only decisions, artifacts, and justifications

### Execution Contract for Every Request

1) Confirm surface and success criteria (one sentence)
2) List constraints, invariants, non-goals
3) Produce the artifact with acceptance checks inlined
4) Add follow-ups and risks (max 3 bullets)
5) Create PHR for significant work
6) If architecturally significant decisions made, suggest ADR

### Minimum Acceptance Criteria

- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant
- Tests pass and coverage ≥80%

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Common Tasks

### Adding a New Task Field

1. Update `specs/001-cli-todo-app/spec.md` with new requirement
2. Update `src/models/task.py` dataclass
3. Add validation in `__post_init__` if needed
4. Update `tests/test_task.py` with new test cases
5. Update `TaskService` methods if needed
6. Update display functions in `src/ui/display.py`
7. Run tests and format code

### Fixing a Bug

1. Write failing test in appropriate test file
2. Run test to confirm it fails: `uv run pytest tests/test_<module>.py -v`
3. Fix the bug in source code
4. Run test to confirm it passes
5. Run full test suite: `uv run pytest`
6. Format code: `uv run black src/ tests/`

### Adding a New Menu Option

1. Update spec with new user story
2. Add menu option in `src/ui/menu.py::display_main_menu()`
3. Update `get_menu_choice()` validation range
4. Create handler function in `src/main.py`
5. Add elif branch in main loop
6. Write tests for new functionality
7. Manual test the new option

## Error Handling Patterns

### Validation Errors

```python
try:
    task = service.create_task(title, description)
except ValidationError as e:
    display_error(str(e))
```

### Task Not Found

```python
try:
    task = service.get_task(task_id)
    if task is None:
        display_error(f"Task with ID {task_id} not found.")
        return
except TaskNotFoundError as e:
    display_error(str(e))
```

### User Cancellation

```python
task_id = prompt_task_id()
if task_id == -1:  # User cancelled
    return
```

### Keyboard Interrupt

```python
try:
    # Main loop
    pass
except KeyboardInterrupt:
    print("\n\nExiting...")
    break
```

## Constitutional Compliance

When working on this project, ensure:

1. **All code is AI-generated**: No manual coding allowed
2. **Spec-first**: Changes start with spec updates
3. **Tests-first**: TDD approach (Red-Green-Refactor)
4. **Reproducibility**: Document decisions and preserve artifacts
5. **Phase constraints**: Respect Phase I limitations
6. **Type safety**: Maintain type hints throughout
7. **Code quality**: Run Black and pytest before committing
8. **Architecture**: Follow clean architecture patterns

## Best Practices

1. **Single Responsibility**: Each function does one thing well
2. **DRY Principle**: Extract common patterns into functions
3. **Explicit is Better**: Clear variable names, no magic numbers
4. **Fail Fast**: Validate inputs early, raise exceptions immediately
5. **Type Everything**: Use type hints on all function signatures
6. **Test Everything**: Minimum 80% coverage, aim for 90%+
7. **Document Why, Not What**: Code should be self-documenting
8. **Keep It Simple**: Prefer simple solutions over clever ones

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/001-cli-todo-app/` — Current feature specification, plan, tasks
- `specs_history/phase1/` — Archived specification versions
- `src/` — Application source code
- `tests/` — Unit and integration tests
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Questions?

For questions about:
- **Project principles**: See `.specify/memory/constitution.md`
- **Feature requirements**: See `specs/001-cli-todo-app/spec.md`
- **Architecture decisions**: See `specs/001-cli-todo-app/plan.md`
- **Task breakdown**: See `specs/001-cli-todo-app/tasks.md`
- **Code patterns**: Read existing code in `src/` directory
- **Testing patterns**: Read existing tests in `tests/` directory

---

**Last Updated**: 2026-01-02
**Phase**: I (CLI)
**Version**: 0.1.0
