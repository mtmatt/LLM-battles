import re

summarized_memory = """
(summary)
Texas Hold'em Poker, the most popular variant globally, aims for players to make the best five-card hand using two hole cards and five community cards, winning by having the strongest hand or forcing others to fold.

### **Objective & Game Setup**
- **Players & Cards**: 2-10 players, standard 52-card deck, 2 hole cards per player, 5 community cards.
- **Table Positions**: Dealer button rotates clockwise. Small blind (player left of button) and big blind (next player, typically twice the small blind) are mandatory bets.

### **Betting Actions**
- **Actions**: Fold, Check (no bet), Call (match bet), Raise (increase bet), All-in (bet all chips).

### **Betting Rounds**
1. **Pre-flop**: After hole cards, betting starts left of big blind.
2. **The Flop**: Three community cards, betting round starts clockwise from the button.
3. **The Turn ("Fourth Street")**: Fourth community card, another betting round.
4. **The River ("Fifth Street")**: Final community card, last betting round.

### **Showdown & Winning**
- **Showdown**: If ≥2 players remain, they reveal hands starting with the last bettor or the player clockwise from the button if no final bet.
- **Hand Evaluation**: Best five cards from seven (hole + community). **Key Principle**: Use the best five cards available; you can use zero hole cards if the board is stronger.
- **Hand Rankings (Strongest to Weakest)**:
  1. Royal Flush
  2. Straight Flush
  3. Four-of-a-Kind
  4. Full House
  5. Flush
  6. Straight
  7. Three-of-a-Kind
  8. Two Pair
  9. One Pair
  10. High Card
- **Tie-Breaks**: Compare highest cards, pairs, kickers, etc., depending on the hand type.

### **Alternative Wins & Key Rules**
- **Fold-Out**: Win by folding out all opponents.
- **Bluffing**: Betting weak hands to force folds.
- **Betting Limits**: Typically no-limit; minimum bet equals big blind.
- **Dealer Procedures**: Burning cards before flop, turn, and river; clockwise dealing from the small blind.
- **Live Blinds**: Blinds count towards betting action, allowing the big blind to check or raise if all call.

### **Detailed Key Points for Clarity**
- **Using All Seven Cards**: The primary rule in hand evaluation is utilizing the best five cards from the total seven (two hole cards + five community cards), with the flexibility to use none of your hole cards if the community cards offer a better hand.
- **Tie-Breaking Examples**:
  - **High Card/One Pair**: Highest card wins. For pairs, the higher pair wins first.
  - **Two Pair**: Higher pair first, then lower pair, and the kicker.
  - **Straight**: Highest top card determines the winner.
  - **Full House**: Three matching cards compared first, then the pair.

(/summary)
"""


# """
# <summary>This is a test summary of the memory.</summary>
# (summary) This is another test summary of the memory.(/summary)
# [summary]This is yet another test summary of the memory.[/summary]
# {summary}This is a final test summary of the memory.{/summary}
# """

summary_match = re.search(
    r'<summary>(.*?)</summary>|\(summary\)(.*?)\(/summary\)|\[summary\](.*?)\[/summary\]|\{summary\}(.*?)\{/summary\}', summarized_memory, re.DOTALL)
if summary_match:
    text = summary_match.group(1) or summary_match.group(
        2) or summary_match.group(3) or summary_match.group(4)
    print(f'Extracted summary: {text}')
else:
    raise ValueError(
        "Memory compression did not return a valid summary. Ensure the LLM is configured correctly.")
