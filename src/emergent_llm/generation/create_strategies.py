"""Generate LLM strategies for social dilemma games."""

import argparse
import ast
import logging
import os
import textwrap
import time
from typing import Union

import anthropic
import openai

from emergent_llm.common.attitudes import Attitude
from emergent_llm.games.game_description import GameDescription, PublicGoodsDescription, CollectiveRiskDescription

# Configure logging
logging.basicConfig(
    filename="create_strategies.log",
    filemode="w",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Reduce noise from HTTP clients
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.WARNING)


def generate_strategy_description(client: Union[openai.OpenAI, anthropic.Anthropic],
                                 attitude: Attitude,
                                 game_description: GameDescription,
                                 temperature: float = 0.7) -> str:
    """Generate natural language strategy description."""

    system_prompt = "You are an AI assistant with expertise in strategic thinking."
    user_prompt = create_strategy_user_prompt(attitude, game_description)

    logger.info(f"Generating {attitude.value} strategy description")
    logger.info(f"System prompt: {system_prompt[:200]}...")
    logger.info(f"User prompt: {user_prompt[:200]}...")

    response = get_llm_response(client, system_prompt, user_prompt, temperature)
    logger.info(f"Strategy description: {response[:200]}...")

    return response


def generate_strategy_code(client: Union[openai.OpenAI, anthropic.Anthropic],
                          strategy_description: str,
                          game_description: GameDescription) -> str:
    """Generate Python code from strategy description."""

    system_prompt = "You are an expert Python programmer implementing game theory strategies."
    user_prompt = create_code_user_prompt(strategy_description, game_description)

    logger.info("Generating strategy code")
    logger.info(f"Code user prompt: {user_prompt[:200]}...")

    response = get_llm_response(client, system_prompt, user_prompt, temperature=0.0)

    # Clean and validate the code
    code = clean_generated_code(response)
    validate_strategy_code(code, game_description)

    logger.info(f"Generated code: {code[:200]}...")
    return code


def create_strategy_user_prompt(attitude: Attitude, game_description: GameDescription) -> str:
    """Create user prompt for strategy description generation."""

    game_info = format_game_description(game_description)

    return f"""{game_info}

Design a {attitude.lower()} strategy for this game. Your strategy should:

1. **Specify decision rules** - When exactly do you cooperate vs defect?
2. **Consider adaptation** - How do you respond to others' behavior over time?
3. **Handle edge cases** - What do you do in the first round, last rounds, etc.?
4. **Be {attitude.lower()}** - Clearly align with the {attitude.lower()} mindset

Provide a detailed strategy description with concrete decision rules. Include some pseudocode or logical steps if helpful."""


def create_code_user_prompt(strategy_description: str, game_description: GameDescription) -> str:
    """Create user prompt for code generation."""

    game_info = format_game_description(game_description)
    interface_info = get_interface_description()

    return f"""Your task is to convert a natural language strategy description into clean, efficient Python code.

Focus on:
- Correct logic implementation
- Proper state management using self attributes
- Handling edge cases (first round, empty history)
- Clean, readable code structure

{game_info}

{interface_info}

**Strategy to Implement:**
{strategy_description}

**Your Task:**
Implement this strategy as a Python function with exactly this signature:

```python
def strategy(self, history):
    # Your implementation here
    return C  # or D
```

Requirements:

Use self.variable_name to store state between rounds
Initialize state variables when history.is_first_round is True
Only return C or D (imported at module level)
Handle edge cases properly
Include brief comments for complex logic
Assume numpy and pandas have been imported as np and pd, respectively

Example pattern:

```python
def strategy(self, history):
    if history.is_first_round:
        self.cooperation_count = 0
        return C  # Initial choice

    # Your strategy logic here
    # Use history.opponent_actions, history.my_actions, etc.

    return C  # or D based on your logic
```

Implement the strategy faithfully. Only provide the Python function, no explanation."""



def format_game_description(game_description: GameDescription) -> str:
    """Format game description for prompts."""
    if isinstance(game_description, PublicGoodsDescription):
      return f"""GAME SPECIFICATION: N-Player Public Goods Game

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


def get_interface_description() -> str:
    """Get description of the PlayerHistory interface."""
    return """Available Information in history:

history.is_first_round: True if this is the first round
history.round_number: Current round (0-indexed)
history.my_actions: numpy array of your past actions [C, D, C, ...]
history.my_payoffs: numpy array of your past payoffs [1.5, 2.0, 1.0, ...]
history.opponent_actions: 2D numpy array [round][opponent] of all opponents' actions
history.opponent_payoffs: 2D numpy array [round][opponent] of all opponents' payoffs

Available Actions:

C: Cooperate
D: Defect"""


def clean_generated_code(response: str) -> str:
    """Clean LLM response to extract just the Python code."""
    # Remove code block markers
    code = response.replace("```python", "").replace("```", "").strip()

    # Fix common LLM mistakes
    replacements = {
        "Action.C": "C",
        "Action.D": "D",
        "COOPERATE": "C",
        "DEFECT": "D",
        "np.random.rand()": "np.random.random()",
        "random.rand()": "random.random()",
       }

    for old, new in replacements.items():
        code = code.replace(old, new)

    return code


def validate_strategy_code(code: str, game_description: GameDescription):
"""Validate strategy code for safety and correctness."""
    def is_safe_node(node):
        """Check if AST node is safe."""
        allowed_types = (
            ast.Return, ast.UnaryOp, ast.BoolOp, ast.BinOp, ast.FunctionDef,
            ast.If, ast.IfExp, ast.And, ast.Or, ast.Not, ast.Compare,
            ast.List, ast.Dict, ast.Tuple, ast.Constant, ast.Num, ast.Str,
            ast.Name, ast.arguments, ast.arg, ast.Expr, ast.Attribute,
            ast.Call, ast.Store, ast.Load, ast.Subscript, ast.Index, ast.Slice,
            ast.For, ast.While, ast.Pass, ast.Break, ast.Continue,
            ast.Assign, ast.AugAssign, ast.Add, ast.Sub, ast.Mult, ast.Div,
            ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq,
            ast.In, ast.NotIn, ast.Is, ast.IsNot
        )

        if not isinstance(node, allowed_types):
            raise ValueError(f"Unsafe node type: {type(node).__name__}")

        for child in ast.iter_child_nodes(node):
            is_safe_node(child)

    try:
        # Parse the code
        tree = ast.parse(code)

        # Must be exactly one function
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
            raise ValueError("Code must contain exactly one function definition")

        func = tree.body[0]

        # Check function name and signature
        if func.name != 'strategy':
            raise ValueError(f"Function must be named 'strategy', got '{func.name}'")

        args = [arg.arg for arg in func.args.args]
        if args != ['self', 'history']:
            raise ValueError(f"Function signature must be (self, history), got {args}")

        # Check for unsafe constructs
        is_safe_node(func)

        logger.info("Code validation passed")

    except SyntaxError as e:
        raise ValueError(f"Syntax error in generated code: {e}")
    except Exception as e:
        raise ValueError(f"Code validation failed: {e}")


def get_llm_response(client: Union[openai.OpenAI, anthropic.Anthropic],
                     system_prompt: str,
                     user_prompt: str,
                     temperature: float) -> str:
    """Get response from LLM client."""
    if isinstance(client, openai.OpenAI):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=1500
        )
        return response.choices[0].message.content

    elif isinstance(client, anthropic.Anthropic):
        # Retry logic for Anthropic
        for attempt in range(3):
            try:
                response = client.messages.create(
                    model="claude-4-sonnet",
                    max_tokens=1500,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text
            except anthropic.InternalServerError:
                if attempt < 2:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise

    else:
        raise ValueError(f"Unknown client type: {type(client)}")


def format_class_comment(text: str, width: int = 78) -> str:
    """Format text as Python comments."""
    if not text:
    return ""
    wrapped = textwrap.wrap(text, width=width)
    return "\n".join("# " + line for line in wrapped)


def write_strategy_class(description: str, code: str, attitude: Attitude,
    n: int, game_description: GameDescription) -> str:
    """Write complete strategy class."""
    # Add proper indentation to the strategy method
    indented_code = "\n".join("    " + line for line in code.splitlines())

    description_comment = format_class_comment(description)

    return f"""{description_comment}
class {attitude.name}_{n}(LLMStrategyPlayer):
n = {n}
attitude = Attitude.{attitude.name}
game_type = '{game_description.class.name}'
game_description = {repr(game_description)}
{indented_code}"""


def create_single_strategy(client: Union[openai.OpenAI, anthropic.Anthropic],
                           attitude: Attitude, n: int,
                           game_description: GameDescription,
                           temperature: float) -> str:
    """Create a single strategy class."""
    print(f"Generating {attitude.name}_{n}...")

    # Step 1: Generate strategy description
    description = generate_strategy_description(client, attitude, game_description, temperature)

    # Step 2: Generate code implementation
    code = generate_strategy_code(client, description, game_description)

    # Step 3: Create complete class
    class_code = write_strategy_class(description, code, attitude, n, game_description)

    return class_code


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument("--llm", choices=["openai", "anthropic"], required=True,
                       help="LLM provider to use")
    parser.add_argument("--n", type=int, required=True,
                       help="Number of strategies per attitude to generate")
    parser.add_argument("--output", type=str, required=True,
                       help="Output file name (without .py extension)")
    parser.add_argument("--temperature", type=float, default=0.7,
                       help="Temperature for strategy generation")

    # Game parameters
    parser.add_argument("--game", choices=["public_goods", "collective_risk"],
                       default="public_goods", help="Game type")
    parser.add_argument("--n_players", type=int, default=6, help="Number of players")
    parser.add_argument("--n_rounds", type=int, default=20, help="Number of rounds")
    parser.add_argument("--k", type=float, default=2.0, help="Game parameter k")
    parser.add_argument("--m", type=int, default=3,
                       help="Threshold parameter for collective risk")

    return parser.parse_args()

def create_game_description(args: argparse.Namespace) -> GameDescription:
    """Create game description from arguments."""
    if args.game == "public_goods":
        return PublicGoodsDescription(
            n_players=args.n_players,
            n_rounds=args.n_rounds,
            k=args.k
        )
    elif args.game == "collective_risk":
        return CollectiveRiskDescription(
            n_players=args.n_players,
            n_rounds=args.n_rounds,
            m=args.m,
            k=args.k
        )
    else:
        raise ValueError(f"Unknown game: {args.game}")


def main():
    """Main function."""
    args = parse_arguments()
    # Setup LLM client
    if args.llm == "openai":
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    else:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Create game description
    game_description = create_game_description(args)

    # Check if output file exists
    output_file = f"{args.output}.py"
    if os.path.exists(output_file):
        raise FileExistsError(f"{output_file} already exists")

    # Write file header
    with open(output_file, "w", encoding="utf8") as f:
        f.write("""from emergent_llm.players import LLMStrategyPlayer
from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.actions import C, D
import numpy as np""")

    # Generate strategies
    attitudes = [Attitude.COOPERATIVE, Attitude.AGGRESSIVE, Attitude.NEUTRAL]

    with open(output_file, "a", encoding="utf8") as f:
        for attitude in attitudes:
            for i in range(1, args.n + 1):
                try:
                    strategy_class = create_single_strategy(
                        client, attitude, i, game_description, args.temperature
                    )
                    f.write("\n\n\n" + strategy_class)
                    f.flush()  # Save progress

                except Exception as e:
                    logger.error(f"Failed to generate {attitude.name}_{i}: {e}")
                    print(f"Error generating {attitude.name}_{i}: {e}")
                    continue

    print(f"Strategies written to {output_file}")

if name == "main":
    main()
