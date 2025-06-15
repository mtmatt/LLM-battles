from memory import create_memory_from_config, MemoryConfig, ModelApiType

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

def test_memory_decay():
    """Test memory decay functionality."""
    config = MemoryConfig(
        storage_path=None,
        max_entries=10,
        verbose=True,
        decay=0.1,
        # model_name='nvidia/llama-3.3-nemotron-super-49b-v1',
        model_name='google/gemma-3-27b-it',
        model_api_type=ModelApiType.NVIDIA

        # model_name='gemini-2.0-flash',
        # model_name='gemini-2.5-flash-preview-05-20',
        # model_api_type=ModelApiType.GOOGLE
    )
    memory_manager = create_memory_from_config(config)

    with open('texas_holdem/rules.md', 'r') as f:
        rules = f.read()
    # Store some values
    for i in range(3):
        memory_manager.store(rules)

    data = memory_manager.retrieve()
    assert data is not None, 'Expected to retrieve a value from memory after decay'

    with open('tests/test_memory_decay.md', 'w') as f:
        f.write(data)
    print(f'Decayed Data: \n{data}')

if __name__ == "__main__":
    test_memory_manager()
    test_memory_decay()
    print("MemoryManager test completed successfully.")