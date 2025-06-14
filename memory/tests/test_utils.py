"""
Unit tests for utility functions.
"""

import pytest
import tempfile
import shutil

from memory.utils import create_memory_from_config
from memory.config import MemoryConfig
from memory.core import MemoryManager


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_create_memory_from_config_basic(self):
        """Test basic memory manager creation from config."""
        config = MemoryConfig(
            storage_path=None,
            max_entries=10,
            verbose=False,
            decay=0.0
        )
        
        manager = create_memory_from_config(config)
        
        assert isinstance(manager, MemoryManager)
        assert manager.max_entries == 10
        assert manager.verbose is False

    def test_create_memory_from_config_with_custom_path(self):
        """Test memory manager creation with custom storage path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = MemoryConfig(
                storage_path=temp_dir,
                max_entries=5,
                verbose=True,
                decay=0.2
            )
            
            manager = create_memory_from_config(config)
            
            assert isinstance(manager, MemoryManager)
            assert manager.storage_path == temp_dir
            assert manager.max_entries == 5
            assert manager.verbose is True

    def test_create_memory_from_config_preserves_all_settings(self):
        """Test that all configuration settings are preserved."""
        config = MemoryConfig(
            storage_path="/test/path",
            max_entries=42,
            verbose=True,
            decay=0.7
        )
        
        manager = create_memory_from_config(config)
        
        # Verify all settings are correctly applied
        assert manager.storage_path == "/test/path"
        assert manager.max_entries == 42
        assert manager.verbose is True
        # Note: decay might not be directly accessible, depending on implementation

    def test_create_memory_from_config_with_none_storage_path(self):
        """Test memory manager creation with None storage path."""
        config = MemoryConfig(storage_path=None)
        manager = create_memory_from_config(config)
        
        assert isinstance(manager, MemoryManager)
        # Should use default storage path
        assert manager.storage_path == "memory_data"

    def test_create_memory_from_config_multiple_instances(self):
        """Test creating multiple memory managers from the same config."""
        config = MemoryConfig(
            storage_path=None,
            max_entries=15,
            verbose=False,
            decay=0.1
        )
        
        manager1 = create_memory_from_config(config)
        manager2 = create_memory_from_config(config)
        
        # Should be different instances
        assert manager1 is not manager2
        assert isinstance(manager1, MemoryManager)
        assert isinstance(manager2, MemoryManager)
        
        # But with same configuration
        assert manager1.max_entries == manager2.max_entries
        assert manager1.verbose == manager2.verbose
        assert manager1.storage_path == manager2.storage_path
