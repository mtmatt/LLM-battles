from .llm_agent import LLMAgent
from memory import ModelApiType

class DeepseekAgent(LLMAgent):
    def __init__(self, input_receiver=None):
        super().__init__(
            agent_name='DeepSeek_R1',
            llm_name='deepseek-ai/deepseek-r1',  # Use available model
            llm_api_type=ModelApiType.NVIDIA,
            input_receiver=input_receiver
        )
        self.name = 'DeepSeek R1'