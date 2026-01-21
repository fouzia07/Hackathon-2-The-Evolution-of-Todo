#!/usr/bin/env python
"""
Debug script to test user registration directly.
"""

import sys
from pathlib import Path
import os

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set environment to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./todo_app.db'

from sqlmodel import Session
from src.database.session import engine
from src.models.user import UserCreate
from src.services.user_service import UserService

def test_registration():
    """Test user registration directly."""
    print("Testing user registration...")

    # Create a user create object
    user_data = UserCreate(
        email="test2@example.com",
        password="shortpass123",  # Shorter password to comply with bcrypt limit
        first_name="Test",
        last_name="User"
    )

    # Create a database session
    with Session(engine) as session:
        try:
            print("Attempting to create user...")
            user = UserService.create_user(session, user_data)
            print(f"User created successfully: {user.email}")
            print(f"User ID: {user.id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_registration()