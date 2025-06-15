"""
Unit tests for the MemoryManager core functionality.
"""

import pytest
import tempfile
import shutil
import os
from unittest.mock import patch, MagicMock

from memory.core import SimpleMemoryManager
from memory.config import MemoryConfig
from memory.utils import create_memory_from_config


class TestMemoryManager:
    """Test cases for MemoryManager class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = MemoryConfig(
            storage_path=self.temp_dir,
            max_entries=5,
            verbose=False,
            decay=0.0
        )
        self.memory_manager = create_memory_from_config(self.config)

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test memory manager initialization."""
        assert self.memory_manager.storage_path == self.temp_dir
        assert self.memory_manager.max_entries == 5
        assert self.memory_manager.verbose is False
        assert len(self.memory_manager._memory_store) == 0

    def test_store_single_value(self):
        """Test storing a single value."""
        self.memory_manager.store("Test memory")
        assert len(self.memory_manager._memory_store) == 1
        assert "Test memory" in self.memory_manager._memory_store

    def test_store_multiple_values(self):
        """Test storing multiple values."""
        values = ["Memory 1", "Memory 2", "Memory 3"]
        for value in values:
            self.memory_manager.store(value)
        
        assert len(self.memory_manager._memory_store) == 3
        for value in values:
            assert value in self.memory_manager._memory_store

    def test_max_entries_limit(self):
        """Test that memory store respects max_entries limit."""
        # Store more than max_entries
        for i in range(10):
            self.memory_manager.store(f"Memory {i}")
        
        # Should only keep the last max_entries items
        assert len(self.memory_manager._memory_store) == 5
        
        # Check that oldest entries were removed
        assert "Memory 0" not in self.memory_manager._memory_store
        assert "Memory 9" in self.memory_manager._memory_store

    def test_retrieve_empty_memory(self):
        """Test retrieving from empty memory."""
        result = self.memory_manager.retrieve()
        assert result is None

    def test_retrieve_with_memories(self):
        """Test retrieving memories."""
        self.memory_manager.store("Memory 1")
        self.memory_manager.store("Memory 2")
        
        result = self.memory_manager.retrieve()
        assert result is not None
        assert "Memory 1" in result
        assert "Memory 2" in result
        assert "<2 round before>" in result
        assert "<1 round before>" in result

    def test_clear_memory(self):
        """Test clearing all memories."""
        self.memory_manager.store("Memory 1")
        self.memory_manager.store("Memory 2")
        assert len(self.memory_manager._memory_store) == 2
        
        self.memory_manager.clear()
        assert len(self.memory_manager._memory_store) == 0

    def test_save_to_file(self):
        """Test saving memories to file."""
        self.memory_manager.store("Memory 1")
        self.memory_manager.store("Memory 2")
        
        filename = os.path.join(self.temp_dir, "test_save.json")
        self.memory_manager.save_to_file(filename)
        
        assert os.path.exists(filename)

    def test_load_from_file(self):
        """Test loading memories from file."""
        # First save some data
        self.memory_manager.store("Memory 1")
        self.memory_manager.store("Memory 2")
        filename = os.path.join(self.temp_dir, "test_load.json")
        self.memory_manager.save_to_file(filename)
        
        # Clear and load
        self.memory_manager.clear()
        assert len(self.memory_manager._memory_store) == 0
        
        self.memory_manager.load_from_file(filename)
        assert len(self.memory_manager._memory_store) == 2
        assert "Memory 1" in self.memory_manager._memory_store
        assert "Memory 2" in self.memory_manager._memory_store

    @patch('builtins.print')
    def test_verbose_mode(self, mock_print):
        """Test verbose logging."""
        verbose_config = MemoryConfig(
            storage_path=self.temp_dir,
            max_entries=5,
            verbose=True,
            decay=0.0
        )
        verbose_manager = create_memory_from_config(verbose_config)
        
        verbose_manager.store("Test memory")
        mock_print.assert_called()

    def test_storage_directory_creation(self):
        """Test that storage directory is created if it doesn't exist."""
        new_path = os.path.join(self.temp_dir, "new_storage")
        config = MemoryConfig(
            storage_path=new_path,
            max_entries=5,
            verbose=False,
            decay=0.0
        )
        
        # Directory shouldn't exist yet
        assert not os.path.exists(new_path)
        
        # Creating manager should create the directory
        manager = create_memory_from_config(config)
        assert os.path.exists(new_path)


@pytest.mark.integration
class TestMemoryManagerIntegration:
    """Integration tests for MemoryManager."""

    def test_full_workflow(self):
        """Test complete memory management workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = MemoryConfig(
                storage_path=temp_dir,
                max_entries=3,
                verbose=True,
                decay=0.0
            )
            
            manager = create_memory_from_config(config)
            
            # Store some memories
            memories = ["First memory", "Second memory", "Third memory"]
            for memory in memories:
                manager.store(memory)
            
            # Retrieve and verify
            result = manager.retrieve()
            assert result is not None
            for memory in memories:
                assert memory in result
            
            # Save to file
            save_path = os.path.join(temp_dir, "memories.json")
            manager.save_to_file(save_path)
            assert os.path.exists(save_path)
            
            # Create new manager and load
            new_manager = create_memory_from_config(config)
            new_manager.load_from_file(save_path)
            
            # Verify loaded memories
            loaded_result = new_manager.retrieve()
            assert loaded_result == result
