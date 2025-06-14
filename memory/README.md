# LLM Battles Memory

A sophisticated memory management system for Large Language Model (LLM) applications.

## Features

- **Configurable Memory Storage**: Flexible storage backends with customizable parameters
- **Memory Decay**: Optional time-based decay for forgetting old memories
- **Verbose Logging**: Detailed logging for debugging and monitoring
- **Persistent Storage**: Save and load memory state to/from files
- **Type Safety**: Full type hints for better development experience
- **Extensible Design**: Easy to extend and customize for specific use cases

## Installation

### From Source

```bash
git clone https://github.com/llm-battles/memory.git
cd memory
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/llm-battles/memory.git
cd memory
pip install -e ".[dev]"
```

## Quick Start

```python
from memory import MemoryManager, MemoryConfig, create_memory_from_config

# Create a memory configuration
config = MemoryConfig(
    storage_path="my_memory",
    max_entries=100,
    verbose=True,
    decay=0.1
)

# Create memory manager
memory_manager = create_memory_from_config(config)

# Store memories
memory_manager.store("Important information to remember")
memory_manager.store("Another piece of data")

# Retrieve memories
all_memories = memory_manager.retrieve()
print(all_memories)

# Save to file
memory_manager.save_to_file("backup.json")

# Clear memories
memory_manager.clear()
```

## Configuration

The `MemoryConfig` class provides various configuration options:

- `storage_path`: Directory path for persistent storage (default: "memory_data")
- `max_entries`: Maximum number of memory entries to keep (default: 100)
- `verbose`: Enable verbose logging (default: False)
- `decay`: Memory decay factor between 0.0 and 1.0 (default: 0.0)

## API Reference

### MemoryManager

The main class for memory management operations.

#### Methods

- `store(value: str)`: Store a new memory entry
- `retrieve() -> Optional[str]`: Retrieve all memories formatted with round indicators
- `clear()`: Clear all memory entries
- `save_to_file(filename: Optional[str] = None)`: Save memories to a JSON file
- `load_from_file(filename: str)`: Load memories from a JSON file

### MemoryConfig

Configuration class for memory manager settings.

### Utility Functions

- `create_memory_from_config(config: MemoryConfig) -> MemoryManager`: Factory function to create memory manager from config

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/llm-battles/memory.git
cd memory

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=memory

# Run specific test categories
pytest -m unit
pytest -m integration
```

### Code Quality

```bash
# Format code
black memory tests

# Sort imports
isort memory tests

# Lint code
flake8 memory tests

# Type checking
mypy memory
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0 (2024-XX-XX)

- Initial release
- Basic memory management functionality
- Configurable storage options
- Memory decay support
- Persistent storage capabilities
