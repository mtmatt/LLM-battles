from .llm_agent import LLMAgent
from memory import ModelApiType

class NvidiaLlama3_3Agent(LLMAgent):
    def __init__(self, input_receiver=None):
        super().__init__(
            agent_name='Nvidia_Llama3_3',
            llm_name='nvidia/llama-3.3-nemotron-super-49b-v1',
            llm_api_type=ModelApiType.NVIDIA,
            input_receiver=input_receiver
        )
        self.name = 'Nvidia Llama3.3 70B'