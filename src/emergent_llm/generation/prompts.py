from emergent_llm.common.actions import Actions
from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.public_goods import PublicGoodsDescription


def format_game_description(game_description: GameDescription) -> str:
    """Format game description for prompts."""
    if isinstance(game_description, PublicGoodsDescription):
      return """GAME SPECIFICATION: N-Player Public Goods Game

PARAMETERS:
- n: number of players (integer, n ≥ 2)
- r: number of rounds (integer, r ≥ 1)
- k: multiplication factor (float, 1 < k < n)

GAME STRUCTURE:
- Type: Simultaneous-move, repeated game
- Rounds: r identical rounds
- Players: n players, indexed i ∈ {1, 2, ..., n}

ACTIONS PER ROUND:
Each player i has action set A_i = {C, D} where:
- C (Cooperate): Contribute endowment to community project
- D (Defect): Keep endowment privately

PAYOFF CALCULATION:
For player i in a single round:
π_i = (1 - c_i) + (k/n) × Σ(j=1 to n) c_j

where:
- c_i = 1 if player i plays C, c_i = 0 if player i plays D
- Σ(j=1 to n) c_j = total number of cooperators in the round

PAYOFF MATRIX INTERPRETATION:
- Private payoff from keeping: 1 - c_i
- Share of public good: (k/n) × total_contributions

EXAMPLE CALCULATIONS (n=6, k=2):
1. All players play D: π_i = 1 + (2/6) × 0 = 1 for all i
2. All players play C: π_i = 0 + (2/6) × 6 = 2 for all i
3. 3 players play C, 3 play D:
   - If player i played C: π_i = 0 + (2/6) × 3 = 1
   - If player i played D: π_i = 1 + (2/6) × 3 = 2

TOTAL GAME PAYOFF:
Total payoff for player i over r rounds = Σ(t=1 to r) π_i,t"""


#     elif isinstance(game_description, CollectiveRiskDescription):
#       return f"""Collective Risk Dilemma:
# {game_description.n_players} players, {game_description.n_rounds} rounds
# Each round: Choose Cooperate (C) or Defect (D)
# Defecting gives you 1.0 points
# If ≥{game_description.m} players cooperate, EVERYONE gets additional {game_description.k} points
# Example: If you defect and {game_description.m} others cooperate, you get 1.0 + {game_description.k} = {1.0 + game_description.k}
# Example: If only {game_description.m-1} cooperate, everyone gets base payoff only"""

    assert False, "GameDescription not recognised"


def create_strategy_user_prompt(attitude: Attitude, game_description: GameDescription) -> str:
    """Create user prompt for strategy description generation."""

    return f"""{format_game_description(game_description)}

Design a {attitude.lower()} strategy for this game. Your strategy should:

1. **Specify decision rules** - When exactly do you cooperate vs defect?
2. **Consider adaptation** - How do you respond to others' behavior over time?
3. **Handle edge cases** - What do you do in the first round, last rounds, etc.?
4. **Be {attitude.lower()}** - Clearly align with the {attitude.lower()} mindset

Provide a detailed strategy description with concrete decision rules. Include some pseudocode or logical steps if helpful."""


def create_code_user_prompt(strategy_description: str, game_description: GameDescription) -> str:
    """Create user prompt for code generation."""

    return f"""Your task is to convert a natural language strategy description into clean, efficient Python code.

Focus on:
- Correct logic implementation
- Proper state management using self attributes
- Handling edge cases (first round, empty history)
- Clean, readable code structure

{format_game_description(game_description)}

**Strategy to Implement:**
{strategy_description}

**Your Task:**
Implement this strategy in a Python block as a callable class with this signature:

```python
class Strategy:
    def __init__(self, game_description: GameDescription):
        # your implementation here
        self.game_description = game_description

    def __call__(self, history: PlayerHistory):
        \"\"\"Strategy description here\"\"\"
        # Your implementation here
        return C  # or D
```

Existing code:
{get_interface_description(game_description)}"""


def get_interface_description(game_description: GameDescription) -> str:
    """Get description of the PlayerHistory interface."""
    return f"""from dataclasses import dataclass
from enum import Enum

import numpy as np


{Actions.print_definition}


{game_description.print_definition()}


@dataclass
class PlayerHistory:
    my_actions: np.ndarray      # This player's actions
    my_payoffs: np.ndarray      # This player's payoffs
    opponent_actions: np.ndarray  # Opponents' actions [round, opponent]
    opponent_payoffs: np.ndarray  # Opponents' payoffs [round, opponent]

    @property
    def round_number(self) -> int:
        \"\"\"Current round number (number of completed rounds).\"\"\"
        return len(self.my_actions)

    @property
    def is_first_round(self) -> bool:
        \"\"\"True if this is the first round (no history yet).\"\"\"
        return self.round_number == 0

Requirements:
- You may not import and libraries."""
