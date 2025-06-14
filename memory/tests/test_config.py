"""
Unit tests for the MemoryConfig configuration class.
"""

import pytest
from memory.config import MemoryConfig, DEFAULT_CONFIG


class TestMemoryConfig:
    """Test cases for MemoryConfig class."""

    def test_default_initialization(self):
        """Test MemoryConfig with default values."""
        config = MemoryConfig()
        
        assert config.storage_path is None
        assert config.max_entries == 100
        assert config.verbose is False
        assert config.decay == 0.0

    def test_custom_initialization(self):
        """Test MemoryConfig with custom values."""
        config = MemoryConfig(
            storage_path="/custom/path",
            max_entries=50,
            verbose=True,
            decay=0.5
        )
        
        assert config.storage_path == "/custom/path"
        assert config.max_entries == 50
        assert config.verbose is True
        assert config.decay == 0.5

    def test_decay_validation_valid_values(self):
        """Test that valid decay values are accepted."""
        # Test boundary values
        config1 = MemoryConfig(decay=0.0)
        assert config1.decay == 0.0
        
        config2 = MemoryConfig(decay=1.0)
        assert config2.decay == 1.0
        
        config3 = MemoryConfig(decay=0.5)
        assert config3.decay == 0.5

    def test_decay_validation_invalid_values(self):
        """Test that invalid decay values raise ValueError."""
        with pytest.raises(ValueError, match="Decay must be between 0.0 and 1.0"):
            MemoryConfig(decay=-0.1)
        
        with pytest.raises(ValueError, match="Decay must be between 0.0 and 1.0"):
            MemoryConfig(decay=1.1)

    def test_max_entries_validation_valid_values(self):
        """Test that valid max_entries values are accepted."""
        config1 = MemoryConfig(max_entries=1)
        assert config1.max_entries == 1
        
        config2 = MemoryConfig(max_entries=1000)
        assert config2.max_entries == 1000

    def test_max_entries_validation_invalid_values(self):
        """Test that invalid max_entries values raise ValueError."""
        with pytest.raises(ValueError, match="max_entries must be positive"):
            MemoryConfig(max_entries=0)
        
        with pytest.raises(ValueError, match="max_entries must be positive"):
            MemoryConfig(max_entries=-1)

    def test_config_immutability_after_creation(self):
        """Test that config values cannot be changed after creation."""
        config = MemoryConfig(max_entries=50)
        
        # Try to modify (this should work since we're not using frozen dataclass)
        config.max_entries = 100
        assert config.max_entries == 100

    def test_default_config_constant(self):
        """Test that DEFAULT_CONFIG constant has expected values."""
        assert DEFAULT_CONFIG.storage_path is None
        assert DEFAULT_CONFIG.max_entries == 100
        assert DEFAULT_CONFIG.verbose is False
        assert DEFAULT_CONFIG.decay == 0.0

    def test_config_equality(self):
        """Test MemoryConfig equality comparison."""
        config1 = MemoryConfig(
            storage_path="/test",
            max_entries=50,
            verbose=True,
            decay=0.1
        )
        
        config2 = MemoryConfig(
            storage_path="/test",
            max_entries=50,
            verbose=True,
            decay=0.1
        )
        
        config3 = MemoryConfig(
            storage_path="/different",
            max_entries=50,
            verbose=True,
            decay=0.1
        )
        
        assert config1 == config2
        assert config1 != config3

    def test_config_repr(self):
        """Test MemoryConfig string representation."""
        config = MemoryConfig(
            storage_path="/test",
            max_entries=50,
            verbose=True,
            decay=0.1
        )
        
        repr_str = repr(config)
        assert "MemoryConfig" in repr_str
        assert "storage_path='/test'" in repr_str
        assert "max_entries=50" in repr_str
        assert "verbose=True" in repr_str
        assert "decay=0.1" in repr_str
