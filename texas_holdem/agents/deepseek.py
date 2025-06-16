from .baseagent import BaseAgent

class DeepseekAgent(BaseAgent):
    def __init__(self, input_receiver=None):
        super().__init__(input_receiver)
        self.name = 'DeepSeek R1'

    def declare_action(self, valid_actions, hole_card, round_state):
        # Here you would implement the logic to interact with DeepSeek 70B API
        # For now, we will just call the base class method
        return super().declare_action(valid_actions, hole_card, round_state)