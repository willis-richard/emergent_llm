"""Generate LLM strategies for social dilemma games in two phases.

Phase 1: Generate strategy descriptions
Phase 2: Generate code implementations from descriptions
"""
import argparse
import ast
import importlib.util
import inspect
import logging
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path

import anthropic
import ollama
import openai
from google import genai
from google.genai import errors as genai_errors

from emergent_llm.common import COLLECTIVE, EXPLOITATIVE, Attitude, Gene
from emergent_llm.games import STANDARD_GENERATORS
from emergent_llm.generation.prompts import create_code_user_prompt, create_strategy_user_prompt
from emergent_llm.players import (
    BaseStrategy,
    Cooperator,
    Defector,
    GradualDefector,
    PeriodicDefector,
    Random,
    RandomCooperator,
    RandomDefector,
)


def setup_logging(log_file: Path) -> logging.Logger:
    """Setup logging configuration."""
    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.basicConfig(filename=str(log_file),
                        filemode="w",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Reduce noise from HTTP clients
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)

    return logger


@dataclass
class LLMConfig:
    client: openai.OpenAI | anthropic.Anthropic | ollama.Client | genai.Client
    model_name: str
    max_retries: int = 3


def parse_strategy_description_file(
        strategy_description_file: Path) -> dict[tuple[str, int], str]:
    """Parse existing strategy description file and extract existing descriptions.

    Returns dict mapping (attitude_name, n) tuple to strategy description string.
    """
    if not strategy_description_file.exists():
        return {}

    strategy_descriptions = {}

    try:
        with open(strategy_description_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the file as Python AST
        tree = ast.parse(content)

        # Extract string assignments that match our pattern
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and isinstance(
                        node.value, ast.Constant):
                    var_name = target.id

                    # Check if it matches our description variable pattern
                    match = re.match(r'description_([A-Z]+)_(\d+)', var_name)
                    if match:
                        attitude_name = match.group(1)
                        n = int(match.group(2))
                        strategy_description = node.value.value
                        strategy_descriptions[(attitude_name, n)] = strategy_description

    except Exception as e:
        logging.warning(
            f"Error parsing strategy description file {strategy_description_file}: {e}")
        return {}

    return strategy_descriptions


def parse_strategy_implementation_file(strategy_implementation_file: Path) -> set[str]:
    """Parse existing strategy file and extract implemented strategy class names.

    Returns set of class names like 'Strategy_COLLECTIVE_1'.
    """
    if not strategy_implementation_file.exists():
        print(f"WARNING: {strategy_implementation_file} not found")
        return set()

    strategy_classes = set()

    try:
        with open(strategy_implementation_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the file as Python AST
        tree = ast.parse(content)

        # Extract class definitions that match our pattern
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                if re.match(r'Strategy_[A-Z]+_\d+', class_name):
                    strategy_classes.add(class_name)

    except Exception as e:
        error_msg = f"Error parsing strategy implementations file {strategy_implementation_file}: {e}"
        logging.warning(error_msg)
        print(f"WARNING: {error_msg}")
        return set()

    return strategy_classes


def write_description_to_file(strategy_description_file: Path, attitude: Attitude,
                              n: int, strategy_description: str):
    """Append a new description using triple single quotes."""
    var_name = f"description_{attitude.name}_{n}"

    # Create description entry
    strategy_description = strategy_description.replace("'''", "\\'\\'\\'")
    description_entry = f"\n{var_name} = '''\n{strategy_description}\n'''\n"

    # Append to file
    with open(strategy_description_file, 'a', encoding='utf-8') as f:
        f.write(description_entry)


def get_missing_descriptions(existing_descriptions: dict[tuple[str, int], str],
                             attitudes: list[Attitude],
                             n_per_attitude: int) -> list[tuple[Attitude, int]]:
    """Get list of (attitude, n) tuples for missing descriptions."""
    missing = []

    for attitude in attitudes:
        for i in range(1, n_per_attitude + 1):
            key = (attitude.name, i)
            if key not in existing_descriptions:
                missing.append((attitude, i))

    return missing


def get_missing_implementations(
    existing_implementations: set[str], existing_descriptions: dict[tuple[str, int],
                                                                    str]
) -> list[tuple[str, int, str]]:
    """Get list of (attitude_name, n, description) tuples for missing implementations."""
    missing = []

    for (attitude_name, n), description in existing_descriptions.items():
        class_name = f"Strategy_{attitude_name}_{n}"
        if class_name not in existing_implementations:
            missing.append((attitude_name, n, description))

    return missing


def generate_strategy_description(config: LLMConfig,
                                  attitude: Attitude,
                                  game_name: str,
                                  logger: logging.Logger = None) -> str:
    """Generate natural language strategy description."""
    system_prompt = "You are an AI assistant with expertise in strategic thinking."
    user_prompt = create_strategy_user_prompt(attitude, game_name)

    if logger:
        logger.info(f"Generating {attitude.value} strategy description")
        logger.info(f"System prompt: {system_prompt}")
        logger.info(f"User prompt: {user_prompt}")

    response = get_llm_response(config, system_prompt, user_prompt)

    if logger:
        logger.info(f"Strategy description: {response}")

    return response


def generate_strategy_code(config: LLMConfig,
                           strategy_description: str,
                           game_name: str,
                           logger: logging.Logger = None) -> str:
    """Generate Python code from strategy description."""
    system_prompt = "You are an expert Python programmer implementing game theory strategies."
    user_prompt = create_code_user_prompt(strategy_description,
                                          game_name)

    if logger:
        logger.info("Generating strategy code")
        logger.info(f"Code user prompt: {user_prompt}")

    response = get_llm_response(config, system_prompt, user_prompt)

    if logger:
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
        if len(code_blocks) != 1:
            raise ValueError("More than one code block in response")
        code = code_blocks[0]
    else:
        # Fallback: look for class definition without code blocks
        class_pattern = r'(class\s+\w+.*?)(?=\n\n|\Z)'
        class_matches = re.findall(class_pattern, response, re.DOTALL)
        if class_matches:
            code = class_matches[0].strip()
        else:
            raise ValueError(
                "No Python code block or class definition found in response")

    # Remove any remaining markdown artifacts
    code = re.sub(r'^```.*$', '', code, flags=re.MULTILINE)
    code = code.strip()

    # Remove forbidden import statements that are already available in the environment
    forbidden_imports = [
        r'^import\s+math\s*$',  # import math
        r'^import\s+random\s*$',  # import random
        r'^import\s+numpy\s+as\s+np\s*$',  # import numpy as np
    ]

    for pattern in forbidden_imports:
        code = re.sub(pattern, '', code, flags=re.MULTILINE)

    # Fix quoted type hints - remove quotes around PlayerHistory in type annotations
    # Handle both double and single quotes
    code = re.sub(r'\b(:\s*(?:None\s*\|\s*)?)["\']PlayerHistory["\']',
                  r'\1PlayerHistory', code)

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
            ast.arg, ast.Name, ast.NamedExpr, ast.arguments, ast.keyword, ast.Expr, ast.Attribute,
            ast.Call, ast.Store, ast.Load, ast.Subscript, ast.Index, ast.Slice,
            ast.GeneratorExp, ast.comprehension, ast.ListComp, ast.Lambda, ast.DictComp, ast.SetComp,
            ast.For, ast.While, ast.Pass, ast.Break, ast.Continue,
            ast.Assign, ast.AugAssign, ast.AnnAssign,
            ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq,
            ast.In, ast.NotIn, ast.Is, ast.IsNot, ast.Compare,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Pow, ast.Mod,
            ast.UAdd, ast.USub, ast.MatMult,
            ast.Try, ast.ExceptHandler,
        )
        # yapf: enable

        # Dangerous constructs
        dangerous_types = (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal,
                           ast.Delete, ast.With, ast.AsyncWith, ast.Raise)

        dangerous_funcs = {
            'eval', 'exec', 'compile', 'open', '__import__', 'globals',
            'locals', 'vars', 'dir'
        }

        if isinstance(node, dangerous_types):
            raise ValueError(
                f"Dangerous node type: {type(node).__name__}\nnode:\n{ast.unparse(node)}"
            )

        if not isinstance(node, allowed_types):
            raise ValueError(
                f"Unsafe node type: {type(node).__name__}\nnode:\n{ast.unparse(node)}"
            )

        # Check for dangerous function calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in dangerous_funcs:
                    raise ValueError(
                        f"Dangerous function call: {node.func.id}\nnode:\n{ast.unparse(node)}"
                    )

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
                        raise ValueError(
                            "__init__ must have signature (self, game_description)"
                        )

                # Validate __call__ method
                elif node.name == '__call__':
                    args = [arg.arg for arg in node.args.args]
                    if args != ['self', 'state', 'history']:
                        raise ValueError(
                            "__call__ must have signature (self, state, history)"
                        )

        # Check required methods exist
        missing_methods = required_methods - found_methods
        if missing_methods:
            raise ValueError(f"Missing required methods: {missing_methods}")

        # Check for unsafe constructs
        is_safe_node(class_def)

    except SyntaxError as e:
        raise ValueError(f"Syntax error in generated code: {e}") from e
    except Exception as e:
        raise ValueError(f"Code validation failed: {e}") from e


def test_generated_strategy(class_code: str,
                            game_name: str):
    """Test the generated strategy by actually running it in games."""
    import tempfile

    from emergent_llm.players import LLMPlayer, SimplePlayer

    # Create a temporary module to load the strategy
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Write necessary imports and the class
        f.write("""
from emergent_llm.players import BaseStrategy
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription, CommonPoolDescription, CommonPoolState
from emergent_llm.common import Action, C, D, PlayerHistory, GameState
import numpy as np
from numpy.typing import NDArray
import math
import random

""")
        f.write(class_code)
        temp_file = f.name

    try:
        # Load the temporary module
        spec = importlib.util.spec_from_file_location("temp_strategy",
                                                      temp_file)
        temp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(temp_module)

        # Find the strategy class
        strategy_classes = [
            cls for name, cls in inspect.getmembers(temp_module)
            if inspect.isclass(cls) and issubclass(cls, BaseStrategy) and
            cls != BaseStrategy
        ]

        if not strategy_classes:
            raise ValueError("No strategy class found in generated code")

        assert len(
            strategy_classes) == 1, "More than one strategy class defined"
        strategy_class = strategy_classes[0]


        for n_players in [4, 256]:
            game_description = STANDARD_GENERATORS[game_name + "_default"](n_players=n_players)
            game_class = game_description.game_type()

            player = LLMPlayer("test_player",
                            Gene("dummy", COLLECTIVE),
                            game_description,
                            strategy_class,
                            max_errors=0)

            # Test against different opponent types
            test_mixtures = [
                [
                    SimplePlayer(f"cooperator_{i}", Cooperator)
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"defector_{i}", Defector)
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"random_{i}", Random)
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"mostly_coop_{i}", RandomCooperator)
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"mostly_defect_{i}", RandomDefector)
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"alternating_{i}", PeriodicDefector(2))
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"grad_{i}", GradualDefector(10 + i))
                    for i in range(n_players - 1)
                ],
                [
                    SimplePlayer(f"period_{i}", PeriodicDefector(2 + i))
                    for i in range(n_players - 1)
                ]
            ]


            start_time = time.time()

            for mixture in test_mixtures:
                players = [player] + mixture
                game = game_class(players, game_description)

                # This will raise an exception if the strategy fails
                result = game.play_game()

            total_time = time.time() - start_time
            if total_time > 1:
                raise RuntimeError(f"Strategy took {total_time:.1f} to run all mixtures")

    finally:
        # Clean up temp file
        os.unlink(temp_file)


def get_llm_response(config: LLMConfig, system_prompt: str,
                     user_prompt: str) -> str:
    """Get response from LLM client."""

    def handle_retry(attempt, max_retries, error):
        """Helper function to handle retry logic consistently"""
        if attempt < max_retries - 1:
            wait_time = 2**attempt
            logging.warning(
                f"Attempt {attempt + 1} failed: {error}. Retrying in {wait_time}s..."
            )
            time.sleep(wait_time)
            return True
        logging.error(
            f"All {max_retries} attempts failed. Final error: {error}")
        return False

    for attempt in range(config.max_retries):
        if isinstance(config.client, openai.OpenAI):
            try:
                response = config.client.chat.completions.create(
                    model=config.model_name,
                    messages=[{
                        "role": "system",
                        "content": system_prompt
                    }, {
                        "role": "user",
                        "content": user_prompt
                    }],
                )
                return response.choices[0].message.content
            except (openai.InternalServerError, openai.RateLimitError,
                    openai.APITimeoutError, openai.APIConnectionError) as e:
                if not handle_retry(attempt, config.max_retries, e):
                    raise
                continue

        elif isinstance(config.client, anthropic.Anthropic):
            try:
                response = config.client.messages.create(
                    model=config.model_name,
                    system=system_prompt,
                    max_tokens=4096,
                    messages=[{
                        "role": "user",
                        "content": user_prompt
                    }])
                if hasattr(
                        response,
                        'stop_reason') and response.stop_reason == "max_tokens":
                    logging.warning(
                        f"Response was truncated due to max_tokens limit. "
                        f"Consider increasing max_tokens. Stop reason: {response.stop_reason}"
                    )
                return response.content[0].text
            except (anthropic.InternalServerError, anthropic.RateLimitError,
                    anthropic.APITimeoutError,
                    anthropic.APIConnectionError) as e:
                if not handle_retry(attempt, config.max_retries, e):
                    raise
                continue

        elif isinstance(config.client, ollama.Client):
            try:
                response = config.client.chat(model=config.model_name,
                                              messages=[{
                                                  "role": "system",
                                                  "content": system_prompt
                                              }, {
                                                  "role": "user",
                                                  "content": user_prompt
                                              }])
                return response['message']['content']
            except ollama.ResponseError as e:
                if e.status_code == 404:
                    logging.error(
                        f"Ollama model '{config.model_name}' not found. Use 'ollama pull {config.model_name}' to download it."
                    )
                raise

        elif isinstance(config.client, genai.Client):
            full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
            try:
                response = config.client.models.generate_content(
                    model=config.model_name,
                    contents=full_prompt,
                )
                return response.text
            except genai_errors.APIError as e:
                if not handle_retry(attempt, config.max_retries, e):
                    raise
                continue

        else:
            raise ValueError(f"Unknown client type: {type(config.client)}")

    raise RuntimeError(f"All {config.max_retries} attempts failed")


def write_strategy_class(description: str, code: str, attitude: Attitude,
                         n: int) -> str:
    """Create a complete strategy class with proper naming and documentation."""

    # Parse and modify the class
    tree = ast.parse(code)
    class_def = tree.body[0]

    # Rename class to be unique
    class_name = f"Strategy_{attitude.name}_{n}"
    class_def.name = class_name

    # Convert back to source code
    return ast.unparse(tree)


def generate_descriptions(config: LLMConfig, game_name: str,
                          attitudes: list[Attitude], n_per_attitude: int,
                          description_file: Path, logger: logging.Logger):
    """Phase 1: Generate strategy descriptions."""

    # Check existing descriptions
    existing_descriptions = parse_strategy_description_file(description_file)
    logger.info(f"Found {len(existing_descriptions)} existing descriptions")

    # Get missing descriptions
    missing = get_missing_descriptions(existing_descriptions, attitudes,
                                       n_per_attitude)

    if not missing:
        print("All descriptions already exist!")
        return

    # Create description file header if it doesn't exist
    if not description_file.exists():
        header = f'''"""
Strategy descriptions for {game_name}.

Generated with:
- Provider: {config.client.__class__.__name__}
- Model: {config.model_name}
"""

'''
        description_file.parent.mkdir(parents=True, exist_ok=True)
        with open(description_file, 'w', encoding='utf-8') as f:
            f.write(header)

    # Generate missing descriptions
    print(f"Generating {len(missing)} missing descriptions...")

    for attitude, n in missing:
        try:
            print(f"Generating {attitude.name}_{n} description...")
            description = generate_strategy_description(config, attitude,
                                                        game_name, logger)
            write_description_to_file(description_file, attitude, n,
                                      description)
            print(f"✓ Generated description for {attitude.name}_{n}")
            logger.info(
                f"Successfully generated description for {attitude.name}_{n}")

        except Exception as e:
            logger.error(
                f"Failed to generate description for {attitude.name}_{n}: {e}")
            print(
                f"✗ Error generating description for {attitude.name}_{n}: {e}")
            continue

    print(f"\nDescriptions written to {description_file}")


def generate_implementations(config: LLMConfig, game_name: str,
                             description_file: Path, strategy_file: Path,
                             logger: logging.Logger, max_retries: int = 3):
    """Phase 2: Generate code implementations from descriptions."""

    # Read existing descriptions
    existing_descriptions = parse_strategy_description_file(description_file)
    if not existing_descriptions:
        print(
            f"No descriptions found in {description_file}. Run description generation first."
        )
        return

    # Check existing implementations
    existing_strategies = parse_strategy_implementation_file(strategy_file)
    logger.info(f"Found {len(existing_strategies)} existing implementations")

    # Get missing implementations
    missing = get_missing_implementations(existing_strategies,
                                          existing_descriptions)

    if not missing:
        print("All implementations already exist!")
        return

    # Create strategy file header if it doesn't exist
    if not strategy_file.exists():
        header = f'''"""
Generated LLM strategies for social dilemma games.

This file contains strategy classes generated by LLMs for game theory experiments.
Each strategy is a callable class that implements a specific approach to the game.

Generated with:
- Provider: {config.client.__class__.__name__}
- Model: {config.model_name}
- Game: {game_name}
"""

from emergent_llm.players import BaseStrategy
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription, CommonPoolDescription, CommonPoolState
from emergent_llm.common import Action, C, D, PlayerHistory, GameState
import numpy as np
from numpy.typing import NDArray
import math
import random

'''
        strategy_file.parent.mkdir(parents=True, exist_ok=True)
        with open(strategy_file, "w", encoding="utf8") as f:
            f.write(header)

    # Generate missing implementations
    print(f"Generating {len(missing)} missing implementations...")

    with strategy_file.open("a", encoding="utf-8") as f:
        for attitude_name, n, description in missing:
            try:
                print(f"Implementing {attitude_name}_{n}...")

                # Convert attitude name back to Attitude enum
                attitude = Attitude[attitude_name]

                strategy_class = create_single_strategy_implementation(
                    config, attitude, n, description, game_name,
                    logger, max_retries)
                f.write("\n\n" + strategy_class)
                f.flush()  # Save progress
                print(f"✓ Implemented {attitude_name}_{n}")
                logger.info(f"Successfully implemented {attitude_name}_{n}")

            except Exception as e:
                logger.error(f"Failed to implement {attitude_name}_{n}: {e}")
                print(f"✗ Error implementing {attitude_name}_{n}: {e}")
                continue

    print(f"\nImplementations written to {strategy_file}")


def create_single_strategy_implementation(
        config: LLMConfig, attitude: Attitude,
        n: int, description: str, game_name: str,
        logger: logging.Logger, max_retries: int = 3) -> str:
    """Create a single strategy implementation from description."""

    # Code generation with retry logic
    for attempt in range(max_retries):
        try:
            print(f"  Coding attempt {attempt + 1}...")

            # Generate code implementation
            code = generate_strategy_code(config, description,
                                          game_name, logger)

            # Create complete class
            class_code = write_strategy_class(description, code, attitude, n)

            # Test the generated strategy
            test_generated_strategy(class_code, game_name)

            return class_code

        except Exception as e:
            logger.warning(
                f"Coding attempt {attempt + 1} failed for {attitude.name}_{n}: {e}"
            )
            print(f"  ✗ Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                logger.error(
                    f"All {max_retries} coding attempts failed for {attitude.name}_{n}"
                )
                raise
            time.sleep(1)  # Brief pause before retry

    raise RuntimeError(
        f"Unexpected failure in strategy implementation for {attitude.name}_{n}"
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate LLM strategies for social dilemma games")

    # Phase selection
    subparsers = parser.add_subparsers(dest='phase', help='Generation phase')
    subparsers.required = True

    # Phase 1: Description generation
    desc_parser = subparsers.add_parser('descriptions',
                                        help='Generate strategy descriptions')
    desc_parser.add_argument(
        "--llm_provider",
        choices=["openai", "anthropic", "ollama", "google"],
        required=True)
    desc_parser.add_argument("--model_name", type=str, required=True)
    desc_parser.add_argument("--n",
                             type=int,
                             required=True,
                             help="Number of strategies per attitude")
    desc_parser.add_argument(
        "--game_name",
        choices=["public_goods", "collective_risk", "common_pool"],
        required=True)

    # Phase 2: Implementation generation
    impl_parser = subparsers.add_parser('implementations',
                                        help='Generate code implementations')
    impl_parser.add_argument(
        "--llm_provider",
        choices=["openai", "anthropic", "ollama", "google"],
        required=True)
    impl_parser.add_argument("--model_name", type=str, required=True)
    impl_parser.add_argument(
        "--game_name",
        choices=["public_goods", "collective_risk", "common_pool"],
        required=True)
    impl_parser.add_argument("--max_retries", type=int, default=3)

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    # Create output directory structure
    strategies_dir = Path("strategies") / args.game_name
    strategies_dir.mkdir(parents=True, exist_ok=True)
    log_dir = Path(f"{strategies_dir}/logs")
    log_dir.mkdir(exist_ok=True)

    # Setup file paths
    description_file = strategies_dir / f"{args.model_name}_descriptions.py"
    strategy_file = strategies_dir / f"{args.model_name}.py"
    log_file = log_dir / f"{args.model_name}_{args.phase}.log"

    # Setup logging
    logger = setup_logging(log_file)

    # Setup LLM client
    if args.llm_provider == "openai":
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    elif args.llm_provider == "anthropic":
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    elif args.llm_provider == "ollama":
        client = ollama.Client(host=os.environ["OLLAMA_HOST"])
    elif args.llm_provider == "google":
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    else:
        raise ValueError(f"Unknown client {args.llm_provider}")

    config = LLMConfig(client, args.model_name)

    # Run appropriate phase
    if args.phase == 'descriptions':
        generate_descriptions(config, args.game_name,
                              [COLLECTIVE, EXPLOITATIVE], args.n,
                              description_file, logger)
    elif args.phase == 'implementations':
        generate_implementations(config, args.game_name,
                                 description_file, strategy_file, logger,
                                 args.max_retries)

    logger.info(f"Phase {args.phase} completed")


if __name__ == "__main__":
    main()
