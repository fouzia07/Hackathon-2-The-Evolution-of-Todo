"""
Logging utilities for the Full-Stack Web Todo Application.

This module provides logging configuration and utilities.
"""
import logging
from typing import Any, Dict
import json
from datetime import datetime


def setup_logging():
    """
    Set up application logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def log_info(message: str, extra: Dict[str, Any] = None):
    """
    Log an info message.

    Args:
        message (str): The message to log
        extra (Dict[str, Any]): Additional context to include in the log
    """
    logger = logging.getLogger(__name__)
    if extra:
        logger.info(f"{message} - Extra: {json.dumps(extra)}")
    else:
        logger.info(message)


def log_error(message: str, extra: Dict[str, Any] = None):
    """
    Log an error message.

    Args:
        message (str): The message to log
        extra (Dict[str, Any]): Additional context to include in the log
    """
    logger = logging.getLogger(__name__)
    if extra:
        logger.error(f"{message} - Extra: {json.dumps(extra)}")
    else:
        logger.error(message)


def log_debug(message: str, extra: Dict[str, Any] = None):
    """
    Log a debug message.

    Args:
        message (str): The message to log
        extra (Dict[str, Any]): Additional context to include in the log
    """
    logger = logging.getLogger(__name__)
    if extra:
        logger.debug(f"{message} - Extra: {json.dumps(extra)}")
    else:
        logger.debug(message)