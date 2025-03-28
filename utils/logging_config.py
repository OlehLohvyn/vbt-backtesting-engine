"""
Logging configuration for the vbt-backtesting-engine project.

This module defines a centralized logger named 'vbt_engine' with a consistent
format and INFO-level logging. It avoids adding duplicate handlers when imported
multiple times.

Usage:
    from utils.logging_config import logger
    logger.info("This is a log message.")
"""

import logging

# Create a named logger instance for the project
logger = logging.getLogger("vbt_engine")
logger.setLevel(logging.INFO)

# Add handler only once to avoid duplicate logs in repeated imports
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
