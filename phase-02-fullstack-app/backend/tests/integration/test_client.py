#!/usr/bin/env python
"""
Test script using FastAPI TestClient to debug the registration issue.
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

def test_with_testclient():
    """Test using FastAPI TestClient."""
    client = TestClient(app)

    # Test the root endpoint first
    print("Testing root endpoint...")
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint response: {response.json() if response.content else 'No content'}")

    # Test registration
    print("\nTesting registration endpoint...")
    user_data = {
        "email": "test_client@example.com",
        "password": "shortpass123",
        "first_name": "Test",
        "last_name": "Client"
    }

    try:
        response = client.post("/api/v1/auth/register", json=user_data)
        print(f"Registration status: {response.status_code}")
        print(f"Registration response: {response.text}")

        if response.status_code != 200:
            print(f"Headers: {response.headers}")
            print(f"Raw response: {response.content}")
    except Exception as e:
        print(f"Error during registration test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_testclient()