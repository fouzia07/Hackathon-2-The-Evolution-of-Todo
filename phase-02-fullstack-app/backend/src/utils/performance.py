"""
Performance utilities for the Full-Stack Web Todo Application.

This module provides performance optimization utilities.
"""
import time
import functools
from typing import Callable, Any
from .logger import log_debug


def measure_execution_time(func: Callable) -> Callable:
    """
    Decorator to measure the execution time of a function.

    Args:
        func: The function to measure

    Returns:
        Callable: The wrapped function with timing
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        log_debug(
            f"Function {func.__name__} executed in {execution_time:.4f} seconds",
            extra={"function": func.__name__, "execution_time": execution_time}
        )

        return result

    return wrapper


def cache_result(ttl: int = 300):
    """
    Decorator to cache function results for a specified time-to-live (TTL).

    Args:
        ttl (int): Time-to-live in seconds (default: 300 seconds = 5 minutes)

    Returns:
        Callable: The decorator
    """
    def decorator(func: Callable) -> Callable:
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key from arguments
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()

            # Check if result is in cache and not expired
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl:
                    log_debug(f"Cache hit for {func.__name__}", extra={"function": func.__name__})
                    return result
                else:
                    # Remove expired entry
                    del cache[key]

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            log_debug(f"Cached result for {func.__name__}", extra={"function": func.__name__})

            return result

        return wrapper

    return decorator


class QueryOptimizer:
    """
    Utility class for optimizing database queries.
    """

    @staticmethod
    def optimize_pagination_query(query, page: int, page_size: int):
        """
        Optimize a query with pagination to avoid performance issues.

        Args:
            query: The SQLModel query object
            page (int): Page number (starting from 1)
            page_size (int): Number of items per page

        Returns:
            The paginated query
        """
        offset = (page - 1) * page_size
        paginated_query = query.offset(offset).limit(page_size)

        log_debug(
            "Query optimized with pagination",
            extra={
                "page": page,
                "page_size": page_size,
                "offset": offset
            }
        )

        return paginated_query


def bulk_insert(session, model_class, data_list, chunk_size: int = 1000):
    """
    Perform bulk insert of data with optimization.

    Args:
        session: The database session
        model_class: The SQLModel class to insert
        data_list: List of data dictionaries to insert
        chunk_size (int): Number of records to insert per chunk (default: 1000)

    Returns:
        int: Number of records inserted
    """
    total_inserted = 0

    for i in range(0, len(data_list), chunk_size):
        chunk = data_list[i:i + chunk_size]
        objects = [model_class(**item) for item in chunk]

        session.add_all(objects)
        session.flush()  # Flush to get IDs without committing
        total_inserted += len(objects)

        log_debug(
            f"Bulk insert chunk completed",
            extra={
                "chunk_start": i,
                "chunk_size": len(chunk),
                "total_inserted": total_inserted
            }
        )

    session.commit()
    return total_inserted