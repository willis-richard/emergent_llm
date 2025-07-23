"""Generate LLM strategies for social dilemma games."""
import argparse
import ast
import importlib.util
import inspect
import logging
import os
import time
import numpy as np

import anthropic
import openai
from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.attitudes import AGGRESSIVE, COOPERATIVE, Attitude
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.collective_risk import CollectiveRiskDescription
from emergent_llm.games.public_goods import PublicGoodsDescription
from emergent_llm.generation.prompts import (create_code_user_prompt,
                                             create_strategy_user_prompt)
from emergent_llm.players.base_player import BaseStrategy

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

def generate_strategy_description(client: openai.OpenAI | anthropic.Anthropic,
                                 attitude: Attitude,
                                 game_description: GameDescription,
                                 temperature: float = 0.7) -> str:
    """Generate natural language strategy description."""

    system_prompt = "You are an AI assistant with expertise in strategic thinking."
    user_prompt = create_strategy_user_prompt(attitude, game_description)

    logger.info(f"Generating {attitude.value} strategy description")
    logger.info(f"System prompt: {system_prompt}")
    logger.info(f"User prompt: {user_prompt}")

    response = get_llm_response(client, system_prompt, user_prompt, temperature)
    logger.info(f"Strategy description: {response}")

    return response


def generate_strategy_code(client: openai.OpenAI | anthropic.Anthropic,
                           strategy_description: str,
                           game_description: GameDescription) -> str:
    """Generate Python code from strategy description."""

    system_prompt = "You are an expert Python programmer implementing game theory strategies."
    user_prompt = create_code_user_prompt(strategy_description, game_description)

    logger.info("Generating strategy code")
    logger.info(f"Code user prompt: {user_prompt}")

    response = get_llm_response(client, system_prompt, user_prompt, temperature=0.0)
    logger.info(f"Generated code: {response}")

    # Clean and validate the code
    code = clean_generated_code(response)
    validate_strategy_code(code)
    return code


def clean_generated_code(response: str) -> str:
    """Clean LLM response to extract just the Python code."""
    import re

    # Extract from code blocks with proper multiline matching
    code_block_pattern = r'```(?:python)?\s*\n(.*?)```'
    code_blocks = re.findall(code_block_pattern, response, re.DOTALL)

    if code_blocks:
        # Use the largest code block found (most likely to be the complete class)
        code = max(code_blocks, key=len).strip()
    else:
        # Fallback: look for class definition without code blocks
        class_pattern = r'(class\s+\w+.*?)(?=\n\n|\Z)'
        class_matches = re.findall(class_pattern, response, re.DOTALL)
        if class_matches:
            code = class_matches[0].strip()
        else:
            raise ValueError("No Python code block or class definition found in response")

    # Remove any remaining markdown artifacts
    code = re.sub(r'^```.*$', '', code, flags=re.MULTILINE)
    code = code.strip()

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


def validate_strategy_code(code: str):
    """Validate strategy code for safety and correctness."""
    def is_safe_node(node):
        """Check if AST node is safe."""
        # yapf: disable
        allowed_types = (
            ast.Return, ast.UnaryOp, ast.BoolOp, ast.BinOp, ast.ClassDef, ast.FunctionDef,
            ast.If, ast.IfExp, ast.And, ast.Or, ast.Not, ast.Eq,
            ast.BitOr, ast.BitAnd, ast.BitXor, ast.Invert,
            ast.List, ast.Dict, ast.Tuple, ast.Num, ast.Str, ast.Constant, ast.Set,
            ast.arg, ast.Name, ast.arguments, ast.keyword, ast.Expr, ast.Attribute,
            ast.Call, ast.Store, ast.Load, ast.Subscript, ast.Index, ast.Slice,
            ast.GeneratorExp, ast.comprehension, ast.ListComp, ast.Lambda, ast.DictComp,
            ast.For, ast.While, ast.Pass, ast.Break, ast.Continue,
            ast.Assign, ast.AugAssign, ast.AnnAssign,
            ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq,
            ast.In, ast.NotIn, ast.Is, ast.IsNot, ast.Compare, ast.USub,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Pow, ast.Mod,
        )
        # yapf: enable

        # Dangerous constructs
        dangerous_types = (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal,
                          ast.Delete, ast.With, ast.AsyncWith, ast.Try, ast.Raise)

        if isinstance(node, dangerous_types):
            raise ValueError(f"Dangerous node type: {type(node).__name__}\nnode:\n{ast.unparse(node)}")

        if not isinstance(node, allowed_types):
            raise ValueError(f"Unsafe node type: {type(node).__name__}\nnode:\n{ast.unparse(node)}")

        # Check for dangerous function calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                dangerous_funcs = {'eval', 'exec', 'compile', 'open', '__import__', 'globals', 'locals', 'vars', 'dir'}
                if node.func.id in dangerous_funcs:
                    raise ValueError(f"Dangerous function call: {node.func.id}\nnode:\n{ast.unparse(node)}")

        for child in ast.iter_child_nodes(node):
            is_safe_node(child)

    try:
        # Parse the code
        tree = ast.parse(code)

        # Must be exactly one class
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.ClassDef):
            raise ValueError("Code must contain exactly one class definition")

        class_def = tree.body[0]

        # Check class structure
        required_methods = {'__init__', '__call__'}
        found_methods = set()

        for node in class_def.body:
            if isinstance(node, ast.FunctionDef):
                found_methods.add(node.name)

                # Validate __init__ method
                if node.name == '__init__':
                    args = [arg.arg for arg in node.args.args]
                    if args != ['self', 'game_description']:
                        raise ValueError("__init__ must have signature (self, game_description)")

                # Validate __call__ method
                elif node.name == '__call__':
                    args = [arg.arg for arg in node.args.args]
                    if args != ['self', 'history']:
                        raise ValueError("__call__ must have signature (self, history)")

        # Check required methods exist
        missing_methods = required_methods - found_methods
        if missing_methods:
            raise ValueError(f"Missing required methods: {missing_methods}")

        # Check for unsafe constructs
        is_safe_node(class_def)

        logger.info("Class validation passed")

    except SyntaxError as e:
        raise ValueError(f"Syntax error in generated code: {e}") from e
    except Exception as e:
        raise ValueError(f"Code validation failed: {e}") from e


def test_generated_strategy(class_code: str, game_description: GameDescription):
    """Test the generated strategy by actually running it in games."""
    import tempfile

    from emergent_llm.common.attitudes import Attitude
    from emergent_llm.players import LLMPlayer, SimplePlayer

    # Create a temporary module to load the strategy
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Write necessary imports and the class
        f.write("""
from emergent_llm.players.base_player import BaseStrategy
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription
from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.history import PlayerHistory
import numpy as np
from numpy.typing import NDArray
import random

""")
        f.write(class_code)
        temp_file = f.name

    try:
        # Load the temporary module
        spec = importlib.util.spec_from_file_location("temp_strategy", temp_file)
        temp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(temp_module)

        # Find the strategy class
        strategy_classes = [cls for name, cls in inspect.getmembers(temp_module)
                          if inspect.isclass(cls) and issubclass(cls, BaseStrategy) and cls != BaseStrategy]

        if not strategy_classes:
            raise ValueError("No strategy class found in generated code")

        assert len(strategy_classes) == 1, "More than one strategy class defined"
        strategy_class = strategy_classes[0]

        # Determine game type and create test games
        if isinstance(game_description, PublicGoodsDescription):
            from emergent_llm.games.public_goods import PublicGoodsGame
            game_class = PublicGoodsGame
        elif isinstance(game_description, CollectiveRiskDescription):
            from emergent_llm.games.collective_risk import CollectiveRiskGame
            game_class = CollectiveRiskGame
        else:
            raise ValueError(f"Unknown game description type: {type(game_description)}")

        # Create test player
        player = LLMPlayer("test_player", Attitude.COOPERATIVE, game_description, strategy_class)

        # Test against different opponent types
        test_mixtures = [
            [SimplePlayer(f"cooperator_{i}", lambda: C) for i in range(game_description.n_players - 1)],
            [SimplePlayer(f"defector_{i}", lambda: D) for i in range(game_description.n_players - 1)],
            [SimplePlayer(f"random_{i}", lambda: np.random.choice([C, D])) for i in range(game_description.n_players - 1)],
        ]

        for mixture in test_mixtures:
            players = [player] + mixture
            game = game_class(players, game_description)

            # This will raise an exception if the strategy fails
            result = game.play_game()

    finally:
        # Clean up temp file
        os.unlink(temp_file)


def get_llm_response(client: openai.OpenAI | anthropic.Anthropic,
                     system_prompt: str,
                     user_prompt: str,
                     temperature: float) -> str:
    """Get response from LLM client."""
    for attempt in range(3):
        try:
            if isinstance(client, openai.OpenAI):
                response = client.chat.completions.create(
                    model="gpt-4.1-nano",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=1500
                )
                return response.choices[0].message.content

            elif isinstance(client, anthropic.Anthropic):
                response = client.messages.create(
                    model="claude-4-sonnet",
                    max_tokens=1500,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text
        except (openai.InternalServerError, anthropic.InternalServerError):
            if attempt < 2:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise

    else:
        raise ValueError(f"Unknown client type: {type(client)}")


def write_strategy_class(description: str, code: str, attitude: Attitude, n: int,
                        game_description: GameDescription) -> str:
    """Create a complete strategy class with proper naming and documentation."""

    # Parse and modify the class
    tree = ast.parse(code)
    class_def = tree.body[0]

    # Rename class to be unique
    class_name = f"Strategy_{attitude.name}_{n}"
    class_def.name = class_name

    # # Add docstring to __call__ method if it doesn't exist
    # for node in class_def.body:
    #     if isinstance(node, ast.FunctionDef) and node.name == '__call__':
    #         if (not node.body or
    #             not isinstance(node.body[0], ast.Expr) or
    #             not isinstance(node.body[0].value, ast.Constant)):
    #             # Add docstring
    #             docstring = ast.Expr(value=ast.Constant(value=description.strip()))
    #             node.body.insert(0, docstring)
    #         break

    # Convert back to source code
    return ast.unparse(tree)


def create_single_strategy(client: openai.OpenAI | anthropic.Anthropic,
                           attitude: Attitude, n: int,
                           game_description: GameDescription,
                           temperature: float,
                           max_retries: int = 3) -> str:
    """Create a single strategy class with retry logic."""

    for attempt in range(max_retries):
        try:
            print(f"Generating {attitude.name}_{n} (attempt {attempt + 1})...")

            # Step 1: Generate strategy description
            description = generate_strategy_description(client, attitude, game_description, temperature)

            # Step 2: Generate code implementation
            code = generate_strategy_code(client, description, game_description)

            # Step 3: Create complete class
            class_code = write_strategy_class(description, code, attitude, n, game_description)

            # Step 4: Test the generated strategy
            test_generated_strategy(class_code, game_description)

            return class_code

        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for {attitude.name}_{n}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)  # Brief pause before retry


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate LLM strategies for social dilemma games"
    )
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
            n_players=6,
            n_rounds=20,
            k=2.0
        )
    elif args.game == "collective_risk":
        return CollectiveRiskDescription(
            n_players=6,
            n_rounds=20,
            m=3,
            k=2.0,
        )
    else:
        raise ValueError(f"Unknown game: {args.game}")


def main():
    """Main function."""
    args = parse_arguments()

    # Setup LLM client
    if args.llm == "openai":
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    elif args.llm == "anthropic":
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    else:
        raise ValueError(f"Unknown client {args.llm}")

    # Create game description
    game_description = create_game_description(args)

    # Check if output file exists
    output_file = f"{args.output}.py"
    if os.path.exists(output_file):
        raise FileExistsError(f"{output_file} already exists")

    # Write file header
    header = '''"""
Generated LLM strategies for social dilemma games.

This file contains strategy classes generated by LLMs for game theory experiments.
Each strategy is a callable class that implements a specific approach to the game.
"""

from emergent_llm.players.base_player import BaseStrategy
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription
from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.history import PlayerHistory
import numpy as np
from numpy.typing import NDArray
import random

'''

    with open(output_file, "w", encoding="utf8") as f:
        f.write(header)

    # Generate strategies
    with open(output_file, "a", encoding="utf8") as f:
        for attitude in [COOPERATIVE, AGGRESSIVE]:
            for i in range(1, args.n + 1):
                try:
                    strategy_class = create_single_strategy(
                        client, attitude, i, game_description, args.temperature
                    )
                    f.write("\n\n" + strategy_class)
                    f.flush()  # Save progress
                    print(f"✓ Generated {attitude.name}_{i}")

                except Exception as e:
                    logger.error(f"Failed to generate {attitude.name}_{i}: {e}")
                    print(f"✗ Error generating {attitude.name}_{i}: {e}")
                    continue

    print(f"\nStrategies written to {output_file}")


if __name__ == "__main__":
    main()
