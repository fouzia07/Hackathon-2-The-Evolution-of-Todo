"""
Database module for the Full-Stack Web Todo Application.

This module provides database connection and session management using SQLModel.
"""
from sqlmodel import create_engine
from .session import SessionLocal, engine

__all__ = ["SessionLocal", "engine"]