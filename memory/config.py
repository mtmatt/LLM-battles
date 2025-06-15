"""
Configuration settings for the memory module.
"""

import os
from dataclasses import dataclass
from typing import Optional
import enum

class ModelApiType(enum.Enum):
    """Enum for model API types."""
    NVIDIA = 'nvidia'
    GOOGLE = 'google'

@dataclass
class MemoryConfig:
    """Configuration class for memory settings."""

    # Storage settings
    storage_path: Optional[str] = None
    max_entries: int = 100
    verbose: bool = False
    # Decay factor for memory length, for example, 0.3 means 30% of the memory length will be decayed in each round
    decay: float = 0.0
    model_name: Optional[str] = None
    model_api_type: ModelApiType = ModelApiType.NVIDIA

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
            decay=float(os.getenv('MEMORY_DECAY', '0.0')),
            model_name=os.getenv('MEMORY_MODEL_NAME'),
            model_api_type=ModelApiType(os.getenv('MEMORY_MODEL_API_TYPE', 'nvidia').lower())
        )

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            'storage_path': self.storage_path,
            'max_entries': self.max_entries,
            'verbose': self.verbose,
            'decay': self.decay,
            'model_name': self.model_name,
            'model_api_type': self.model_api_type.value
        }


# Default configuration instance
DEFAULT_CONFIG = MemoryConfig()
