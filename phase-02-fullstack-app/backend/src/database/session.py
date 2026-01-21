"""
Database session management for the Full-Stack Web Todo Application.

This module provides database session creation and management using SQLModel.
"""
from typing import Generator
from sqlmodel import create_engine, Session
from ..config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True for debugging SQL queries
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections after 5 minutes
)

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for use with dependency injection.

    Yields:
        Session: A SQLModel database session
    """
    with Session(engine) as session:
        yield session

# For direct use when dependency injection is not available
SessionLocal = Session