"""Test generated LLM strategies for correctness and safety."""
import unittest
import argparse
import inspect
import importlib.util
import sys
from pathlib import Path
from typing import List, Type

import numpy as np

from emergent_llm.players import LLMPlayer as LLMStrategyPlayer
from emergent_llm.common.actions import C, D
from emergent_llm.common.history import PlayerHistory
from emergent_llm.games.public_goods import PublicGoodsGame
from emergent_llm.games.collective_risk import CollectiveRiskGame
from emergent_llm.games.public_goods import PublicGoodsDescription
from emergent_llm.games.collective_risk import CollectiveRiskDescription


class TestStrategyClass(unittest.TestCase):
    """Dynamic test container for strategy classes."""
    pass


def load_strategy_module(module_path: str):
    """Load a Python module containing strategy classes."""

    if not module_path.endswith(".py"):
        module_path += ".py"

    module_path = Path(module_path).resolve()
    if not module_path.exists():
        raise ImportError(f"Could not find module at {module_path}")

    spec = importlib.util.spec_from_file_location("strategies", module_path)
    if spec is None:
        raise ImportError(f"Could not load module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_strategy_classes(module) -> List[Type[LLMStrategyPlayer]]:
    """Extract strategy classes from module."""

    classes = []
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) and
            issubclass(obj, LLMStrategyPlayer) and
            obj != LLMStrategyPlayer):
            classes.append(obj)

    return classes


def check_for_dangerous_patterns(strategy_method) -> List[str]:
    """Check for dangerous or problematic patterns in strategy code."""

    warnings = []

    # Get source code
    try:
        source = inspect.getsource(strategy_method)
    except OSError:
        return ["Could not retrieve source code"]

    # Check for problematic patterns
    if "hasattr(" in source:
        warnings.append("hasattr() found - use 'if history.is_first_round:' to initialize instead")

    if "del " in source:
        warnings.append("del statement found - set variables to None/0 instead")

    if "import " in source:
        warnings.append("import statement found - may fail in restricted environment")

    if "eval(" in source or "exec(" in source:
        warnings.append("eval/exec found - dangerous code execution")

    if "while True:" in source:
        warnings.append("infinite loop detected")

    # Check for reasonable complexity
    lines = [line.strip() for line in source.split('\n') if line.strip()]
    if len(lines) > 50:
        warnings.append(f"strategy method is very long ({len(lines)} lines)")

    return warnings


def create_mock_history(round_num: int = 0, n_opponents: int = 5) -> PlayerHistory:
    """Create mock history for testing."""

    if round_num == 0:
        return PlayerHistory(
            my_actions=np.array([], dtype=object),
            my_payoffs=np.array([]),
            opponent_actions=np.empty((0, n_opponents), dtype=object),
            opponent_payoffs=np.empty((0, n_opponents))
        )

    # Create some mock history
    my_actions = np.array([C if i % 2 == 0 else D for i in range(round_num)], dtype=object)
    my_payoffs = np.array([1.5, 2.0, 1.0, 2.5][:round_num])

    # Random opponent actions
    opponent_actions = np.array([
        [C if (i + j) % 3 == 0 else D for j in range(n_opponents)]
        for i in range(round_num)
    ], dtype=object)

    opponent_payoffs = np.array([
        [1.5 + 0.1 * j for j in range(n_opponents)]
        for i in range(round_num)
    ])

    return PlayerHistory(
        my_actions=my_actions,
        my_payoffs=my_payoffs,
        opponent_actions=opponent_actions,
        opponent_payoffs=opponent_payoffs
    )


def create_strategy_test(strategy_class: Type[LLMStrategyPlayer], verbose: bool = False):
    """Create a test function for a strategy class."""

    def test_strategy(self):
        if verbose:
            print(f"Testing {strategy_class.__name__}")

        # Test 1: Basic instantiation
        try:
            player = strategy_class(name=f"test_{strategy_class.__name__}")
        except Exception as e:
            self.fail(f"Failed to instantiate {strategy_class.__name__}: {e}")

        # Test 2: Check for dangerous patterns
        warnings = check_for_dangerous_patterns(player.strategy)
        for warning in warnings:
            print(f"WARNING in {strategy_class.__name__}: {warning}")

        # Test 3: First round behavior
        try:
            first_history = create_mock_history(0)
            action = player.strategy(first_history)
            self.assertIn(action, [C, D],
                         f"{strategy_class.__name__} returned invalid action on first round: {action}")
        except Exception as e:
            self.fail(f"{strategy_class.__name__} failed on first round: {e}")

        # Test 4: Behavior with history
        try:
            player.reset()  # Reset for clean test
            history = create_mock_history(5)
            action = player.strategy(history)
            self.assertIn(action, [C, D],
                         f"{strategy_class.__name__} returned invalid action with history: {action}")
        except Exception as e:
            self.fail(f"{strategy_class.__name__} failed with history: {e}")

        # Test 5: Multiple calls (state consistency)
        try:
            player.reset()
            history1 = create_mock_history(0)
            action1 = player.strategy(history1)

            history2 = create_mock_history(1)
            action2 = player.strategy(history2)

            self.assertIn(action1, [C, D])
            self.assertIn(action2, [C, D])
        except Exception as e:
            self.fail(f"{strategy_class.__name__} failed consistency test: {e}")

        # Test 6: Game integration (if possible)
        if hasattr(strategy_class, 'game_description'):
            try:
                self._test_game_integration(strategy_class)
            except Exception as e:
                print(f"WARNING: {strategy_class.__name__} failed game integration: {e}")

    def _test_game_integration(self, strategy_class):
        """Test strategy in actual game context."""
        game_desc = strategy_class.game_description

        # Create players
        players = [
            strategy_class(name=f"player_{i}")
            for i in range(game_desc.n_players)
        ]

        # Create appropriate game
        if game_desc.__class__.__name__ == 'PublicGoodsDescription':
            game = PublicGoodsGame(players, game_desc)
        elif game_desc.__class__.__name__ == 'CollectiveRiskDescription':
            game = CollectiveRiskGame(players, game_desc)
        else:
            return  # Skip unknown game types

        # Play a few rounds
        for _ in range(min(3, game_desc.n_rounds)):
            game.play_round()

    # Bind the integration test method
    test_strategy._test_game_integration = _test_game_integration

    return test_strategy


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--strategies", type=str, required=True,
                       help="Path to the Python module containing strategy classes")
    parser.add_argument("--verbose", action="store_true",
                       help="Print strategy names being tested")

    return parser.parse_args()


def main():
    """Main function to run tests."""
    args = parse_arguments()

    # Load strategies
    try:
        module = load_strategy_module(args.strategies)
        strategy_classes = get_strategy_classes(module)
    except Exception as e:
        print(f"Error loading strategies: {e}")
        sys.exit(1)

    if not strategy_classes:
        print("No strategy classes found in module")
        sys.exit(1)

    print(f"Found {len(strategy_classes)} strategy classes")

    # Dynamically create test methods
    for strategy_class in strategy_classes:
        test_method = create_strategy_test(strategy_class, args.verbose)
        test_name = f'test_{strategy_class.__name__}'
        setattr(TestStrategyClass, test_name, test_method)

    # Run tests
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    main()
