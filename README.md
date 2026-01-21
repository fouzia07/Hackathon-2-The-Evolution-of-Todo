# Todo Application - Evolution Project

A progressive todo application demonstrating the evolution from CLI to full-stack web application, following Spec-Driven Development principles.

## Project Status

| Phase | Description | Status | Completion |
|-------|-------------|--------|------------|
| **Phase I** | CLI Console App | ✅ Complete | 100% |
| **Phase II** | Full-Stack Web App | ✅ Complete | 100% |
| Phase III | AI Chatbot | 🔄 Pending | 0% |
| Phase IV | Local Kubernetes | 🔄 Pending | 0% |
| Phase V | Cloud Deployment | 🔄 Pending | 0% |

## Phase II - Full-Stack Web Application ✅

**Status**: **COMPLETED** (January 15, 2026)

A modern, secure, multi-user web application with authentication and persistent storage.

### Technology Stack

**Frontend:**
- Next.js 16.1.2 (App Router)
- TypeScript 5+
- TailwindCSS 4
- Axios for API calls

**Backend:**
- FastAPI 0.104.1
- SQLModel ORM
- PostgreSQL (Neon Serverless)
- JWT Authentication

### Features Implemented

✅ **All 5 Basic Level Features:**
1. Create tasks with title and description
2. View all tasks with filtering (All/Active/Completed)
3. Update task details and completion status
4. Delete tasks with confirmation
5. Mark tasks as complete/incomplete

✅ **Authentication & Security:**
- User registration with email/password
- Secure login with JWT tokens
- Password hashing with bcrypt
- User isolation (users only see their own tasks)
- Token-based API authentication

✅ **User Experience:**
- Responsive design (mobile, tablet, desktop)
- Real-time task statistics
- Loading states and error handling
- Form validation
- Clean, modern interface

## Quick Start

### Prerequisites

- **Python**: 3.11+ (for backend)
- **Node.js**: 18+ (for frontend)
- **PostgreSQL**: Neon account (or local PostgreSQL)

### 1. Clone Repository

```bash
git clone <repository-url>
cd "Hackathon_II_The evalution of todo"
```

### 2. Start Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL

# Run database migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload --port 8000
```

Backend runs on: **http://localhost:8000**
API docs: **http://localhost:8000/docs**

### 3. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:3000**

### 4. Test the Application

**Manual Testing:**
1. Open http://localhost:3000
2. Click "Create Account"
3. Register with email and password
4. Create, edit, and manage tasks
5. Test filtering and completion toggle
6. Sign out and sign in again

**Automated Integration Testing:**
```bash
# Make sure both backend and frontend are running
chmod +x test_phase2_integration.sh
./test_phase2_integration.sh
```

## Project Structure

```
Hackathon_II_The evalution of todo/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/v1/            # REST API endpoints
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   ├── auth/              # Authentication
│   │   └── main.py            # Application entry
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   └── CLAUDE.md              # Backend documentation
│
├── frontend/                  # Next.js frontend
│   ├── app/
│   │   ├── auth/              # Authentication pages
│   │   ├── tasks/             # Task management
│   │   └── page.tsx           # Landing page
│   ├── components/tasks/      # Task components
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   └── auth.ts            # Auth configuration
│   ├── package.json           # Node dependencies
│   ├── CLAUDE.md              # Frontend documentation
│   └── README.md              # Frontend guide
│
├── src/                       # Phase I CLI code
├── tests/                     # Phase I tests
├── specs/                     # Specifications
│   ├── 001-cli-todo-app/      # Phase I specs
│   └── 002-fullstack-web-todo/ # Phase II specs
│
├── test_phase2_integration.sh # Integration tests
├── PHASE2_SUMMARY.md          # Phase II completion summary
└── README.md                  # This file
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login (returns JWT)
- `POST /api/v1/auth/logout` - User logout

### Tasks (Requires Authentication)
- `GET /api/v1/tasks` - Get all user tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

All task endpoints require `Authorization: Bearer <token>` header.

## Phase I - CLI Console App ✅

The original CLI application is still available in the `src/` directory.

### Running Phase I

```bash
# With UV (recommended)
uv run python src/main.py

# Or with activated venv
python src/main.py
```

See the original README sections below for Phase I details.

## Development Approach

This project follows **Spec-Driven Development (SDD)** principles:

1. **Spec-First**: All features start with specifications
2. **AI-Native**: Code generated by Claude Code
3. **No Manual Coding**: Specifications refined until correct output
4. **Reproducible**: All decisions and iterations documented
5. **Constitutional**: Follows project constitution principles

## Documentation

- **Phase II Summary**: `PHASE2_SUMMARY.md`
- **Backend Guide**: `backend/CLAUDE.md`
- **Frontend Guide**: `frontend/CLAUDE.md` and `frontend/README.md`
- **Specifications**: `specs/002-fullstack-web-todo/`
- **Hackathon Details**: `Hackathon II - Todo Spec-Driven Development.md`

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=src --cov-report=term-missing
```

### Integration Tests
```bash
./test_phase2_integration.sh
```

### Manual Testing Checklist
- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Tasks can be created
- [ ] Tasks can be viewed (filtered by user)
- [ ] Tasks can be updated
- [ ] Tasks can be deleted
- [ ] Task completion toggle works
- [ ] User isolation works (users can't see others' tasks)
- [ ] Authentication is required for all task operations
- [ ] Frontend UI is responsive

## Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
vercel deploy
```

### Backend (Railway/Render/Fly.io)
```bash
cd backend
# Follow platform-specific instructions
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key
```

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
cd backend
pip install -r requirements.txt
```

**Database connection errors:**
- Verify DATABASE_URL in `.env`
- Check Neon database is accessible
- Run migrations: `alembic upgrade head`

### Frontend Issues

**"Cannot find module" errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API calls failing:**
- Ensure backend is running on http://localhost:8000
- Check CORS configuration in backend
- Verify token is stored in localStorage

## Contributing

This project follows strict Spec-Driven Development:
1. All changes must start with specification updates
2. Use Claude Code for implementation
3. No manual coding allowed
4. Follow the project constitution

## License

Part of the Hackathon II - Evolution of Todo project.

---

## Phase I Details (Original CLI App)

### Features

- ✅ **Add Task**: Create tasks with title and description
- ✅ **View Tasks**: Display all tasks in a formatted table
- ✅ **Update Task**: Edit task title and/or description
- ✅ **Delete Task**: Remove tasks by ID with confirmation
- ✅ **Mark Complete/Incomplete**: Toggle task completion status

### Installation (Phase I)

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install development dependencies (optional)
uv pip install pytest pytest-cov black mypy
```

### Usage (Phase I)

```bash
uv run python src/main.py
```

### Testing (Phase I)

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_task.py -v
```

---

**Last Updated**: January 15, 2026
**Current Phase**: II (Complete)
**Next Phase**: III (AI Chatbot)
