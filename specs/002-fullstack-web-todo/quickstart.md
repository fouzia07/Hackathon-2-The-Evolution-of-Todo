# Quickstart Guide: Full-Stack Web Todo Application - Phase II

**Feature**: Full-Stack Web Todo Application - Phase II
**Date**: 2026-01-07
**Related Plan**: [plan.md](plan.md)

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- PostgreSQL-compatible database (Neon recommended)
- UV package manager (for Python dependencies)
- Git

## Environment Setup

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up Python Environment
```bash
# Install UV if not already installed
pip install uv

# Install backend dependencies
cd backend
uv pip install -r requirements.txt
```

### 3. Set Up Frontend Environment
```bash
# From repository root
cd frontend
npm install
```

## Configuration

### 1. Environment Variables
Create `.env` files in both backend and frontend directories:

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NEON_DATABASE_URL=your-neon-database-url
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 2. Database Setup
```bash
# From backend directory
cd backend
alembic upgrade head
```

## Running the Application

### 1. Start Backend Server
```bash
# From backend directory
cd backend
uv run python -m src.main
# or
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend Server
```bash
# From frontend directory
cd frontend
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

## Development Commands

### Backend
```bash
# Run tests
cd backend
uv run pytest

# Format code
uv run black .

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### Frontend
```bash
# Run tests
cd frontend
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

## Key Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user

### Tasks
- `GET /api/v1/tasks` - Get user's tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL server is running and DATABASE_URL is correct
2. **Port Conflicts**: Check that ports 8000 (backend) and 3000 (frontend) are available
3. **Dependency Issues**: Reinstall dependencies if import errors occur
4. **Authentication Failures**: Verify JWT secret and algorithm configuration

### Reset Database
```bash
# From backend directory
alembic downgrade base
alembic upgrade head
```