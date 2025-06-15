"""
Core memory functionality for the LLM battles project.

This module contains the main memory management classes and functions.
"""

from typing import Any, Dict, List, Optional
import json
import os
from openai import OpenAI
from google.genai import types
from google import genai
from .config import ModelApiType
import re
import time

MIN_MEMORY_LENGTH = 8


class SimpleMemoryManager:
    """
    Main memory manager class for handling memory operations.
    """

    _system_prompt = 'You are a memory assistant that summarizes text efficiently.'
    _task_prompt = '''Please summarize the following text with the following constraints:
        1. The summary should be exactly fit the specified number of words. (i.e. write as many as possible within the constraint)
        2. The summary should base on the given context.
        3. Wrap the summary in <summary> and </summary> tags.
        4. Output directly, without repeating the prompt.
        5. Simply comply the rule.
        Word Quota: '''

    def __init__(self, storage_path: Optional[str], max_entries, verbose: bool, decay: float,
                 llm_name: Optional[str] = None, llm_api_type: ModelApiType = ModelApiType.NVIDIA):
        """
        Initialize the memory manager.

        Args:
            storage_path: Optional path for persistent storage
        """
        self.storage_path: str = storage_path or 'memory_data'
        self._memory_store: List[str] = []
        self.max_entries = max_entries
        self.verbose = verbose
        self.decay = decay
        self.llm_name = llm_name
        self.llm_api_type = llm_api_type

        if self.llm_api_type == ModelApiType.NVIDIA:
            api_key = os.getenv('NVIDIA_API_KEY')
            if not api_key:
                raise ValueError(
                    'NVIDIA API key is not set in environment variables.')
            self._llm_client = OpenAI(api_key=api_key,
                                      base_url='https://integrate.api.nvidia.com/v1') if self.llm_name else None
        elif self.llm_api_type == ModelApiType.GOOGLE:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError(
                    'NVIDIA API key is not set in environment variables.')
            self._llm_client = genai.Client(
                api_key=api_key) if self.llm_name else None
        else:
            raise ValueError(f"Unsupported LLM API type: {self.llm_api_type}")

        if self.max_entries <= 0:
            raise ValueError("max_entries must be a positive integer")
        if self.decay < 0.0 or self.decay > 1.0:
            raise ValueError("decay must be between 0.0 and 1.0")
        self._ensure_storage_directory()
        if self.verbose:
            print(
                f"[Memory Manger] Initializing memory manager with storage path: {self.storage_path}")

    def _ensure_storage_directory(self):
        """Ensure the storage directory exists."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _compress_memory(self) -> None:
        for i in range(len(self._memory_store)):
            if len(self._memory_store[i]) < MIN_MEMORY_LENGTH:
                continue
            if hasattr(self, '_llm_client') and self._llm_client:
                # Use a simple whitespace tokenizer as approximation
                tokens = self._memory_store[i].split()
                max_tokens = max(
                    int(len(tokens) * (1 - self.decay)), MIN_MEMORY_LENGTH)
                if self.verbose:
                    print(
                        f'[Memory Manger] Applying decay: {self.decay} to memory entry {i}. Original length: {len(tokens)}, New length: {max_tokens}')

                memory_compression_prompt = f'{self._task_prompt} {max_tokens}\n\n Contents:\n{self._memory_store[i]}'
                if self.llm_api_type == ModelApiType.NVIDIA:
                    response = self._llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=[
                            {'role': 'system',
                                'content': self._system_prompt},
                            {'role': 'user',
                                'content': memory_compression_prompt}
                        ],
                        max_tokens=max_tokens + 128,
                        temperature=0.2,
                        top_p=0.95
                    )
                    summarized_memory = response.choices[0].message.content
                elif self.llm_api_type == ModelApiType.GOOGLE:
                    config = types.GenerateContentConfig(
                        temperature=0.2,
                        top_p=0.95,
                        max_output_tokens=max_tokens + 128,
                        system_instruction=self._system_prompt,
                    )
                    response = self._llm_client.models.generate_content(
                        model=self.llm_name,
                        contents=memory_compression_prompt,
                        config=config
                    )
                    print(f'Res: {response}')
                    summarized_memory = response.text
            else:
                raise ValueError(
                    'LLM client is not initialized. Cannot apply decay.')

            # Extract summary from <summary> tags
            summary_match = re.search(
                r'<summary>(.*?)</summary>|<summary>(.*?)$|\(summary\)(.*?)\(/summary\)|\(summary\)(.*?)$|\[summary\](.*?)\[/summary\]|\[summary\](.*?)$|\{summary\}(.*?)\{/summary\}|\{summary\}(.*?)$',
                summarized_memory, re.DOTALL)
            if summary_match:
                self._memory_store[i] = summary_match.group(1) or summary_match.group(2) or \
                    summary_match.group(3) or summary_match.group(4)
                if self.verbose:
                    print(f'[Memory Manger] Compressed memory entry {i}')
            else:
                print(f'Summary: {summarized_memory}')
                raise ValueError(
                    'Memory compression did not return a valid summary. Ensure the LLM is configured correctly.')

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

        if self.decay > 0.0:
            self._compress_memory()
        if self.verbose:
            print(
                f"[Memory Manger] Current memory size: {len(self._memory_store)}")

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
            ret += f'<{memory_size - idx} round before>\n' + \
                s + f'\n</{memory_size - idx} round before>\n\n'
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
            filename = os.path.join(
                self.storage_path, f'memory_{int(os.time.time())}.json')

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
