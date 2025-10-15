"""Test generated LLM strategies for correctness and safety."""
import argparse
import importlib
import importlib.util
import inspect
import os
import time
import unittest

import numpy as np
from emergent_llm.common import C, D, Gene
from emergent_llm.games import (CollectiveRiskDescription, CollectiveRiskGame,
                                PublicGoodsDescription, PublicGoodsGame)
from emergent_llm.players import BaseStrategy, LLMPlayer, SimplePlayer


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        help="Name of the python module to call the LLM algorithms")
    parser.add_argument(
        "--game",
        type=str,
        required=True,
        choices=['pgg', 'crd', 'cpr'],
        help="Game type: pgg (Public Goods Game), crd (Collective Risk Dilemma), cpr (Common Pool Resource)")
    parser.add_argument(
        "--name",
        action="store_true",
        help="Print the name of the class being tested, to help discover slow implementations")
    return parser.parse_args()


class TestStrategyClass(unittest.TestCase):
    pass


def check_for_string(func_or_method, string: str) -> bool:
    """Check if a string appears in the source code of a function or method."""
    # Unwrap the function if it's decorated
    while hasattr(func_or_method, '__wrapped__'):
        func_or_method = func_or_method.__wrapped__

    try:
        source = inspect.getsource(func_or_method)
        return string in source
    except OSError:
        # Can't get source (e.g., built-in function)
        return False


def create_test(strategy_class: type, game_name: str, log: bool = False):
    """Create a test function for a strategy class."""
    def test(self):
        if log:
            print(f"{strategy_class.__name__}")

        # Create game instance based on command line argument
        if game_name == 'pgg':
            game_type = PublicGoodsGame  # Use defaults
            game_description = PublicGoodsDescription(
                n_players=6,
                n_rounds=20,
                k=2.0
            )
        elif game_name == 'crd':
            game_type = CollectiveRiskGame  # Use defaults
            game_description = CollectiveRiskDescription(
                n_players=6,
                n_rounds=20,
                m=3,
                k=2.0,
            )
        else:
            raise ValueError(f"Unknown game type: {game_type}")

        player = LLMPlayer(f"{strategy_class.__name__}",
                           Gene(None, None),
                           game_description,
                           strategy_class)

        # Test in different opponent mixtures
        test_mixtures = [
            [SimplePlayer(f"cooperator_{i}", lambda: C) for i in range(game_description.n_players - 1)],
            [SimplePlayer(f"defector_{i}", lambda: D) for i in range(game_description.n_players - 1)],
            [SimplePlayer(f"random_{i}", lambda: np.random.choice([C,D])) for i in range(game_description.n_players - 1)],
        ]

        for i, mixture in enumerate(test_mixtures):
            players = [player] + mixture

            try:
                # Time the game
                start_time = time.time()
                game = game_type(players, game_description)
                result = game.play_game()
                end_time = time.time()

                game_duration = end_time - start_time
                print(f"Strategy {strategy_class.__name__} vs mixture {i+1}: {game_duration:.4f}s")

            except Exception as e:
                self.fail(f"Strategy {strategy_class.__name__} failed during game: {str(e)}")

    return test



def load_module(module_path: str):
    """
    Load a Python module from either an absolute or relative path.

    Args:
        module_path (str): Path to the Python module

    Returns:
        module: The loaded Python module
    """
    # add .py if missing from the module
    if not module_path.endswith(".py"):
      module_path += ".py"

    # Convert relative path to absolute path if needed
    if not os.path.isabs(module_path):
      # Get absolute path relative to current working directory
      module_path = os.path.abspath(module_path)

    if not os.path.exists(module_path):
        raise ImportError(f"Could not find module at {module_path}")

    # Get the module name from the file path
    module_name = os.path.basename(module_path)

    # Load the module using importlib
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Could not load module specification from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def load_algorithms(module_name: str) -> list[type[BaseStrategy]]:
  module = load_module(module_name)

  # Get all classes from the module that are derived from axelrod.Player
  algos = [
    cls for name, cls in inspect.getmembers(module)
    if inspect.isclass(cls) and issubclass(cls, BaseStrategy) and cls != BaseStrategy
  ]

  return algos

def main():
    parsed_args = parse_arguments()
    algos = load_algorithms(parsed_args.algo)

    # Dynamically create test methods for each strategy class
    for strategy_class in algos:
        test_method = create_test(strategy_class, parsed_args.game, parsed_args.name)
        test_method.__name__ = f'test_{strategy_class.__name__}'
        setattr(TestStrategyClass, test_method.__name__, test_method)

    # Run tests
    unittest.main(argv=['first-arg-is-ignored'])


if __name__ == '__main__':
    main()
