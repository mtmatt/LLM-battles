"""
Configuration settings for the memory module.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryConfig:
    """Configuration class for memory settings."""

    # Storage settings
    storage_path: str = "memory_data"
    pass

    @classmethod
    def from_env(cls) -> 'MemoryConfig':
        """
        Create configuration from environment variables.

        Returns:
            MemoryConfig instance with values from environment
        """
        return cls(
            storage_path=os.getenv('MEMORY_STORAGE_PATH', 'memory_data'),
        )

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            'storage_path': self.storage_path,
        }


# Default configuration instance
DEFAULT_CONFIG = MemoryConfig()
