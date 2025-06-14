from memory import create_memory_from_config, MemoryConfig

def test_memory_manager():
    """Test the MemoryManager functionality."""
    # Initialize memory manager with default config
    config = MemoryConfig(
        storage_path=None,
        max_entries=10,
        verbose=True,
        decay=0.0
    )
    memory_manager = create_memory_from_config(config)

    # Store some values
    for i in range(12):
        memory_manager.store(f'Value {i}')
    
    data = memory_manager.retrieve()
    assert data is not None, 'Expected to retrieve a value from memory'

    print(f'Data: \n{data}')

if __name__ == "__main__":
    test_memory_manager()
    print("MemoryManager test completed successfully.")