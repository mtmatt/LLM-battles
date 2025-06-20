"""
Memory module for LLM battles project.

This module provides memory-related functionality for the LLM battles application.
"""

__version__ = "0.1.0"
__author__ = "LLM Battles Project"

# Import main classes/functions
from .core import SimpleMemoryManager
from .config import MemoryConfig, DEFAULT_CONFIG, ModelApiType
from .utils import create_memory_from_config


__all__ = [
    "SimpleMemoryManager",
    "MemoryConfig", 
    "DEFAULT_CONFIG",
    "create_memory_from_config",
    "ModelApiType"
]
