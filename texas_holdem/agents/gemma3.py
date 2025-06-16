from .llm_agent import LLMAgent
from memory import ModelApiType

class Gemma3Agent(LLMAgent):
    def __init__(self, input_receiver=None):
        super().__init__(
            agent_name='Gemma3_27B',
            llm_name='google/gemma-3-27b-it',  # Use working model
            llm_api_type=ModelApiType.NVIDIA,
            input_receiver=input_receiver
        )
        self.name = 'Gemma3 27B'