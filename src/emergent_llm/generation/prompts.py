from emergent_llm.common.actions import Action
from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.public_goods import PublicGoodsDescription
from emergent_llm.games.collective_risk import CollectiveRiskDescription


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
    if isinstance(game_description, CollectiveRiskDescription):
        return """GAME SPECIFICATION: Collective Risk Dilemma

PARAMETERS:
- n: number of players (integer, n ≥ 2)
- r: number of rounds (integer, r ≥ 1)
- m: minimum cooperators needed (integer, 1 < m < n)
- k: reward if threshold met factor (float, k > 1)

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
- If fewer than m players cooperate: π_i = (1 - c_i)
- If m or more players cooperate: π_i = (1 - c_i) + k

where:
- c_i = 1 if player i plays C, c_i = 0 if player i plays D

PAYOFF MATRIX INTERPRETATION:
- Private payoff from keeping: 1
- Reward of risk averted: k

EXAMPLE CALCULATIONS (n=6, m=3, k=2):
1. All players play D: π_i = 1 + 0 = 1 for all i
2. All players play C: π_i = 0 + 2 = 2 for all i
3. 3 players play C, 3 play D:
   - If player i played C: π_i = 0 + 2 = 3
   - If player i played D: π_i = 1 + 2 = 4

TOTAL GAME PAYOFF:
Total payoff for player i over r rounds = Σ(t=1 to r) π_i,t"""

    assert False, "GameDescription not recognised"


def create_strategy_user_prompt(attitude: Attitude, game_description: GameDescription) -> str:
    """Create user prompt for strategy description generation."""

    return f"""{format_game_description(game_description)}

Design a {attitude} strategy for this game. Your strategy should:

1. **Specify decision rules** - When exactly do you cooperate vs defect?
2. **Consider adaptation** - How do you respond to others' behavior over time?
3. **Handle edge cases** - What do you do in the first round, last rounds, etc.?
4. **Be {attitude}** - Clearly align with the {attitude} mindset

Provide a detailed strategy description with concrete decision rules. Include pseudocode or logical steps if helpful."""


def create_code_user_prompt(strategy_description: str, game_description: GameDescription) -> str:
    """Create user prompt for code generation."""

    return f"""Convert this strategy description into a Python class that inherits from BaseStrategy.

{format_game_description(game_description)}

**Strategy to Implement:**
{strategy_description}

**Requirements:**
- Must be a single class inheriting from BaseStrategy
- Must implement __init__(self, game_description) and __call__(self, history)
- Return only the class definition, no explanatory text
- Use only numpy and random operations, and basic Python (no imports allowed)
- Handle first round (history=None) appropriately

**Template:**
```python
class Strategy(BaseStrategy):
    def __init__(self, game_description: {game_description.__class__.__name__}):
        # Initialize any state variables here
        self.game_description = game_description

    def __call__(self, history: None | PlayerHistory) -> Action:
        \"\"\"Your strategy description here\"\"\"
        if history is None:
            # First round logic
            return Action.C  # or Action.D

        # Subsequent rounds logic using history
        return Action.C  # or Action.D

{get_interface_description(game_description)}"""


def get_interface_description(game_description: GameDescription) -> str:
    """Get description of the PlayerHistory interface."""
    return f"""from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import NDArray
import random


{Action.print_definition()}


{game_description.print_definition()}


@dataclass
class PlayerHistory:
    my_actions: NDArray[np.bool_]    # This player's actions, indexed [round]
    my_payoffs: NDArray[np.float64]  # This player's payoffs, indexed [round]
    opponent_actions: NDArray[np.bool_]    # Opponents' actions, indexed [round, player]
    opponent_payoffs: NDArray[np.float64]  # Opponents' payoffs, indexed [round, player]

    @property
    def round_number(self) -> int:
        \"\"\"Current round number (number of completed rounds).\"\"\"
        return len(self.my_actions)

Requirements:
- You may not import any libraries."""
