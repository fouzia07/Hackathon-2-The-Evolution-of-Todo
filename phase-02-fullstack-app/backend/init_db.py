"""
Database initialization script for the Full-Stack Web Todo Application.

This script creates all database tables defined in the models.
Run this script before starting the application for the first time.
"""
from sqlmodel import SQLModel
from src.database.session import engine
from src.models.user import User
from src.models.task import Task

def init_db():
    """
    Initialize the database by creating all tables.
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
