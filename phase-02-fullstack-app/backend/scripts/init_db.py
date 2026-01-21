#!/usr/bin/env python
"""
Script to initialize the database tables for the Full-Stack Web Todo Application.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlmodel import SQLModel
from src.database.session import engine
from src.models.user import User
from src.models.task import Task

def init_db():
    """Initialize the database by creating all tables."""
    print("Initializing database...")

    # Create all tables
    SQLModel.metadata.create_all(engine)

    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()