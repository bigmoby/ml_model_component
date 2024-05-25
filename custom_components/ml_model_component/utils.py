"""Utilities for ML model Assistant Integration.

This module provides utility functions for checking if a string is blank or not.

Functions:
    isNotBlank(test_string: str | None) -> bool: Check if a string is not blank.
    isBlank(test_string: str | None) -> bool: Check if a string is blank.
"""


def isNotBlank(test_string: str | None) -> bool:
    """Check if a string is not blank.

    This function returns True if the input string is not None, not empty, and contains
    non-whitespace characters. Otherwise, it returns False.

    Args:
        test_string (str | None): The string to be tested.

    Returns:
        bool: True if the string is not blank, False otherwise.

    """
    return bool(test_string and test_string.strip())


def isBlank(test_string: str | None) -> bool:
    """Check if a string is blank.

    This function returns True if the input string is None, empty, or contains only
    whitespace characters. Otherwise, it returns False.

    Args:
        test_string (str | None): The string to be tested.

    Returns:
        bool: True if the string is blank, False otherwise.

    """
    return not (test_string and test_string.strip())
