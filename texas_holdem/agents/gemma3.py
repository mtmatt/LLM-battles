from .baseagent import BaseAgent

class Gemma3Agent(BaseAgent):
    def __init__(self, input_receiver=None):
        super().__init__(input_receiver)
        self.name = 'Gemma3 27B'

    def declare_action(self, valid_actions, hole_card, round_state):
        # Here you would implement the logic to interact with Gemma 3 27B API
        # For now, we will just call the base class method
        return super().declare_action(valid_actions, hole_card, round_state)