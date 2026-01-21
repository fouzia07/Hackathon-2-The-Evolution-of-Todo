# Phase II - Full-Stack Web Todo Application

This folder contains the complete Phase II implementation - a modern, secure, multi-user web application with authentication and persistent storage.

## Contents

### **backend/** - FastAPI Backend
- **Technology**: FastAPI, SQLModel, PostgreSQL (Neon), JWT Authentication
- **Features**:
  - RESTful API with 8 endpoints
  - JWT token-based authentication
  - Password hashing with bcrypt
  - User isolation (tasks filtered by user_id)
  - Database migrations with Alembic
  - Comprehensive error handling

- **Structure**:
  ```
  backend/
  ├── src/              # Source code
  │   ├── api/v1/       # REST API endpoints
  │   ├── auth/         # JWT + bcrypt
  │   ├── models/       # Database models
  │   ├── services/     # Business logic
  │   └── main.py       # FastAPI app
  ├── tests/            # Tests
  │   ├── integration/  # Integration tests
  │   └── unit/         # Unit tests
  ├── scripts/          # Utility scripts
  └── .venv/            # Virtual environment
  ```

### **frontend/** - Next.js Frontend
- **Technology**: Next.js 16, TypeScript, TailwindCSS, Axios
- **Features**:
  - User authentication (signup/signin)
  - Task CRUD operations
  - Task filtering (All/Active/Completed)
  - Real-time statistics dashboard
  - Responsive design
  - JWT token management

- **Structure**:
  ```
  frontend/
  ├── app/              # Next.js App Router
  │   ├── auth/         # Authentication pages
  │   ├── tasks/        # Main application
  │   ├── layout.tsx    # Root layout
  │   └── page.tsx      # Landing page
  ├── components/tasks/ # React components
  ├── lib/              # API client
  └── node_modules/     # Dependencies
  ```

## Running Phase II

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon account or local)

### **Start Backend**
```bash
cd phase2-fullstack/backend
uvicorn src.main:app --reload --port 8001
```

**Backend URLs:**
- API: http://localhost:8001
- Docs: http://localhost:8001/docs
- Health: http://localhost:8001/health

### **Start Frontend**
```bash
cd phase2-fullstack/frontend
npm run dev
```

**Frontend URL:**
- App: http://localhost:3000

### **Environment Setup**

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key
```

## Features Implemented

### ✅ All 5 Basic Level Features
1. **Create Task** - Add tasks with title and description
2. **View Tasks** - Display all tasks with filtering
3. **Update Task** - Edit task details and completion status
4. **Delete Task** - Remove tasks with confirmation
5. **Mark Complete** - Toggle task completion status

### ✅ Authentication & Security
- User registration with email/password
- Secure login with JWT tokens
- Password hashing with bcrypt
- User isolation (users only see their own tasks)
- Token-based API authentication
- Automatic token refresh handling

### ✅ User Experience
- Responsive design (mobile, tablet, desktop)
- Loading states for async operations
- Error messages with user feedback
- Form validation (client & server)
- Task statistics dashboard
- Smooth transitions and hover effects

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

## Testing

### Backend Tests
```bash
cd phase2-fullstack/backend
pytest tests/
pytest --cov=src --cov-report=term-missing
```

### Manual Testing
1. Open http://localhost:3000
2. Click "Create Account"
3. Register with email and password
4. Create, edit, complete, delete tasks
5. Test filtering (All/Active/Completed)
6. Sign out and sign in again

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend Framework | Next.js | 16.1.2 |
| Frontend Language | TypeScript | 5+ |
| Frontend Styling | TailwindCSS | 4 |
| Backend Framework | FastAPI | 0.104.1 |
| Backend Language | Python | 3.11+ |
| ORM | SQLModel | 0.0.16 |
| Database | PostgreSQL | Neon |
| Authentication | JWT | python-jose |
| HTTP Client | Axios | Latest |

## Specifications

See `../specs/002-fullstack-web-todo/` for detailed specifications, plan, and tasks.

## Evolution

This full-stack web application evolved from Phase I (CLI app). It demonstrates the project's progression from a simple console application to a complete, production-ready web system with authentication, persistent storage, and modern UI.

---

**Phase**: II (Full-Stack Web)
**Status**: 95-98% Complete
**Previous Phase**: Phase I (CLI) - See `../phase1-cli/`
**Next Phase**: Phase III (AI Chatbot)
