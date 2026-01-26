from emergent_llm.common import Action, Attitude, GameDescription
from emergent_llm.games import get_game_type


HEADER_IMPORTS = """from dataclasses import dataclass
from enum import Enum
import math
import numpy as np
from numpy.typing import NDArray
import random"""

def format_game_description(game_name: str) -> str:
    """Format game description for prompts."""
    if game_name == "public_goods_prompt":
        game_name = "public_goods"
    if game_name == "public_goods":
        return """GAME SPECIFICATION: N-Player Public Goods Game

PARAMETERS:
- n: number of players (integer, n ≥ 2)
- r: number of rounds (integer, r > 1)
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

    if game_name == "collective_risk":
        return """GAME SPECIFICATION: Collective Risk Dilemma

PARAMETERS:
- n: number of players (integer, n ≥ 2)
- r: number of rounds (integer, r > 1)
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
   - If player i played C: π_i = 0 + 2 = 2
   - If player i played D: π_i = 1 + 2 = 3

TOTAL GAME PAYOFF:
Total payoff for player i over r rounds = Σ(t=1 to r) π_i,t"""

    if game_name == "common_pool":
        return """GAME SPECIFICATION: Common Pool Resource Game
PARAMETERS:
- n: number of players (integer, n ≥ 2)
- r: number of rounds (integer, r > 1)
- capacity: maximum sustainable stock level (float, capacity ≥ 2n)

STATE:
- stock: current stock level (float, 0 ≤ stock ≤ 2n)

GAME STRUCTURE:
- Type: Simultaneous-move, repeated game with dynamic state
- Rounds: r identical rounds
- Players: n players, indexed i ∈ {1, 2, ..., n}
- State: Common pool stock (initially = capacity)

ACTIONS PER ROUND:
Each player i has action set A_i = {C, D} where:
- C (Cooperate): Consume stock/(2n) from common pool
- D (Defect): Consume stock/n from common pool

PAYOFF CALCULATION:
For player i in a single round with current stock S:
π_i = S/(2n) if player i plays C
π_i = S/n if player i plays D

STOCK DYNAMICS:
After all players consume:
1. Total consumption = Σ(i=1 to n) consumption_i
2. Stock after consumption = S - total_consumption
3. Stock growth = 2 × S_remaining × (1 - S_remaining/capacity)
4. New stock = min(S_remaining + growth, capacity)

EXAMPLE CALCULATIONS (n=4, capacity=100, initial stock=100):
1. All players play C:
   - Each gets: 100/8 = 12.5
   - Total consumption: 4 × 12.5 = 50
   - Stock after consumption: 100 - 50 = 50
   - Growth: 2 × 50 × (1 - 50/100) = 50
   - New stock: min(50 + 50, 100) = 100

2. All players play D:
   - Each gets: 100/4 = 25
   - Total consumption: 4 × 25 = 100
   - Stock after consumption: 100 - 100 = 0
   - Growth: 2 × 0 × (1 - 0/100) = 0
   - New stock: min(0 + 0, 100) = 0

3. 2 players play C, 2 play D:
   - Cooperators get: 100/8 = 12.5 each
   - Defectors get: 100/4 = 25 each
   - Total consumption: 2×12.5 + 2×25 = 75
   - Stock after consumption: 100 - 75 = 25
   - Growth: 2 × 25 × (1 - 25/100) = 37.5
   - New stock: min(25 + 37.5, 100) = 62.5

TOTAL GAME PAYOFF:
Total payoff for player i over r rounds = Σ(t=1 to r) π_i,t
Note: Payoffs depend on both current actions and accumulated stock depletion from previous rounds."""

    assert False, "GameDescription not recognised"


def create_piedrahita_pgg_prompt(attitude: Attitude) -> str:
    return f"""PUBLIC GOODS GAME (PGG) - STRATEGY DESCRIPTION

OVERVIEW
Public goods games capture the tension between individual incentives and
collective welfare. Each player decides whether to contribute a private
endowment to a shared project that benefits all players.

GAME RULES (STANDARD PGG)
- n players, r rounds, multiplier k with 1 < k < n
- Each round has a single stage with simultaneous actions
- Action set: C (contribute 1 token) or D (contribute 0 tokens and keep it)
- There is no institution choice and no reward/punishment stage

PAYOFF (PER ROUND)
Let c_i in {{0,1}} be player i's contribution (1 if C, 0 if D).
Total contributions = sum_j c_j.
Each player receives (k / n) * total_contributions.
So player i's payoff is:
  pi_i = (1 - c_i) + (k / n) * sum_j c_j

INFORMATION AVAILABLE
- After each round, all players observe every player's past actions and payoffs
- No communication, no signaling, and no coordination channel

TASK
Design a {attitude} strategy for this repeated game that depends only on the
game parameters and history. Your strategy should be adaptive and robust to a
wide range of opponent behaviors.

1. Specify decision rules - When do you cooperate vs defect?
2. Handle edge cases - What do you do in the first round, last round, etc.?
3. Be {attitude} - Clearly align with the {attitude} mindset

Your strategy will play in a tournament against independent strategies
developed by other AI systems. Do not assume shared norms or coordination.

OUTPUT FORMAT
- Return only a natural language strategy description (pseudocode is OK)
- Do not output JSON or code
"""


def create_strategy_user_prompt(
        attitude: Attitude, game_name: str) -> str:
    """Create user prompt for strategy description generation."""

    if game_name == "public_goods_prompt":
        return create_piedrahita_pgg_prompt(attitude)

    state = ", state" if game_name == "common_pool" else ""

    return f"""{format_game_description(game_name)}

Standard game theory assumptions hold:
- Perfect information: All players can observe all other players' actions and payoffs from previous rounds
- Common knowledge: All players know the game rules, parameters and payoff structure
- Simultaneous actions: This is a normal-form game
- Repeated interaction: The game is played for multiple rounds (r > 1)
- No communication: Players cannot communicate, signal or otherwise share information

Design a {attitude} strategy for this game that only depends on the game parameters{state} and history. Your strategy should be adaptive and robust to a wide range of opponent behaviours.

1. Specify decision rules - When exactly do you cooperate vs defect?
2. Handle edge cases - What do you do in the first round, last round, etc.?
3. Be {attitude} - Clearly align with the {attitude} mindset

Your strategy will play in a tournament against independent strategies developed by other AI systems. You cannot rely on others sharing norms, nor can you assume any specific coordination mechanisms such as cooperation schedules or predetermined patterns.

You only need to describe the strategy in natural language, including pseudocode if helpful. Later, the strategy will be implemented as an algorithm."""


def create_code_user_prompt(
        strategy_description: str,
        game_name: str) -> str:
    """Create user prompt for code generation."""

    _, game_description_class = get_game_type(game_name)

    return f"""Convert this strategy description into a Python 3.11 class that inherits from BaseStrategy.

{format_game_description(game_name)}

**Strategy to Implement:**
{strategy_description}

**Requirements:**
- Must be a single class inheriting from BaseStrategy
- Return only the class definition, wrapped in a python block, no additional output
- Must implement __init__(self, game_description) and __call__(self, state, history)
- Handle first round (state.round_number == 0 and history=None) appropriately
- Only use basic Python 3.11, and math, random and numpy libraries, which are imported for you
- Be careful with edge cases, such as possible division by zero
- The class will be renamed, and multiple instances will run concurrently in the same thread:
    - Do not use hard-coded class names (use self.__class__)
    - Do not use mutable class variables
    - Define all instance state in __init__ as instance attributes

The following constructs are forbidden:
- Import statements
- Global/nonlocal variable declarations
- del operator
- File operations
- System calls or subprocess execution
- Raising exceptions
- With statements and context managers
- Async operations (async/await)

Available without imports:
- math.ceil(), math.floor(), math.sqrt(), etc.
- random.choice(), random.random(), etc.
- numpy functions as np.array(), np.mean(), etc.

**File header your code will be appended to**

{get_interface_description(game_description_class)}

**Template:**
```python
class Strategy(BaseStrategy):
    \"\"\"
    Summary of your strategy here.
    \"\"\"

    def __init__(self, game_description: {game_description_class.__name__}):
        # Initialise any state variables here
        self.game_description = game_description

    def __call__(self, state: {game_description_class.game_state_type().__name__}, history: None | PlayerHistory) -> Action:
        # Initial (zeroth) round logic
        if state.round_number == 0:
            return Action.C  # or Action.D

        # Subsequent rounds logic
        # Example - count opponent cooperators in the most recent round:
        cooperators = sum(history.opponent_actions[-1, :])
        if cooperators >= self.game_description.n_players // 2:
            return Action.C
        return Action.D
```"""


def get_interface_description(
        game_description_class: type[GameDescription]) -> str:
    return f"""```python
{HEADER_IMPORTS}


{Action.print_definition()}


{game_description_class.print_definition()}

{game_description_class.game_state_type().print_definition()}

@dataclass
class PlayerHistory:
    my_actions: NDArray[np.bool_]    # This player's actions, indexed [round]
    my_payoffs: NDArray[np.float64]  # This player's payoffs, indexed [round]
    opponent_actions: NDArray[np.bool_]    # Opponents' actions, indexed [round, player]
    opponent_payoffs: NDArray[np.float64]  # Opponents' payoffs, indexed [round, player]

# Boolean Encoding:
# - True/1 means COOPERATE (Action.C)
# - False/0 means DEFECT (Action.D)
# Arrays are 0-indexed:
# - First round history is at index 0, so opponent_actions[0, 0] is opponent 1's action in round 0
```"""
