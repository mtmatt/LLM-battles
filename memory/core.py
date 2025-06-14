"""
Core memory functionality for the LLM battles project.

This module contains the main memory management classes and functions.
"""

from typing import Any, Dict, List, Optional
import json
import os


class MemoryManager:
    """
    Main memory manager class for handling memory operations.
    """

    def __init__(self, storage_path: Optional[str], max_entries, verbose: bool, decay: float):
        """
        Initialize the memory manager.

        Args:
            storage_path: Optional path for persistent storage
        """
        self.storage_path: str = storage_path or "memory_data"
        self._memory_store: List[str] = []
        self.max_entries = max_entries
        self.verbose = verbose
        self.decay = decay
        if self.max_entries <= 0:
            raise ValueError("max_entries must be a positive integer")
        if self.decay < 0.0 or self.decay > 1.0:
            raise ValueError("decay must be between 0.0 and 1.0")
        self._ensure_storage_directory()
        if self.verbose:
            print(f"[Memory Manger] Initializing memory manager with storage path: {self.storage_path}")

    def _ensure_storage_directory(self):
        """Ensure the storage directory exists."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def store(self, value: Any) -> None:
        """
        Store a value in memory.

        Args:
            key: Unique identifier for the memory
            value: The value to store
            metadata: Optional metadata about the memory
        """
        self._memory_store.append(value)
        if len(self._memory_store) > 8:
            self._memory_store.pop(0)
        # TODO: make the memories before more concise, by calling LLM
        if self.decay > 0.0:
            pass
        if self.verbose:
            print(f"[Memory Manger] Stored value: {value}. Current memory size: {len(self._memory_store)}")

    def retrieve(self) -> Optional[str]:
        """
        Retrieve a value from memory.

        Args:
            key: The key to retrieve

        Returns:
            The stored value or None if not found
        """
        if not self._memory_store:
            return None
            
        ret = ""
        memory_size = len(self._memory_store)
        for idx, s in enumerate(self._memory_store):
            ret += f'<{memory_size - idx} round before>\n' + s + f'\n</{memory_size - idx} round before>\n\n'
        return ret

    def clear(self) -> None:
        """Clear all memory entries."""
        self._memory_store.clear()
        if self.verbose:
            print("[Memory Manger] Memory cleared.")

    def save_to_file(self, filename: Optional[str] = None) -> None:
        """
        Save memory to a JSON file.

        Args:
            filename: Optional filename, defaults to timestamped file
        """
        if filename is None:
            filename = os.path.join(self.storage_path, f'memory_{int(os.time.time())}.json')
        
        memory_json = {}
        for idx, value in enumerate(self._memory_store):
            memory_json[f'{len(self._memory_store) - idx} round before'] = value
        
        with open(filename, 'w') as f:
            json.dump(memory_json, f, indent=4)
        
        if self.verbose:
            print(f"[Memory Manger] Memory saved to {filename}")

    def load_from_file(self, filename: str) -> None:
        """
        Load memory from a JSON file.

        Args:
            filename: The filename to load from
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Memory file {filename} does not exist.")
        
        with open(filename, 'r') as f:
            memory_json = json.load(f)
        
        self._memory_store = []
        for _, value in memory_json.items():
            self._memory_store.append(value)
        
        if self.verbose:
            print(f"[Memory Manger] Memory loaded from {filename}")
