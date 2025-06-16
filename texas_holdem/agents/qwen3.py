from .baseagent import BaseAgent

class Qwen3Agent(BaseAgent):
    def __init__(self, input_receiver=None):
        super().__init__(input_receiver)
        self.name = 'Qwen3 235B a22B'

    def declare_action(self, valid_actions, hole_card, round_state):
        # Here you would implement the logic to interact with Qwen 3 70B API
        # For now, we will just call the base class method
        return super().declare_action(valid_actions, hole_card, round_state)