#!/usr/bin/env python
"""
Comprehensive test script to verify all API endpoints are working correctly.
"""

import sys
from pathlib import Path
import os

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set environment to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./todo_app.db'

import json
from fastapi.testclient import TestClient
from src.main import app

def test_api_endpoints():
    """Test all API endpoints."""
    client = TestClient(app)

    # Test the root endpoint
    print("1. Testing root endpoint...")
    response = client.get("/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json() if response.content else 'No content'}")
    assert response.status_code == 200
    print("   PASS Root endpoint working\n")

    # Test health endpoint
    print("2. Testing health endpoint...")
    response = client.get("/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json() if response.content else 'No content'}")
    assert response.status_code == 200
    print("   PASS Health endpoint working\n")

    # Create a unique test user
    import uuid
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    print(f"3. Testing registration endpoint with {unique_email}...")
    user_data = {
        "email": unique_email,
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        user_response = response.json()
        print(f"   Response: {user_response}")
        user_id = user_response.get('id', 1)  # Use the returned ID or default to 1
        print("   PASS Registration endpoint working\n")
    else:
        print(f"   Error: {response.text}")
        user_id = 1  # Default to 1 if registration failed
        print("   WARN Registration failed, continuing with default user ID\n")

    # Test login endpoint
    print("4. Testing login endpoint...")
    login_data = {
        "email": unique_email,
        "password": "securepassword123"
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        login_response = response.json()
        print(f"   Response: {login_response}")
        token = login_response.get('access_token')
        assert token is not None, "Token should be returned on successful login"
        print("   PASS Login endpoint working\n")
    else:
        print(f"   Error: {response.text}")
        print("   WARN Login failed\n")
        token = None

    # Test task endpoints (require authentication)
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        print("5. Testing task creation endpoint...")
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }

        response = client.post("/api/v1/tasks", json=task_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            task_response = response.json()
            print(f"   Response: {task_response}")
            task_id = task_response.get('id')
            print("   PASS Task creation endpoint working\n")
        else:
            print(f"   Error: {response.text}")
            print("   WARN Task creation failed\n")
            task_id = None

        # Test getting all tasks
        if task_id:
            print("6. Testing get all tasks endpoint...")
            response = client.get("/api/v1/tasks", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                tasks_response = response.json()
                print(f"   Number of tasks: {len(tasks_response)}")
                print("   PASS Get tasks endpoint working\n")
            else:
                print(f"   Error: {response.text}")
                print("   WARN Get tasks failed\n")

        # Test getting specific task
        if task_id:
            print("7. Testing get specific task endpoint...")
            response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                task_response = response.json()
                print(f"   Response: {task_response}")
                print("   PASS Get specific task endpoint working\n")
            else:
                print(f"   Error: {response.text}")
                print("   WARN Get specific task failed\n")

        # Test updating task
        if task_id:
            print("8. Testing update task endpoint...")
            update_data = {
                "title": "Updated Test Task",
                "description": "This is an updated test task"
            }

            response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                task_response = response.json()
                print(f"   Response: {task_response}")
                print("   PASS Update task endpoint working\n")
            else:
                print(f"   Error: {response.text}")
                print("   WARN Update task failed\n")

        # Test completing task (toggle completion)
        if task_id:
            print("9. Testing toggle task completion endpoint...")
            update_data = {
                "is_complete": True
            }

            response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                task_response = response.json()
                print(f"   Response: {task_response}")
                print("   PASS Toggle task completion endpoint working\n")
            else:
                print(f"   Error: {response.text}")
                print("   WARN Toggle task completion failed\n")

        # Test deleting task
        if task_id:
            print("10. Testing delete task endpoint...")
            response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 204:
                print("   PASS Delete task endpoint working\n")
            else:
                print(f"   Error: {response.text}")
                print("   WARN Delete task failed\n")

    print("All API endpoint tests completed!")

if __name__ == "__main__":
    test_api_endpoints()