from .llm_agent import LLMAgent
from memory import ModelApiType

class Gemini25Agent(LLMAgent):
    def __init__(self, input_receiver=None):
        super().__init__(
            agent_name='Gemini_2_5',
            # llm_name='gemini-2.0-flash-exp',
            llm_name='gemini-2.5-flash-preview-05-20',
            llm_api_type=ModelApiType.GOOGLE,
            input_receiver=input_receiver
        )
        self.name = 'Gemini2.5'