"""
Unit tests for the UserService in the Full-Stack Web Todo Application.
"""
import pytest
from unittest.mock import MagicMock
from sqlmodel import Session, select
from src.models.user import User, UserCreate
from src.services.user_service import UserService
from src.utils.exceptions import UserAlreadyExistsException


class TestUserService:
    """Test suite for UserService functionality."""

    @pytest.fixture
    def mock_session(self):
        """Mock database session fixture."""
        return MagicMock(spec=Session)

    @pytest.fixture
    def user_create_data(self):
        """Sample user creation data."""
        return UserCreate(
            email="test@example.com",
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )

    def test_create_user_success(self, mock_session, user_create_data):
        """Test successful user creation."""
        # Arrange
        mock_session.exec.return_value.first.return_value = None  # No existing user

        # Act
        result = UserService.create_user(mock_session, user_create_data)

        # Assert
        assert isinstance(result, User)
        assert result.email == user_create_data.email
        assert result.first_name == user_create_data.first_name
        assert result.last_name == user_create_data.last_name
        assert result.hashed_password is not None  # Password should be hashed
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_create_user_already_exists(self, mock_session, user_create_data):
        """Test user creation fails when user already exists."""
        # Arrange
        existing_user = User(
            id=1,
            email=user_create_data.email,
            hashed_password="somehash"
        )
        mock_session.exec.return_value.first.return_value = existing_user

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException):
            UserService.create_user(mock_session, user_create_data)

    def test_get_user_by_email_found(self, mock_session):
        """Test getting a user by email when user exists."""
        # Arrange
        expected_user = User(
            id=1,
            email="test@example.com",
            hashed_password="somehash"
        )
        mock_session.exec.return_value.first.return_value = expected_user

        # Act
        result = UserService.get_user_by_email(mock_session, "test@example.com")

        # Assert
        assert result == expected_user
        mock_session.exec.assert_called_once()

    def test_get_user_by_email_not_found(self, mock_session):
        """Test getting a user by email when user doesn't exist."""
        # Arrange
        mock_session.exec.return_value.first.return_value = None

        # Act
        result = UserService.get_user_by_email(mock_session, "nonexistent@example.com")

        # Assert
        assert result is None

    def test_get_user_by_id_found(self, mock_session):
        """Test getting a user by ID when user exists."""
        # Arrange
        expected_user = User(
            id=1,
            email="test@example.com",
            hashed_password="somehash"
        )
        mock_session.get.return_value = expected_user

        # Act
        result = UserService.get_user_by_id(mock_session, 1)

        # Assert
        assert result == expected_user
        mock_session.get.assert_called_once_with(User, 1)

    def test_get_user_by_id_not_found(self, mock_session):
        """Test getting a user by ID when user doesn't exist."""
        # Arrange
        mock_session.get.return_value = None

        # Act
        result = UserService.get_user_by_id(mock_session, 999)

        # Assert
        assert result is None

    def test_authenticate_user_success(self, mock_session):
        """Test successful user authentication."""
        # Arrange
        from src.auth.hashing import hash_password
        hashed_pwd = hash_password("validpassword")

        user = User(
            id=1,
            email="test@example.com",
            hashed_password=hashed_pwd,
            is_active=True
        )

        # Mock the get_user_by_email method to return our user
        UserService.get_user_by_email = MagicMock(return_value=user)

        # Act
        result = UserService.authenticate_user(mock_session, "test@example.com", "validpassword")

        # Assert
        assert result == user

    def test_authenticate_user_wrong_password(self, mock_session):
        """Test authentication fails with wrong password."""
        # Arrange
        from src.auth.hashing import hash_password
        hashed_pwd = hash_password("correctpassword")

        user = User(
            id=1,
            email="test@example.com",
            hashed_password=hashed_pwd,
            is_active=True
        )

        # Mock the get_user_by_email method to return our user
        UserService.get_user_by_email = MagicMock(return_value=user)

        # Act
        result = UserService.authenticate_user(mock_session, "test@example.com", "wrongpassword")

        # Assert
        assert result is None

    def test_authenticate_user_inactive(self, mock_session):
        """Test authentication fails for inactive user."""
        # Arrange
        from src.auth.hashing import hash_password
        hashed_pwd = hash_password("validpassword")

        user = User(
            id=1,
            email="test@example.com",
            hashed_password=hashed_pwd,
            is_active=False  # User is inactive
        )

        # Mock the get_user_by_email method to return our user
        UserService.get_user_by_email = MagicMock(return_value=user)

        # Act
        result = UserService.authenticate_user(mock_session, "test@example.com", "validpassword")

        # Assert
        assert result is None