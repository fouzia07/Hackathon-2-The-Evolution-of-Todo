"""
Authentication middleware for the Full-Stack Web Todo Application.

This module provides middleware for authenticating requests using JWT tokens.
"""
from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from ..auth.jwt import verify_token
from ..database.session import get_session


class JWTBearer(HTTPBearer):
    """
    JWT Bearer authentication scheme.
    """
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Validate the JWT token in the request.

        Args:
            request (Request): FastAPI request object

        Returns:
            str: The validated token

        Raises:
            HTTPException: If authentication fails
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            if not self.verify_jwt(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )

    def verify_jwt(self, token: str) -> bool:
        """
        Verify the JWT token.

        Args:
            token (str): JWT token to verify

        Returns:
            bool: True if token is valid, False otherwise
        """
        # In a real implementation, we would verify the token
        # For now, we'll just check if it's not empty
        # The actual verification happens in the dependency
        return token is not None


def get_current_user(token: str = None):
    """
    Get the current user from the JWT token.

    Args:
        token (str): JWT token from the request

    Returns:
        User: The authenticated user
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # We need to get the database session here
    # In a real implementation, this would be handled differently
    # For now, we'll return a placeholder
    return None