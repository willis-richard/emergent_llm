"""Generate LLM strategies for social dilemma games in two phases.

Phase 1: Generate strategy descriptions
Phase 2: Generate code implementations from descriptions
"""
import argparse
import ast
import importlib.util
import inspect
import json
import logging
import os
import re
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

import anthropic
import ollama
import openai
from google import genai
from google.genai import errors as genai_errors

from emergent_llm.common import Attitude, GameDescription
from emergent_llm.generation.prompts import (
    HEADER_IMPORTS,
    create_code_user_prompt,
    create_strategy_user_prompt,
)
from emergent_llm.generation.test_strategies import test_strategy_class
from emergent_llm.games import get_game_type
from emergent_llm.players import (
    BaseStrategy,)

LOCAL_IMPORTS = """from emergent_llm.players import BaseStrategy
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription, CommonPoolDescription
from emergent_llm.common import Action, C, D, PlayerHistory"""

EFFORT_LEVELS = ("low", "medium", "high")

# Anthropic models on adaptive thinking: budget_tokens is a 400 on these, and
# thinking depth is set with output_config.effort instead.
_ANTHROPIC_ADAPTIVE = {
    "claude-opus-5", "claude-fable-5",
}

# Adaptive models that additionally reject thinking={"type": "disabled"}.
_ANTHROPIC_ALWAYS_THINKING = {"claude-fable-5"}

# Legacy extended-thinking-only models (claude-haiku-4-5).
_ANTHROPIC_BUDGETS = {"low": 1024, "medium": 4096, "high": 12000}


class RefusalError(RuntimeError):
    """A safety classifier declined the request (Claude Fable 5).

    Returned as HTTP 200 with stop_reason "refusal", so it must be checked
    explicitly or the refusal text gets parsed as a strategy.
    """


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
    reasoning_effort: str = "low"
    max_retries: int = 3
    max_tokens: int = 32000

    def __post_init__(self):
        if self.reasoning_effort not in EFFORT_LEVELS:
            raise ValueError(
                f"reasoning_effort must be one of {EFFORT_LEVELS}, "
                f"got {self.reasoning_effort!r}")


def parse_strategy_description_file(
        strategy_description_file: Path) -> dict[tuple[str, int], str]:
    """Parse existing strategy description file and extract existing descriptions.

    Descriptions are written by `write_description_to_file` as JSON-escaped
    Python string literals, so evaluating the assignment recovers the model's
    text exactly, backslashes included.

    Returns dict mapping (attitude_name, n) tuple to strategy description string.
    """
    if not strategy_description_file.exists():
        return {}

    source = strategy_description_file.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise RuntimeError(
            f"{strategy_description_file} is not valid Python: {e}") from e

    strategy_descriptions = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if not isinstance(node.value, ast.Constant):
            continue
        match = re.match(r'description_([A-Z]+)_(\d+)$', target.id)
        if match is None:
            continue
        value = node.value.value
        if isinstance(value, str):
            strategy_descriptions[(match.group(1), int(match.group(2)))] = value

    return strategy_descriptions


def parse_strategy_implementation_file(
        strategy_implementation_file: Path) -> set[str]:
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


def write_description_to_file(strategy_description_file: Path,
                              attitude: Attitude, n: int,
                              strategy_description: str):
    """Append a description as a JSON-escaped Python string literal.

    json.dumps escapes backslashes, so `parse_strategy_description_file`
    reads back exactly what the model emitted.
    """
    var_name = f"description_{attitude.name}_{n}"

    # Create description entry
    description_entry = f"\n{var_name} = {json.dumps(strategy_description)}\n"

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
    existing_implementations: set[str], existing_descriptions: dict[tuple[str,
                                                                          int],
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
                                  logger: logging.Logger | None = None) -> str:
    """Generate natural language strategy description."""
    system_prompt = """You are an AI assistant with expertise in strategic thinking.

Output only the strategy description itself — no preamble, no meta-commentary, no conclusion.

Do not:
- Restate the game rules, parameters, or payoff structure
- Discuss why the strategy is good or weigh its tradeoffs
- Add framing like "Here is...", "I'll design...", or "In summary..."
- Hedge with caveats about tournament conditions or opponent uncertainty

Use natural language with optional pseudocode. Be precise about decision rules and edge cases."""
    user_prompt = create_strategy_user_prompt(attitude, game_name)

    if logger:
        logger.info(f"Generating {attitude.value} strategy description")
        logger.info(f"System prompt: {system_prompt}")
        logger.info(f"User prompt: {user_prompt}")

    response = get_llm_response(config, system_prompt, user_prompt).text

    if logger:
        logger.info(f"Strategy description: {response}")

    return response


def generate_strategy_code(config: LLMConfig,
                           strategy_description: str,
                           game_name: str,
                           logger: logging.Logger = None) -> str:
    """Generate Python code from strategy description."""
    system_prompt = "You are an expert Python programmer implementing game theory strategies."
    user_prompt = create_code_user_prompt(strategy_description, game_name)

    if logger:
        logger.info("Generating strategy code")
        logger.info(f"Code user prompt: {user_prompt}")

    response = get_llm_response(config, system_prompt, user_prompt).text

    if logger:
        logger.info(f"Generated code: {response}")

    _, game_description_class = get_game_type(game_name)

    # Clean and validate the code
    code = clean_generated_code(response)
    validate_strategy_code(code, game_description_class)
    return code


def clean_generated_code(response: str) -> str:
    """Clean LLM response to extract just the Python code."""
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


def validate_strategy_code(code: str,
                           game_description_class: type[GameDescription]):
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
            ast.Try, ast.ExceptHandler, ast.Yield,
            ast.JoinedStr, ast.Assert
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

        # Pick the expected __call__ signature based on whether this game has state
        if game_description_class.has_stock():
            expected_call_args = ['self', 'history', 'current_stock']
        else:
            expected_call_args = ['self', 'history']

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
                    if args != expected_call_args:
                        raise ValueError(
                            f"__call__ must have signature {tuple(expected_call_args)}, "
                            f"got {tuple(args)}"
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


def test_generated_strategy(class_code: str, game_name: str):
    """Test the generated strategy by actually running it in games."""
    # Create a temporary module to load the strategy
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Write necessary imports and the class
        f.write(f"""
{HEADER_IMPORTS}

{LOCAL_IMPORTS}
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

        test_strategy_class(strategy_class, game_name, allowed_time=2)

    finally:
        # Clean up temp file
        os.unlink(temp_file)


@dataclass
class LLMResponse:
    """Uniform response across providers.

    `reasoning` is a provider-generated summary, and is not
    comparable across providers. Anthropic summarises with a separate
    model and returns nothing unless display is "summarized"; Gemini and
    OpenAI return their own sanitised summaries; Ollama varies by model.
    For cross-model comparison use the visible reasoning in `text`.
    """
    text: str
    reasoning: str = ""
    usage: dict | None = None
    stop_reason: str | None = None


def get_llm_response(config: LLMConfig,
                     system_prompt: str,
                     user_prompt: str,
                     *,
                     max_tokens: int | None = None,
                     thinking: bool = True) -> LLMResponse:
    """Get response from LLM client, with native reasoning where available.

    `max_tokens` defaults to config.max_tokens. On adaptive-thinking models it
    is a hard ceiling on thinking plus response text combined, so it must be
    generous or responses truncate mid-answer.
    """
    max_tokens = config.max_tokens if max_tokens is None else max_tokens

    def handle_retry(attempt, max_retries, error):
        if attempt < max_retries - 1:
            wait_time = 2**attempt
            logging.warning(
                f"Attempt {attempt + 1} failed: {error}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            return True
        logging.error(f"All {max_retries} attempts failed. Final error: {error}")
        return False

    for attempt in range(config.max_retries):
        if isinstance(config.client, openai.OpenAI):
            try:
                kwargs = dict(
                    model=config.model_name,
                    instructions=system_prompt,
                    input=user_prompt,
                    max_output_tokens=max_tokens,
                )
                if thinking:
                    # OpenAI never exposes raw traces; "auto" gives a summary.
                    kwargs["reasoning"] = {"effort": config.reasoning_effort,
                                           "summary": "auto"}
                response = config.client.responses.create(**kwargs)

                summaries = []
                for item in response.output:
                    if getattr(item, "type", None) != "reasoning":
                        continue
                    for part in (getattr(item, "summary", None) or []):
                        text = getattr(part, "text", None)
                        if text:
                            summaries.append(text)

                return LLMResponse(
                    text=response.output_text,
                    reasoning="\n\n".join(summaries),
                    usage=response.usage.model_dump() if response.usage else None,
                    stop_reason=getattr(response, "status", None),
                )
            except (openai.InternalServerError, openai.RateLimitError,
                    openai.APITimeoutError, openai.APIConnectionError) as e:
                if not handle_retry(attempt, config.max_retries, e):
                    raise
                continue

        elif isinstance(config.client, anthropic.Anthropic):
            adaptive = config.model_name in _ANTHROPIC_ADAPTIVE
            always_thinks = config.model_name in _ANTHROPIC_ALWAYS_THINKING
            try:
                kwargs = dict(
                    model=config.model_name,
                    system=system_prompt,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                if adaptive:
                    # budget_tokens is a 400 here; effort sets thinking depth.
                    # Sampler params (temperature/top_p/top_k) are also 400s.
                    kwargs["output_config"] = {"effort": config.reasoning_effort}
                    if thinking or always_thinks:
                        # display defaults to "omitted": opt in or log blanks.
                        kwargs["thinking"] = {"type": "adaptive",
                                              "display": "summarized"}
                    else:
                        kwargs["thinking"] = {"type": "disabled"}
                elif thinking:
                    budget = _ANTHROPIC_BUDGETS[config.reasoning_effort]
                    kwargs["max_tokens"] = budget + max_tokens
                    # Anthropic requires temperature=1 when thinking is enabled.
                    kwargs["temperature"] = 1.0
                    kwargs["thinking"] = {"type": "enabled",
                                          "budget_tokens": budget}

                # Stream unconditionally: the SDK refuses non-streaming calls
                # above max_tokens 21,333, and thinking pushes us over.
                with config.client.messages.stream(**kwargs) as stream:
                    response = stream.get_final_message()

                if response.stop_reason == "refusal":
                    category = getattr(
                        getattr(response, "stop_details", None),
                        "category", None)
                    raise RefusalError(
                        f"{config.model_name} refused the request "
                        f"(category={category})")

                if response.stop_reason == "max_tokens":
                    raise RuntimeError(
                        "Anthropic response truncated; raise max_tokens")

                return LLMResponse(
                    text="".join(b.text for b in response.content
                                 if b.type == "text"),
                    reasoning="\n\n".join(b.thinking for b in response.content
                                          if b.type == "thinking" and b.thinking),
                    usage=response.usage.model_dump(),
                    stop_reason=response.stop_reason,
                )
            except (anthropic.InternalServerError, anthropic.RateLimitError,
                    anthropic.APITimeoutError, anthropic.APIConnectionError) as e:
                if not handle_retry(attempt, config.max_retries, e):
                    raise
                continue

        elif isinstance(config.client, ollama.Client):
            try:
                # NOTE: Ollama has no effort equivalent; reasoning_effort is
                # ignored here, so it is not comparable with the other rows.
                response = config.client.chat(
                    model=config.model_name,
                    think=thinking,
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": user_prompt}])
                message = response["message"]
                return LLMResponse(text=message["content"],
                                   reasoning=message.get("thinking", "") or "")
            except ollama.ResponseError as e:
                if e.status_code == 404:
                    logging.error(
                        f"Ollama model '{config.model_name}' not found. "
                        f"Use 'ollama pull {config.model_name}'.")
                raise

        elif isinstance(config.client, genai.Client):
            full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
            try:
                thinking_config = genai.types.ThinkingConfig(
                    thinking_level=genai.types.ThinkingLevel(
                        config.reasoning_effort),
                    include_thoughts=thinking,
                )
                response = config.client.models.generate_content(
                    model=config.model_name,
                    contents=full_prompt,
                    config=genai.types.GenerateContentConfig(
                        thinking_config=thinking_config,
                        max_output_tokens=max_tokens,
                        # Don't set temperature — Google recommends the default.
                    ),
                )
                # Iterate parts: response.text can raise when thought parts
                # are present, and we need them separated anyway.
                texts, thoughts = [], []
                for part in response.candidates[0].content.parts:
                    if not getattr(part, "text", None):
                        continue
                    (thoughts if getattr(part, "thought", False)
                     else texts).append(part.text)

                return LLMResponse(
                    text="".join(texts),
                    reasoning="\n\n".join(thoughts),
                    usage=(response.usage_metadata.model_dump()
                           if response.usage_metadata else None),
                )
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
- Effort: {config.reasoning_effort}
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


def generate_implementations(config: LLMConfig,
                             game_name: str,
                             description_file: Path,
                             strategy_file: Path,
                             logger: logging.Logger,
                             max_retries: int = 3):
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
- Effort: {config.reasoning_effort}
- Game: {game_name}
"""

{HEADER_IMPORTS}

{LOCAL_IMPORTS}


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
                    config, attitude, n, description, game_name, logger,
                    max_retries)
                f.write("\n\n" + strategy_class)
                f.flush()  # Save progress
                print(f"✓ Implemented {attitude_name}_{n}")
                logger.info(f"Successfully implemented {attitude_name}_{n}")

            except Exception as e:
                logger.error(f"Failed to implement {attitude_name}_{n}: {e}")
                print(f"✗ Error implementing {attitude_name}_{n}: {e}")
                continue

    print(f"\nImplementations written to {strategy_file}")


def create_single_strategy_implementation(config: LLMConfig,
                                          attitude: Attitude,
                                          n: int,
                                          description: str,
                                          game_name: str,
                                          logger: logging.Logger,
                                          max_retries: int = 3) -> str:
    """Create a single strategy implementation from description."""
    # Code generation with retry logic
    for attempt in range(max_retries):
        try:
            print(f"  Coding attempt {attempt + 1}...")

            # Generate code implementation
            code = generate_strategy_code(config, description, game_name,
                                          logger)

            # Create complete class
            class_code = write_strategy_class(description, code, attitude, n)

            # Test the generated strategy
            test_generated_strategy(class_code, game_name)

            return class_code

        except RefusalError:
            # A classifier refusal will not resolve on retry.
            logger.error(f"Refused for {attitude.name}_{n}; not retrying")
            raise

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
    parser.add_argument("--llm_provider",
                        choices=["openai", "anthropic", "ollama", "google", "openrouter"],
                        required=True)
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--reasoning_effort",
                        choices=list(EFFORT_LEVELS),
                        default="low",
                        help="Provider specific")
    parser.add_argument("--max_tokens", type=int, default=32000,
                        help="Hard ceiling on output. On adaptive-thinking "
                             "models this covers thinking AND response text.")
    parser.add_argument(
        "--game_name",
        choices=["public_goods", "collective_risk", "common_pool"],
        required=True)
    parser.add_argument("--strategies_dir", type=str, default="strategies")
    parser.add_argument(
        "--full_attitudes",
        action="store_true",
        help=("Use the full set of Attitudes, instead of just collective, selfish."),
    )

    # Phase selection
    subparsers = parser.add_subparsers(dest='phase', help='Generation phase')
    subparsers.required = True

    # Phase 1: Description generation
    desc_parser = subparsers.add_parser('descriptions',
                                        help='Generate strategy descriptions')
    desc_parser.add_argument("--n",
                             type=int,
                             required=True,
                             help="Number of strategies per attitude")

    # Phase 2: Implementation generation
    impl_parser = subparsers.add_parser('implementations',
                                        help='Generate code implementations')
    impl_parser.add_argument("--max_retries", type=int, default=3)

    return parser.parse_args()


def make_safe(model_name: str) -> str:
    return model_name.replace("/", "-").replace(":", "-")


def parse_selected_attitudes(attitude_values: str) -> list[Attitude]:
    parsed_values = [value.strip() for value in attitude_values.split(",") if value.strip()]
    invalid_values = [
        value for value in parsed_values
        if value not in {attitude.value for attitude in Attitude}
    ]
    if invalid_values:
        raise ValueError(
            f"Invalid attitudes: {invalid_values}. "
            f"Valid values are {[attitude.value for attitude in Attitude]}")
    return [Attitude(value) for value in parsed_values]


def main():
    """Main function."""
    args = parse_arguments()
    selected_attitudes = list(Attitude) if args.full_attitudes else Attitude.base_attitudes()

    # Create output directory structure
    strategies_dir = Path(args.strategies_dir) / args.game_name
    strategies_dir.mkdir(parents=True, exist_ok=True)
    log_dir = Path(f"{strategies_dir}/logs")
    log_dir.mkdir(exist_ok=True)

    # Setup file paths
    safe_model_name = make_safe(args.model_name)
    description_file = strategies_dir / f"{safe_model_name}_descriptions.py"
    strategy_file = strategies_dir / f"{safe_model_name}.py"
    log_file = log_dir / f"{safe_model_name}_{args.phase}.log"

    # Setup logging
    logger = setup_logging(log_file)

    # Setup LLM client
    if args.llm_provider == "openai":
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    elif args.llm_provider == "anthropic":
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    elif args.llm_provider == "ollama":
        client = ollama.Client(host=os.environ["OLLAMA_HOST"])
    elif args.llm_provider == "openrouter":
        client = openai.OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.environ["OPENROUTER_API_KEY"])
    elif args.llm_provider == "google":
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    else:
        raise ValueError(f"Unknown client {args.llm_provider}")

    config = LLMConfig(client, args.model_name, args.reasoning_effort,
                       max_tokens=args.max_tokens)

    # Run appropriate phase
    if args.phase == 'descriptions':
        generate_descriptions(config, args.game_name,
                              selected_attitudes, args.n,
                              description_file, logger)
    elif args.phase == 'implementations':
        generate_implementations(config, args.game_name, description_file,
                                 strategy_file, logger, args.max_retries)

    logger.info(f"Phase {args.phase} completed")


if __name__ == "__main__":
    main()
