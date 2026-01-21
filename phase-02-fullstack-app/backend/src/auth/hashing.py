"""
Password hashing utilities for the Full-Stack Web Todo Application.

This module provides functions for hashing and verifying passwords.
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    # Truncate password to 72 bytes to comply with bcrypt limit
    password_bytes = password.encode('utf-8')[:72]

    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Hashed password to compare against

    Returns:
        bool: True if passwords match, False otherwise
    """
    # Truncate password to 72 bytes to comply with bcrypt limit
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')

    # Verify the password
    return bcrypt.checkpw(password_bytes, hashed_bytes)