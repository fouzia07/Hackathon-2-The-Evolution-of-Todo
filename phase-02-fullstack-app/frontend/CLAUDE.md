# Claude Code Instructions for Frontend

This file provides guidance for Claude Code when working on the frontend components of the Full-Stack Web Todo Application.

## Purpose

This document ensures Claude Code follows the project's architectural principles and development workflow when making changes to the Next.js frontend.

## Project Context

**Project**: Full-Stack Web Todo Application - Phase II
**Type**: Next.js 16+ frontend with TypeScript
**Architecture**: App Router with client-side state management
**Authentication**: JWT-based with custom implementation
**Target Platform**: Web browsers (responsive design)
**Phase**: II (Web with Authentication & Persistence)

## Architecture Overview

### Frontend Structure

```
frontend/
├── app/
│   ├── auth/
│   │   ├── signin/page.tsx      # Sign in page
│   │   └── signup/page.tsx      # Sign up page
│   ├── tasks/page.tsx           # Main tasks interface
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Landing page
│   └── globals.css              # Global styles
├── components/
│   └── tasks/
│       ├── CreateTaskForm.tsx   # Create task modal
│       ├── EditTaskForm.tsx     # Edit task modal
│       └── TaskCard.tsx         # Task display component
├── lib/
│   ├── api.ts                   # API client with JWT handling
│   ├── auth.ts                  # Better Auth configuration
│   └── auth-client.ts           # Better Auth client
└── public/                      # Static assets
```

### Technology Stack

- **Framework**: Next.js 16.1.2 (App Router)
- **Language**: TypeScript 5+
- **Styling**: TailwindCSS 4
- **HTTP Client**: Axios
- **State Management**: React hooks (useState, useEffect)
- **Authentication**: JWT tokens stored in localStorage

## Development Workflow

### For New Features

1. **Create Component**: Add new component in appropriate directory
2. **Implement Logic**: Use React hooks for state management
3. **Style with Tailwind**: Use utility classes for styling
4. **Connect to API**: Use functions from `lib/api.ts`
5. **Handle Errors**: Display user-friendly error messages
6. **Test Manually**: Verify functionality in browser

### For API Integration

**ALWAYS:**
- Use the API client from `lib/api.ts`
- Handle loading states with useState
- Display error messages to users
- Check for authentication before protected operations
- Use TypeScript interfaces for type safety

**NEVER:**
- Make direct fetch/axios calls (use API client)
- Store sensitive data in component state
- Skip error handling
- Bypass authentication checks
- Use inline styles (use Tailwind classes)

## Code Generation Guidelines

### Page Components (`app/*/page.tsx`)

```typescript
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function PageName() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/auth/signin");
      return;
    }

    // Load data
    loadData();
  }, [router]);

  // Component logic here
}
```

**Rules:**
- Use "use client" directive for interactive components
- Check authentication in useEffect
- Handle loading and error states
- Use useRouter for navigation
- Clean up effects when needed

### UI Components (`components/*/`)

```typescript
"use client";

interface ComponentProps {
  // Define props with TypeScript
}

export default function ComponentName({ prop1, prop2 }: ComponentProps) {
  // Component logic

  return (
    <div className="tailwind-classes">
      {/* JSX here */}
    </div>
  );
}
```

**Rules:**
- Define TypeScript interfaces for props
- Use descriptive prop names
- Keep components focused (single responsibility)
- Use Tailwind utility classes
- Export as default

### API Client Usage (`lib/api.ts`)

```typescript
import { taskAPI, authAPI } from "@/lib/api";

// Authentication
const loginResult = await authAPI.login(email, password);

// Task operations
const tasks = await taskAPI.getTasks();
const task = await taskAPI.createTask({ title, description });
const updated = await taskAPI.updateTask(id, { title: "New title" });
await taskAPI.deleteTask(id);
```

**Rules:**
- Always use try-catch for API calls
- Handle 401 errors (redirect to login)
- Display user-friendly error messages
- Show loading states during API calls

## Styling Guidelines

### TailwindCSS Usage

**Layout:**
- `flex`, `grid` for layouts
- `space-x-*`, `space-y-*` for spacing
- `max-w-*` for max widths
- `mx-auto` for centering

**Colors:**
- Primary: `bg-blue-600`, `text-blue-600`
- Success: `bg-green-600`, `text-green-600`
- Error: `bg-red-600`, `text-red-600`
- Gray scale: `bg-gray-50` to `bg-gray-900`

**Interactive:**
- `hover:bg-*` for hover states
- `focus:ring-*` for focus states
- `disabled:opacity-50` for disabled states
- `transition-colors` for smooth transitions

**Responsive:**
- `sm:*` for small screens (640px+)
- `md:*` for medium screens (768px+)
- `lg:*` for large screens (1024px+)

## Authentication Flow

1. User visits protected page
2. Check for token in localStorage
3. If no token, redirect to `/auth/signin`
4. User logs in, token stored in localStorage
5. API client automatically attaches token to requests
6. On 401 error, clear token and redirect to login

## Error Handling Patterns

### API Errors

```typescript
try {
  const result = await taskAPI.createTask(data);
  // Success handling
} catch (err: any) {
  if (err.response?.status === 401) {
    // Redirect to login (handled by interceptor)
  } else {
    setError(err.response?.data?.detail || "Operation failed");
  }
}
```

### Form Validation

```typescript
const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();

  // Client-side validation
  if (!title.trim()) {
    setError("Title is required");
    return;
  }

  if (title.length > 200) {
    setError("Title must be 200 characters or less");
    return;
  }

  // Submit form
};
```

## State Management

### Local State (useState)

```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");
```

### Effect Hook (useEffect)

```typescript
useEffect(() => {
  // Load data on mount
  loadData();

  // Cleanup function
  return () => {
    // Cleanup if needed
  };
}, [dependencies]);
```

## File Locations

### Pages
- Landing: `app/page.tsx`
- Sign In: `app/auth/signin/page.tsx`
- Sign Up: `app/auth/signup/page.tsx`
- Tasks: `app/tasks/page.tsx`

### Components
- Task Card: `components/tasks/TaskCard.tsx`
- Create Form: `components/tasks/CreateTaskForm.tsx`
- Edit Form: `components/tasks/EditTaskForm.tsx`

### Services
- API Client: `lib/api.ts`
- Auth Config: `lib/auth.ts`
- Auth Client: `lib/auth-client.ts`

## Running the Application

### Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Application runs on http://localhost:3000
```

### Building

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Phase-Specific Constraints

### Phase II (Current)

**What's Allowed:**
- Client-side routing with Next.js App Router
- JWT authentication with localStorage
- API calls to FastAPI backend
- Responsive UI with TailwindCSS
- Form validation and error handling

**What's Forbidden:**
- Server-side authentication (use client-side JWT)
- Direct database access (use API)
- Hardcoded API URLs (use environment variables)
- Inline styles (use Tailwind)
- Class components (use functional components with hooks)

## Best Practices

1. **Type Safety**: Use TypeScript interfaces for all data structures
2. **Error Handling**: Always handle errors gracefully with user feedback
3. **Loading States**: Show loading indicators during async operations
4. **Accessibility**: Use semantic HTML and ARIA labels
5. **Responsive Design**: Test on mobile, tablet, and desktop
6. **Code Organization**: Keep components small and focused
7. **Reusability**: Extract common patterns into reusable components
8. **Performance**: Use React.memo for expensive components (when needed)

## Common Tasks

### Adding a New Page

1. Create `app/new-page/page.tsx`
2. Add "use client" if interactive
3. Implement component with proper types
4. Add navigation links from other pages
5. Test routing and functionality

### Adding a New Component

1. Create file in `components/` directory
2. Define TypeScript interface for props
3. Implement component with Tailwind styling
4. Export as default
5. Import and use in pages

### Connecting to New API Endpoint

1. Add interface for data type in `lib/api.ts`
2. Add function to appropriate API object (authAPI or taskAPI)
3. Use function in component with try-catch
4. Handle loading and error states
5. Update UI based on response

## Troubleshooting

### "Module not found" errors
- Check import paths use `@/` alias
- Verify file exists at specified path
- Restart dev server: `npm run dev`

### Styling not applied
- Check Tailwind classes are correct
- Verify `globals.css` imports Tailwind
- Clear `.next` cache: `rm -rf .next`

### API calls failing
- Verify backend is running on http://localhost:8000
- Check CORS configuration on backend
- Verify token is in localStorage
- Check network tab in browser DevTools

## Constitutional Compliance

When working on this project, ensure:

1. **All code is AI-generated**: No manual coding allowed
2. **Spec-first**: Changes start with spec updates
3. **Type safety**: Use TypeScript throughout
4. **Error handling**: Handle all error cases
5. **User experience**: Provide feedback for all actions
6. **Security**: Never expose sensitive data
7. **Accessibility**: Follow WCAG guidelines
8. **Performance**: Optimize for fast load times

## Questions?

For questions about:
- **Project principles**: See root `CLAUDE.md` and `.specify/memory/constitution.md`
- **API contracts**: See `specs/002-fullstack-web-todo/contracts/`
- **Backend integration**: See `backend/CLAUDE.md`
- **Component patterns**: Read existing components in `components/`
- **Styling patterns**: See `app/globals.css` and existing pages

---

**Last Updated**: 2026-01-15
**Phase**: II (Full-Stack Web)
**Version**: 0.1.0
