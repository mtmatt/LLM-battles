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
    storage_path: Optional[str] = None
    max_entries: int = 100
    verbose: bool = False
    # Decay factor for memory length, for example, 0.3 means 30% of the memory length will be decayed in each round
    decay: float = 0.0

    def __post_init__(self) -> None:
        """Validate configuration parameters after initialization."""
        if self.max_entries <= 0:
            raise ValueError("max_entries must be positive")
        
        if not (0.0 <= self.decay <= 1.0):
            raise ValueError("Decay must be between 0.0 and 1.0")

    @classmethod
    def from_env(cls) -> 'MemoryConfig':
        """
        Create configuration from environment variables.

        Returns:
            MemoryConfig instance with values from environment
        """
        return cls(
            storage_path=os.getenv('MEMORY_STORAGE_PATH'),
            max_entries=int(os.getenv('MEMORY_MAX_ENTRIES', '100')),
            verbose=os.getenv('MEMORY_VERBOSE', 'false').lower() == 'true',
            decay=float(os.getenv('MEMORY_DECAY', '0.0'))
        )

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            'storage_path': self.storage_path,
            'max_entries': self.max_entries,
            'verbose': self.verbose,
            'decay': self.decay
        }


# Default configuration instance
DEFAULT_CONFIG = MemoryConfig()
