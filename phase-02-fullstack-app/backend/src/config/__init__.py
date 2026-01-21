"""
Configuration module for the Full-Stack Web Todo Application.

This module provides application settings using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/todo_db"
    db_echo: bool = False  # Set to True to log SQL queries

    # JWT settings
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application settings
    app_name: str = "Todo API"
    debug: bool = False
    version: str = "1.0.0"

    # CORS settings
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


# Create a single instance of settings
settings = Settings()