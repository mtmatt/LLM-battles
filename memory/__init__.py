"""
Memory module for LLM battles project.

This module provides memory-related functionality for the LLM battles application.
"""

__version__ = "0.1.0"
__author__ = "LLM Battles Project"

# Import main classes/functions
from .core import MemoryManager
from .config import MemoryConfig, DEFAULT_CONFIG
from .utils import (
    serialize_value,
    deserialize_value,
    format_memory_stats,
)

__all__ = [
    "MemoryManager",
    "MemoryConfig", 
    "DEFAULT_CONFIG",
    "generate_memory_key",
    "serialize_value",
    "deserialize_value",
    "format_memory_stats",
    "cleanup_old_entries"
]
