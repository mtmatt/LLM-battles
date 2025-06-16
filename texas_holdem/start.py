from texas_holdem.game.game import setup_config, start_poker
from texas_holdem.agents.deepseek import DeepseekAgent
from texas_holdem.agents.gemma3 import Gemma3Agent
from texas_holdem.agents.gemini25 import Gemini25Agent
from texas_holdem.agents.nvidia_llama3_3 import NvidiaLlama3_3Agent
from texas_holdem.agents.qwen3 import Qwen3Agent

from random import shuffle

def main():
    config = setup_config(max_round=16, verbose=True)
    players = {
        "Deepseek": DeepseekAgent(),
        "Gemma3": Gemma3Agent(),
        "Gemini25": Gemini25Agent(),
        "Nvidia Llama3.3 49B": NvidiaLlama3_3Agent(),
        "Qwen3 235B a22B": Qwen3Agent(),
        "Human": None  # Placeholder for human player
    }
    shuffle(players)

    for name, agent in players.items():
        if agent is not None:
            config.add_player(name, agent)

    start_poker(config)

if __name__ == "__main__":
    main()