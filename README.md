# LLM-battles

Testing Large Language Model via playing multiplayer games.


## Introduction

This project involves three stages.

1. Strategy games.
1. Environment base games including some unknown rules.
1. A small simulated world.

We will give our LLMs several different memory model, allowing us to modify their ability.


## Memory Models

The memory model is the key of the game. It allows players to remember past actions and opinions of other players. We first implemented a simple memory model that stores the last 8 rounds. The memory will decay over time, so the most recent actions will have more weight.

### Simple Time Decaying Model

For example, if the current round is round 12, the memory will look like this:
```
The following is your memories on the last 8 rounds of the game.

<8 round before>
This part is the memory 8 rounds before the current round.
</8 round before>

<7 round before>
This part is the memory 7 rounds before the current round.
</7 round before>

<6 round before>
This part is the memory 6 rounds before the current round.
</6 round before>

...

<1 round before>
This part is the memory 1 round before the current round.
</1 round before>
```


## LLMs

- Google Gemini 2.0, 2.5 Flash
- Google Gemma 27B
- Mistral Medium
- Deepseek R1
- llama3-nemo-128B
- Qwen3 32B
- Microsoft Phi4
- <font color="red">Possible GP 4o</font>
- <font color="red">Possible Claude 4</font>


## First Stage: Strategy Games

In this stage, we focus on clear-ruled games. 

- [Texas hold'em](docs/stage1/texas_holdem.md)
- [Minimum Unique Number](docs/stage1/minimum_unique_number.md)
- [Bomb Defusal](docs/stage1/bomb_defusal.md)

<!-- Planning -->


## Second Stage: Some Unknown rules

In this stage, we want the LLMs to explore the game environment and find the underlying rules and solve the game.

<!-- Planning -->


## Third Stage: A Small Simulated World

In this stage, we will create a small simulated world where LLMs can interact with each other and the environment. The world will have its own rules and dynamics, and LLMs will need to adapt to survive and thrive.

<!-- Planning -->