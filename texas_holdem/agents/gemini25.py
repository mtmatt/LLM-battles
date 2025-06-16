from .baseagent import BaseAgent

class Gemini25Agent(BaseAgent):
    def __init__(self, input_receiver=None):
        super().__init__(input_receiver)
        self.name = 'Gemini 2.5'

    def declare_action(self, valid_actions, hole_card, round_state):
        # Here you would implement the logic to interact with Gemini 2.5 API
        # For now, we will just call the base class method
        return super().declare_action(valid_actions, hole_card, round_state)