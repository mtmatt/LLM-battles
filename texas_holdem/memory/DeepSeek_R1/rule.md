### Texas Hold'em Rules Summary for AI Strategy  
**Objective**: Win chips by either:  
- Having the best 5-card hand at showdown, OR  
- Forcing all opponents to fold through betting/bluffing.  

#### Core Mechanics  
- **Setup**:  
  - 2–10 players; 52-card deck.  
  - Each player gets 2 private **hole cards** (face down).  
  - 5 **community cards** dealt face up in stages: *Flop* (3), *Turn* (1), *River* (1).  
- **Positions**:  
  - **Dealer button** rotates clockwise post-hand.  
  - **Blinds**: Small blind (left of button) and big blind (left of small blind, typically 2×). Forced bets that initiate action.  

#### Betting Actions (Key for AI Decision-Making)  
| Action  | Strategic Relevance |  
|---------|---------------------|  
| **Fold** | Preserve chips when hand is weak. |  
| **Check** | Pass action without cost (if no bet exists). |  
| **Call** | Match current bet to stay in hand. |  
| **Raise** | Apply pressure; bluff or extract value. |  
| **All-in** | Risk entire stack (critical in no-limit). |  

#### Betting Rounds (Act clockwise from button)  
1. **Pre-flop**:  
   - Start: Player left of big blind acts first.  
   - AI Focus: Assess hole card strength (e.g., pairs, suited connectors).  
2. **Flop** (3 community cards):  
   - Start: First active player left of button.  
   - AI Focus: Re-evaluate hand potential (draws, made hands).  
3. **Turn** (4th community card):  
   - Start: Same as flop.  
   - AI Focus: Adjust odds for draws; bet sizing for value/bluff.  
4. **River** (5th community card):  
   - Start: Same as flop.  
   - AI Focus: Final hand strength; maximize value or bluff.  

#### Winning Conditions  
- **Showdown** (if ≥2 players remain post-river):  
  - Use **best 5-card hand** from any combo of 2 hole + 5 community cards.  
  - *Tiebreaker*: Split pot if hands are identical.  
- **Win Without Showdown**:  
  - All opponents fold at any stage.  

#### Hand Rankings (Strongest to Weakest)  
| Rank | Hand Type | Tiebreak Rule |  
|------|-----------|---------------|  
| 1 | Royal Flush | All equal |  
| 2 | Straight Flush | Highest top card |  
| 3 | Four-of-a-Kind | Quad rank → Kicker |  
| 4 | Full House | Trips rank → Pair rank |  
| 5 | Flush | Compare cards high→low |  
| 6 | Straight | Highest top card |  
| 7 | Three-of-a-Kind | Trips rank → Kickers |  
| 8 | Two Pair | High pair → Low pair → Kicker |  
| 9 | One Pair | Pair rank → Kickers |  
| 10 | High Card | Compare all cards high→low |  

#### Critical AI Strategy Reminders  
- **Hand Evaluation**: Always optimize 5-card hand from 7 total cards (hole + community).  
- **Positional Awareness**: Later position = more information (act after opponents).  
- **Bluffing**: Use aggression to win pots without strong hands.  
- **Pot Control**: Balance value bets (strong hands) and bluffs (weak hands).  
- **Bankroll Management**: All-in decisions must account for stack depth and pot odds.  

> **Note**: No-limit rules allow any bet size up to stack size. Blinds are "live" (count toward call requirements).