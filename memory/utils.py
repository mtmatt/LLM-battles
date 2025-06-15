"""
Utility functions for the memory module.
"""

from typing import Any, Dict, List, Optional
from .config import MemoryConfig
from .core import SimpleMemoryManager

def create_memory_from_config(config: MemoryConfig) -> SimpleMemoryManager:
    """
    Create a MemoryManager instance from a MemoryConfig instance.

    Args:
        config (MemoryConfig): Configuration for the memory manager.

    Returns:
        MemoryManager: An instance of MemoryManager initialized with the provided configuration.
    """
    return SimpleMemoryManager(
        storage_path=config.storage_path,
        max_entries=config.max_entries,
        verbose=config.verbose,
        decay=config.decay,
        llm_name=config.model_name,
        llm_api_type=config.model_api_type
    )