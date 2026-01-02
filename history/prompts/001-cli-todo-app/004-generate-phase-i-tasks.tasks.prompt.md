---
id: 004
title: Generate Phase I Tasks
stage: tasks
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5
feature: 001-cli-todo-app
branch: 001-cli-todo-app
user: AI Book Creator
command: /sp.tasks
labels: ["tasks", "phase-i", "implementation", "breakdown"]
links:
  spec: specs/001-cli-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-todo-app/tasks.md
tests:
  - N/A (task planning phase)
---

## Prompt

```text
/sp.task # /sp.task – Phase I: Todo In-Memory Python Console App

## Objective
Break down Phase I into actionable development tasks for Claude Code using Spec-Driven Development.

## Requirements to cover in tasks
- Implement all 5 basic features: **Add, Delete, Update, View, Mark Complete**
- Use **Spec-Kit Plus** and **Claude Code** (no manual coding)
- Follow **clean code principles** and proper **Python project structure**
- Include **UV setup** in environment and instructions
- Create separate folders for:
  - `specs` → all generated specification files
  - `specs_history` → all previous/iterated specification files

## Deliverables to generate via tasks
1. GitHub repository with:
   - `Constitution` file
   - `/specs` folder with spec files
   - `/specs_history` folder
   - `/src` folder with Python code
   - `README.md` with setup instructions
   - `CLAUDE.md` with Claude Code instructions
2. Working console app demonstrating:
   - Adding tasks (title + description)
   - Viewing all tasks with status
   - Updating task details
   - Deleting tasks by ID
   - Marking tasks complete/incomplete

## Task breakdown guidelines for Claude
1. Setup project environment with Python 3.13+ and UV
2. Generate spec for **Add task** → implement via Claude Code → store in `/specs` → copy to `/specs_history`
3. Generate spec for **View tasks** → implement → save in `/specs` and `/specs_history`
4. Generate spec for **Update task** → implement → save in `/specs` and `/specs_history`
5. Generate spec for **Delete task** → implement → save in `/specs` and `/specs_history`
6. Generate spec for **Mark Complete/Incomplete** → implement → save in `/specs` and `/specs_history`
7. Create **README.md** and **CLAUDE.md** with instructions for running the console app with UV
8. Test all functionality and generate report for completeness

## Constraints for tasks
- All code must be generated via Claude Code using spec-driven development
- Specs must be iterated until Claude generates correct output
- Do not write manual code

## Success criteria
- Fully working console app with all 5 features
- Correct folder structure with separate `/specs` and `/specs_history`
- Environment setup works on Windows (WSL 2) and Linux
- README and CLAUDE instructions complete
```

## Response snapshot

Created comprehensive task breakdown for Phase I CLI Todo Application with 34 tasks across 9 implementation phases.

**Task Organization**:
- **9 Phases**: Setup (5 tasks) → Model (4) → Service (3) → UI (3) → Integration (3) → Quality (3) → Documentation (3) → Acceptance (6) → Compliance (4)
- **34 Total Tasks**: T001-T034 covering full implementation lifecycle
- **Parallel Opportunities**: 15 tasks marked [P] can run concurrently
- **User Story Mapping**: Tasks labeled with [US1-US4] for traceability

**Phase Breakdown**:

1. **Phase 1 - Setup (T001-T005)**: Project initialization
   - Install Python 3.13+ and UV
   - Initialize pyproject.toml
   - Create directory structure (src/, tests/, specs_history/)
   - Install dev dependencies (pytest, black, mypy)
   - Create .gitignore

2. **Phase 2 - Core Model (T006-T009)**: Task data structure
   - Archive spec to specs_history/phase1/
   - Implement Task model with dataclass
   - Write 10+ unit tests for Task model
   - Run tests and verify pass (TDD approach)

3. **Phase 3 - Business Logic (T010-T012)**: TaskService
   - Implement TaskService with Dict storage
   - Write 13+ unit tests for CRUD operations
   - Run tests and verify pass

4. **Phase 4 - UI (T013-T015)**: Display and Menu
   - Implement Display module (task formatting)
   - Implement Menu module (input handling)
   - Write UI tests (optional)

5. **Phase 5 - Integration (T016-T018)**: Main application
   - Implement main.py with menu loop
   - Manual testing of all 5 CRUD operations
   - Fix integration bugs

6. **Phase 6 - Quality (T019-T021)**: Code standards
   - Format with Black
   - Run pytest with coverage (target ≥80%)
   - Run mypy type checking (optional)

7. **Phase 7 - Documentation (T022-T024)**: User guides
   - Create README.md (setup + usage)
   - Create CLAUDE.md (Claude Code instructions)
   - Archive final spec to specs_history/

8. **Phase 8 - Acceptance (T025-T030)**: Validation
   - Verify US1 acceptance scenarios (Create/View)
   - Verify US2 acceptance scenarios (Mark Complete)
   - Verify US3 acceptance scenarios (Update)
   - Verify US4 acceptance scenarios (Delete)
   - Verify edge cases (invalid input, errors)
   - Generate test report

9. **Phase 9 - Compliance (T031-T034)**: Constitutional audit
   - Verify Spec-First principle
   - Verify No Manual Coding principle
   - Verify Phase I constraints (in-memory, CLI-only)
   - Verify Technical Standards (Black, type hints, coverage)

**Key Features**:
- **TDD Approach**: Tests written before implementation (T008 before T007, T011 before T010)
- **Spec Versioning**: Spec archived at T006 (v1) and T024 (final) for reproducibility
- **Parallel Execution**: 15 tasks can run concurrently (marked with [P])
- **Clear Dependencies**: Sequential tasks explicitly ordered (T007 depends on T008, etc.)
- **Acceptance Criteria**: Each task has verification steps and expected outcomes

**Implementation Strategy**:
- **MVP First**: Complete Phase 1-5 for minimal working app
- **Incremental**: 5 sprints, one phase per sprint
- **TDD**: Red (write tests) → Green (implement) → Refactor (improve)

**Critical Success Factors**:
1. Spec versioning (T006, T024) - preserves reproducibility
2. TDD discipline (tests before code) - ensures quality
3. Manual testing (T017) - catches integration issues
4. Error handling (T016) - all exceptions caught in main.py
5. Documentation (T022-T023) - clear setup instructions

**Constitutional Compliance**:
- ✅ Spec-First: Tasks T031 verifies spec.md complete before code
- ✅ No Manual Coding: All code via Claude Code (T032)
- ✅ Phase I Constraints: In-memory, CLI-only, transient (T033)
- ✅ Technical Standards: Black, type hints, 80%+ coverage (T034)

**Deliverables**:
```
Repository Structure:
├── src/
│   ├── models/task.py (T007)
│   ├── services/task_service.py (T010)
│   ├── ui/display.py (T013)
│   ├── ui/menu.py (T014)
│   └── main.py (T016)
├── tests/
│   ├── test_task.py (T008)
│   ├── test_task_service.py (T011)
│   └── test_ui.py (T015 - optional)
├── specs_history/phase1/
│   ├── spec-v1.md (T006)
│   ├── spec-final.md (T024)
│   └── test-report.md (T030)
├── README.md (T022)
├── CLAUDE.md (T023)
└── pyproject.toml (T002)
```

## Outcome

- ✅ Impact: Complete task breakdown ready for AI-assisted implementation, 34 tasks covering full development lifecycle
- 🧪 Tests: TDD approach enforced (tests before code), 80%+ coverage target, acceptance testing planned
- 📁 Files: Created tasks.md with 34 tasks, dependencies, parallel opportunities, acceptance criteria
- 🔁 Next prompts: Begin implementation with T001 (Install Python/UV), follow sequential order through T034
- 🧠 Reflection: Task breakdown successfully captures all implementation requirements with clear dependencies. Nine-phase structure enables incremental delivery (MVP after Phase 5, full validation after Phase 9). TDD approach ensures quality (write tests → implement → refactor). Spec versioning at T006 and T024 preserves reproducibility per constitutional requirements. 15 parallel opportunities identified for efficiency. Manual testing at T017 critical for catching integration issues. Constitutional compliance verification at T031-T034 ensures all principles satisfied.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks defined with clear acceptance criteria and dependencies
- Graders run and results (PASS/FAIL): PASS - Task dependencies validated, parallel opportunities identified, TDD approach enforced
- Prompt variant (if applicable): Standard /sp.tasks with emphasis on spec versioning and Claude Code integration
- Next experiment (smallest change to try): Monitor whether 34 tasks is optimal granularity, or if consolidation needed (e.g., combine T007+T008+T009 into single "Implement and test Task model" task)
