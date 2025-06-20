from .llm_agent import LLMAgent
from memory import ModelApiType

class Qwen3Agent(LLMAgent):
    def __init__(self, input_receiver=None):
        super().__init__(
            agent_name='Qwen3_32B',
            # llm_name='qwen/qwen3-235b-a22b',
            llm_name='deepseek-ai/deepseek-r1-distill-qwen-32b',
            llm_api_type=ModelApiType.NVIDIA,
            input_receiver=input_receiver
        )
        self.name = 'Qwen3'