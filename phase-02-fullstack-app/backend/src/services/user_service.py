"""
User service for the Full-Stack Web Todo Application.

This module provides business logic for user-related operations.
"""
from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate
from ..auth.hashing import hash_password
from ..utils.exceptions import UserAlreadyExistsException, UserNotFoundException


class UserService:
    """
    Service class for user-related business logic.
    """

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """
        Create a new user.

        Args:
            db (Session): Database session
            user_create (UserCreate): User creation data

        Returns:
            User: The created user

        Raises:
            UserAlreadyExistsException: If a user with the email already exists
        """
        # Check if user with this email already exists
        existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise UserAlreadyExistsException(user_create.email)

        # Hash the password
        hashed_password = hash_password(user_create.password)

        # Create the user object
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name
        )

        # Add to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get a user by email.

        Args:
            db (Session): Database session
            email (str): User's email

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            db (Session): Database session
            user_id (int): User's ID

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        user = db.get(User, user_id)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            db (Session): Database session
            email (str): User's email
            password (str): User's password

        Returns:
            Optional[User]: The authenticated user if credentials are valid, None otherwise
        """
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None

        if not user.is_active:
            return None

        if not user.hashed_password:
            return None

        # Verify the password using the hashing utility
        from ..auth.hashing import verify_password
        if verify_password(password, user.hashed_password):
            return user

        return None