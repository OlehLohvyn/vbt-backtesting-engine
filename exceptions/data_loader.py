"""
Custom exception definitions for data loading operations.

This module defines exceptions related to the data loading process,
including common issues that may arise during downloading, validation,
or saving of market data.

Use these exceptions across the project to maintain consistency in error handling.
"""

class DataLoaderError(Exception):
    """Base exception for all data loading errors."""
    pass
