# Data Model: Full-Stack Web Todo Application - Phase II

**Feature**: Full-Stack Web Todo Application - Phase II
**Date**: 2026-01-07
**Related Plan**: [plan.md](plan.md)

## Entity Definitions

### User
**Description**: Represents an authenticated user of the system

**Fields**:
- `id`: Integer (Primary Key, Auto-incrementing)
- `email`: String (Unique, Indexed, Max 255 chars, Required)
- `hashed_password`: String (Max 255 chars, Required)
- `first_name`: String (Optional, Max 100 chars)
- `last_name`: String (Optional, Max 100 chars)
- `is_active`: Boolean (Default: True)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on change)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must be hashed before storage
- Email is required for registration

**Relationships**:
- One-to-Many with Task (user has many tasks)

### Task
**Description**: Represents a todo item owned by a single user

**Fields**:
- `id`: Integer (Primary Key, Auto-incrementing)
- `title`: String (Required, 1-200 chars)
- `description`: String (Optional, Max 1000 chars)
- `is_complete`: Boolean (Default: False)
- `user_id`: Integer (Foreign Key to User.id, Required)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on change)

**Validation Rules**:
- Title must be 1-200 characters
- Description must be 0-1000 characters if provided
- Task must belong to a valid user
- Only the owner can modify/delete the task

**Relationships**:
- Many-to-One with User (task belongs to one user)

### AuthenticationToken (Conceptual - handled by Better Auth)
**Description**: Represents JWT tokens for authentication (handled by Better Auth)

**Fields**:
- `user_id`: Integer (Foreign Key to User.id)
- `token_hash`: String (Hashed JWT token)
- `expires_at`: DateTime (Token expiration timestamp)
- `created_at`: DateTime (Auto-generated)

**Note**: Actual token handling will be managed by Better Auth, with this conceptual model representing the data relationship.

## Database Schema Relationships

```
User (1) -----> (Many) Task
```

**Relationship Details**:
- User.id → Task.user_id (Foreign Key)
- Cascade delete: When a user is deleted, all their tasks are also deleted
- Index on Task.user_id for efficient querying of user-specific tasks
- Index on User.email for efficient authentication lookups

## State Transitions

### Task State Transitions
- `is_complete` can transition from `False` to `True` (marked complete)
- `is_complete` can transition from `True` to `False` (marked incomplete)
- Both transitions require the authenticated user to be the task owner

## Data Integrity Constraints

1. **Referential Integrity**:
   - All Task.user_id values must correspond to existing User.id values
   - Deleting a User automatically deletes all associated Tasks

2. **Uniqueness Constraints**:
   - User.email must be unique across all users

3. **Validation Constraints**:
   - Task.title length between 1-200 characters
   - User.email format validation
   - Task.user_id cannot be null

## Query Patterns

### Common Queries
1. Get all tasks for a specific user (filtered by user_id)
2. Get a specific task for a specific user (filtered by user_id and task.id)
3. Create a new task for a specific user (validated ownership)
4. Update a specific task for a specific user (validated ownership)
5. Delete a specific task for a specific user (validated ownership)

### Security Considerations
- All queries must be filtered by the authenticated user's ID
- No cross-user access is allowed
- Authentication must be validated before any data access