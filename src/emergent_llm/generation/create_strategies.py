"""Generate LLM strategies for social dilemma games."""
import argparse
import ast
import logging
import os
import textwrap
import time

import anthropic
import openai
from emergent_llm.common.attitudes import AGGRESSIVE, COOPERATIVE, Attitude
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.collective_risk import CollectiveRiskDescription
from emergent_llm.games.public_goods import PublicGoodsDescription
from emergent_llm.generation.prompts import (create_code_user_prompt,
                                             create_strategy_user_prompt)

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

# def validate_strategy_code(code: str):
#     """Validate strategy code for safety and correctness."""

#     # Allowed AST node types for safe code execution
#     SAFE_NODES = {
#         # Core nodes
#         ast.Module, ast.ClassDef, ast.FunctionDef, ast.Return, ast.Assign,
#         ast.AnnAssign, ast.AugAssign, ast.Expr, ast.Pass,

#         # Control flow
#         ast.If, ast.IfExp, ast.For, ast.While, ast.Break, ast.Continue,

#         # Operators
#         ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare,
#         ast.And, ast.Or, ast.Not,
#         ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
#         ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
#         ast.Is, ast.IsNot, ast.In, ast.NotIn,

#         # Data structures
#         ast.List, ast.Tuple, ast.Dict, ast.Set,
#         ast.ListComp, ast.DictComp, ast.SetComp,

#         # Variables and attributes
#         ast.Name, ast.Attribute, ast.Subscript, ast.Slice,
#         ast.Load, ast.Store, ast.Del,

#         # Literals
#         ast.Constant, ast.Num, ast.Str, ast.Bytes,

#         # Function calls (will be validated separately)
#         ast.Call,

#         # Arguments
#         ast.arguments, ast.arg, ast.keyword,
#     }

#     # Allowed function calls (whitelist approach)
#     SAFE_FUNCTIONS = {
#         'len', 'max', 'min', 'sum', 'abs', 'round', 'int', 'float', 'bool',
#         'list', 'tuple', 'dict', 'set', 'str',
#         'range', 'enumerate', 'zip',
#     }

#     # Allowed numpy functions
#     SAFE_NUMPY_FUNCTIONS = {
#         'random', 'mean', 'std', 'sum', 'max', 'min', 'argmax', 'argmin',
#         'where', 'any', 'all', 'count_nonzero',
#     }

#     # Dangerous patterns to explicitly block
#     DANGEROUS_PATTERNS = [
#         '__', 'import', 'exec', 'eval', 'compile', 'open', 'file',
#         'input', 'raw_input', 'globals', 'locals', 'vars', 'dir',
#         'getattr', 'setattr', 'delattr', 'hasattr',
#     ]

#     def is_safe_node(node):
#         """Check if AST node is safe."""
#         if type(node) not in SAFE_NODES:
#             raise ValueError(f"Unsafe node type: {type(node).__name__}")

#         # Special validation for function calls
#         if isinstance(node, ast.Call):
#             if isinstance(node.func, ast.Name):
#                 if node.func.id not in SAFE_FUNCTIONS:
#                     raise ValueError(f"Unsafe function call: {node.func.id}")
#             elif isinstance(node.func, ast.Attribute):
#                 # Allow numpy functions like np.random.random()
#                 if isinstance(node.func.value, ast.Name) and node.func.value.id == 'np':
#                     if node.func.attr not in SAFE_NUMPY_FUNCTIONS:
#                         raise ValueError(f"Unsafe numpy function: np.{node.func.attr}")
#                 else:
#                     raise ValueError(f"Unsafe attribute call: {ast.unparse(node.func)}")
#             else:
#                 raise ValueError(f"Complex function call not allowed: {ast.unparse(node.func)}")

#         # Check for dangerous patterns in names
#         if isinstance(node, ast.Name):
#             for pattern in DANGEROUS_PATTERNS:
#                 if pattern in node.id.lower():
#                     raise ValueError(f"Dangerous pattern '{pattern}' in name: {node.id}")

#         # Check for dangerous patterns in attributes
#         if isinstance(node, ast.Attribute):
#             for pattern in DANGEROUS_PATTERNS:
#                 if pattern in node.attr.lower():
#                     raise ValueError(f"Dangerous pattern '{pattern}' in attribute: {node.attr}")

#         # Recursively check child nodes
#         for child in ast.iter_child_nodes(node):
#             is_safe_node(child)

#     try:
#         # Check for dangerous patterns in the raw code
#         code_lower = code.lower()
#         for pattern in DANGEROUS_PATTERNS:
#             if pattern in code_lower:
#                 raise ValueError(f"Dangerous pattern found in code: {pattern}")

#         # Parse the code
#         tree = ast.parse(code)

#         # Must be exactly one class definition
#         if len(tree.body) != 1 or not isinstance(tree.body[0], ast.ClassDef):
#             raise ValueError("Code must contain exactly one class definition")

#         class_def = tree.body[0]

#         # Check class name
#         if not class_def.name.startswith('Strategy'):
#             raise ValueError(f"Class must be named 'Strategy*', got '{class_def.name}'")

#         # Must have __init__ and __call__ methods
#         methods = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
#         method_names = [method.name for method in methods]

#         if '__init__' not in method_names:
#             raise ValueError("Strategy class must have __init__ method")
#         if '__call__' not in method_names:
#             raise ValueError("Strategy class must have __call__ method")

#         # Validate method signatures
#         for method in methods:
#             if method.name == '__init__':
#                 args = [arg.arg for arg in method.args.args]
#                 if args != ['self', 'game_description']:
#                     raise ValueError(f"__init__ signature must be (self, game_description), got {args}")
#             elif method.name == '__call__':
#                 args = [arg.arg for arg in method.args.args]
#                 if args != ['self', 'history']:
#                     raise ValueError(f"__call__ signature must be (self, history), got {args}")

#         # Check for unsafe constructs
#         is_safe_node(class_def)

#         logger.info("Code validation passed")

#     except SyntaxError as e:
#         raise ValueError(f"Syntax error in generated code: {e}")
#     except Exception as e:
#         raise ValueError(f"Code validation failed: {e}")


def validate_strategy_code(code: str):
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


class TestClient:
    pass

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
            elif isinstance(client, TestClient):
                return "Cooperate, then do what the majority did, randomly breaking ties."
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

    # Extract class definition from generated code
    tree = ast.parse(code)
    class_def = tree.body[0]

    # Rename class to be unique
    class_name = f"Strategy_{attitude.name}_{n}"
    class_def.name = class_name

    # # Add docstring with strategy description
    # docstring = f'"""{description.strip()}"""'
    # docstring_node = ast.Expr(value=ast.Constant(value=description.strip()))
    # class_def.body.insert(0, docstring_node)

    # Add game description as class attribute
    game_desc_assignment = ast.Assign(
        targets=[ast.Name(id='game_description', ctx=ast.Store())],
        value=ast.Constant(value=game_description.to_dict())
    )
    class_def.body.insert(1, game_desc_assignment)

    # Convert back to source code
    return ast.unparse(tree)


def create_single_strategy(client: openai.OpenAI | anthropic.Anthropic,
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
from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.history import PlayerHistory
import numpy as np

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
