"""
Rate limiting middleware for the Full-Stack Web Todo Application.

This module provides rate limiting functionality for API endpoints.
"""
from fastapi import Request, HTTPException, status
from typing import Dict, Optional
import time
from collections import defaultdict


class RateLimiter:
    """
    Simple in-memory rate limiter.

    Note: In a production environment, you would use a distributed store like Redis
    for rate limiting across multiple instances.
    """
    def __init__(self, max_requests: int = 10, window_size: int = 60):
        """
        Initialize the rate limiter.

        Args:
            max_requests (int): Maximum number of requests allowed in the window
            window_size (int): Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.

        Args:
            identifier (str): Unique identifier for the requester (IP, user ID, etc.)

        Returns:
            bool: True if request is allowed, False otherwise
        """
        current_time = time.time()

        # Remove old requests outside the time window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < self.window_size
        ]

        # Check if we've exceeded the limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False

        # Add the current request
        self.requests[identifier].append(current_time)
        return True


# Create a global rate limiter instance for auth endpoints
auth_rate_limiter = RateLimiter(max_requests=5, window_size=60)  # 5 requests per minute


def check_auth_endpoint_rate_limit(request: Request) -> None:
    """
    Check if the request to an auth endpoint is within rate limits.

    Args:
        request (Request): The incoming request

    Raises:
        HTTPException: If rate limit is exceeded
    """
    # Use IP address as identifier (in production, you might want to use other identifiers)
    client_ip = request.client.host if request.client else "unknown"

    if not auth_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for authentication endpoints. Please try again later."
        )