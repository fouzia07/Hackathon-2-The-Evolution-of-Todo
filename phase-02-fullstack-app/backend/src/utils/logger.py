"""
Comprehensive logging utilities for the Full-Stack Web Todo Application.

This module provides centralized logging functionality for the application.
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum


class LogLevel(Enum):
    """
    Log level enumeration.
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """
    Centralized logger for the application.
    """
    def __init__(self, name: str = "TodoApp", level: LogLevel = LogLevel.INFO):
        """
        Initialize the logger.

        Args:
            name (str): Name of the logger
            level (LogLevel): Minimum log level to record
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.value))

        # Prevent adding handlers multiple times
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.value))

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
            console_handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(console_handler)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a debug message.

        Args:
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        self._log(LogLevel.DEBUG, message, extra)

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an info message.

        Args:
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        self._log(LogLevel.INFO, message, extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a warning message.

        Args:
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        self._log(LogLevel.WARNING, message, extra)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an error message.

        Args:
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        self._log(LogLevel.ERROR, message, extra)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a critical message.

        Args:
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        self._log(LogLevel.CRITICAL, message, extra)

    def _log(self, level: LogLevel, message: str, extra: Optional[Dict[str, Any]]) -> None:
        """
        Internal method to log a message.

        Args:
            level (LogLevel): The log level
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        if extra:
            # Convert extra to string representation for logging
            extra_str = " | ".join([f"{k}={v}" for k, v in extra.items()])
            full_message = f"{message} [{extra_str}]"
        else:
            full_message = message

        getattr(self.logger, level.value.lower())(full_message)

    def log_exception(self, message: str = "An exception occurred", extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an exception with traceback.

        Args:
            message (str): The message to log
            extra (Optional[Dict[str, Any]]): Additional context to include in the log
        """
        if extra:
            extra_str = " | ".join([f"{k}={v}" for k, v in extra.items()])
            full_message = f"{message} [{extra_str}]"
        else:
            full_message = message

        self.logger.exception(full_message)


# Create a global logger instance
app_logger = Logger()


# Convenience functions for easy access
def log_debug(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Log a debug message using the global logger.

    Args:
        message (str): The message to log
        extra (Optional[Dict[str, Any]]): Additional context to include in the log
    """
    app_logger.debug(message, extra)


def log_info(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an info message using the global logger.

    Args:
        message (str): The message to log
        extra (Optional[Dict[str, Any]]): Additional context to include in the log
    """
    app_logger.info(message, extra)


def log_warning(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Log a warning message using the global logger.

    Args:
        message (str): The message to log
        extra (Optional[Dict[str, Any]]): Additional context to include in the log
    """
    app_logger.warning(message, extra)


def log_error(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an error message using the global logger.

    Args:
        message (str): The message to log
        extra (Optional[Dict[str, Any]]): Additional context to include in the log
    """
    app_logger.error(message, extra)


def log_critical(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Log a critical message using the global logger.

    Args:
        message (str): The message to log
        extra (Optional[Dict[str, Any]]): Additional context to include in the log
    """
    app_logger.critical(message, extra)


def log_exception(message: str = "An exception occurred", extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an exception with traceback using the global logger.

    Args:
        message (str): The message to log
        extra (Optional[Dict[str, Any]]): Additional context to include in the log
    """
    app_logger.log_exception(message, extra)