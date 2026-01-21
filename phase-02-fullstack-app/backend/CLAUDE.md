# Claude Code Instructions for Backend

This file provides guidance for Claude Code when working on the backend components of the Full-Stack Web Todo Application.

## Purpose

This document ensures Claude Code follows the project's architectural principles and development workflow when making changes to the backend services.

## Project Context

**Project**: Full-Stack Web Todo Application - Phase II
**Type**: FastAPI backend with SQLModel ORM
**Architecture**: REST API with JWT authentication
**Database**: PostgreSQL via SQLModel
**Phase**: II (Web with Authentication & Persistence)

## Architecture Overview

### Backend Structure

```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic
│   ├── api/             # API endpoints (v1)
│   ├── auth/            # Authentication utilities
│   ├── database/        # Database connection and session management
│   ├── utils/           # Utility functions
│   ├── config/          # Configuration management
│   └── middleware/      # Request middleware
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── contract/       # API contract tests
└── requirements.txt    # Dependencies
```

### Technology Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel 0.0.16
- **Authentication**: python-jose for JWT, passlib for password hashing
- **Database**: PostgreSQL (asyncpg driver)
- **Testing**: pytest, pytest-asyncio
- **Dependencies**: uv for package management

### Design Patterns

1. **Clean Architecture**: Models → Schemas → Services → API → Main
2. **Separation of Concerns**: Business logic isolated from API endpoints
3. **Dependency Injection**: Use FastAPI's built-in DI for services
4. **Type Safety**: Full type hints with Pydantic models
5. **SQLModel Pattern**: Declarative models with validation

## Development Workflow

### For New Features

1. **Define Schemas**: Create Pydantic models for request/response
2. **Create Models**: Define SQLModel database models
3. **Implement Services**: Write business logic in services/
4. **Create Endpoints**: Add API routes in api/ modules
5. **Add Middleware**: Implement authentication/authorization if needed
6. **Write Tests**: Create unit and integration tests

### For API Endpoints

**ALWAYS:**
- Use proper HTTP status codes (200, 201, 204, 400, 401, 404, 500)
- Validate request data with Pydantic schemas
- Handle errors gracefully with proper responses
- Add authentication/authorization checks where needed
- Include comprehensive API documentation

**NEVER:**
- Expose raw database models in API responses
- Bypass authentication for protected endpoints
- Return sensitive data (passwords, tokens) inappropriately
- Skip input validation

## Code Generation Guidelines

### Models (`src/models/`)

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    # ... other fields
```

**Rules:**
- Use `Optional[int] = Field(default=None, primary_key=True)` for auto-incrementing IDs
- Add `unique=True` and `index=True` for frequently queried fields
- Use `sa_column_kwargs={"default": datetime.utcnow}` for timestamps

### Schemas (`src/schemas/`)

```python
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
```

**Rules:**
- Create separate schemas for Create, Read, Update operations
- Use `Optional` for fields that are not required in all contexts
- Never include sensitive data like passwords in response schemas

### Services (`src/services/`)

- Implement business logic in service classes
- Use dependency injection for database sessions
- Handle errors and return appropriate exceptions
- Follow single responsibility principle

### API Endpoints (`src/api/`)

- Use FastAPI's path operations with proper type hints
- Include comprehensive docstrings
- Add authentication dependencies where needed
- Return Pydantic models, not raw database models

## Testing Standards

### Test Structure

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    # Test implementation
    pass
```

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Target**: 90%+ for business logic in services
- **Run**: `uv run pytest --cov=src --cov-report=term-missing`

## Error Handling

### HTTP Exceptions

```python
from fastapi import HTTPException

def get_user(user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
```

### Custom Exceptions

- Define domain-specific exceptions in `src/utils/exceptions.py`
- Use appropriate HTTP status codes
- Provide meaningful error messages

## Security Guidelines

1. **Authentication**: All protected endpoints require JWT tokens
2. **Authorization**: Validate user permissions for each operation
3. **Input Validation**: Use Pydantic models for all request data
4. **SQL Injection**: Use SQLModel's parameterized queries
5. **Password Security**: Hash passwords with bcrypt, never store plain text

## File Locations

### Backend Source Code
- Models: `src/models/`
- Schemas: `src/schemas/`
- Services: `src/services/`
- API: `src/api/v1/`
- Auth: `src/auth/`
- Database: `src/database/`
- Utils: `src/utils/`
- Config: `src/config/`
- Middleware: `src/middleware/`

### Backend Tests
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Contract tests: `tests/contract/`

## Running the Application

### Development

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the application
uvicorn src.main:app --reload --port 8000

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing
```

## Phase-Specific Constraints

### Phase II (Current)

**What's Allowed:**
- Database persistence with PostgreSQL
- JWT-based authentication
- REST API endpoints
- Multi-user support with data isolation

**What's Forbidden:**
- Hardcoded credentials or secrets
- Direct SQL queries (use SQLModel ORM)
- In-memory storage (use database)
- Cross-user data access

## Default Policies

- Use async/await for database operations
- Follow FastAPI best practices for dependency injection
- Implement proper error handling with HTTPException
- Use environment variables for configuration
- Maintain type safety throughout the codebase