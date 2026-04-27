"""Test generated LLM strategies for correctness and safety."""
import time
from collections.abc import Iterator
from itertools import product

from emergent_llm.common import COLLECTIVE, Action, Gene, PlayerHistory
from emergent_llm.games import STANDARD_GENERATORS
from emergent_llm.players import (
    BaseStrategy,
    Cooperator,
    Defector,
    GradualDefector,
    LLMPlayer,
    PeriodicDefector,
    Random,
    RandomCooperator,
    RandomDefector,
    SimplePlayer,
)

CooperatorCounts = tuple[int, ...]  # cooperator count per round


class FixedCooperatorCount:
    """Opponent that cooperates in round r iff its index < the prescribed count."""

    def __init__(self, opponent_index: int, counts: list[int]):
        self.opponent_index = opponent_index
        self.counts = counts

    def __call__(self, history: PlayerHistory):
        return Action.C if self.opponent_index < self.counts[history.round_number] else Action.D


def make_fixed_opponents(
    n_opponents: int, n_rounds: int
) -> Iterator[tuple[CooperatorCounts, list[SimplePlayer]]]:
    """Yield (combo, opponents) for every opponent-cooperator-count history
    of length n_rounds-1. Final-round opponent actions don't affect the
    player's decision that round, so counts are padded with a dummy 0."""
    for combo in product(range(n_opponents + 1), repeat=n_rounds - 1):
        counts = list(combo) + [0]
        opponents = [
            SimplePlayer(f"opp_{i}", FixedCooperatorCount(i, counts))
            for i in range(n_opponents)
        ]
        yield combo, opponents


def _run_exhaustive_sweep(strategy_class, game_name, n_players, n_rounds, n_games):
    """Exhaustive sweep over opponent cooperator-count histories at small n."""
    description = STANDARD_GENERATORS[game_name + "_default"](
        n_players=n_players, n_rounds=n_rounds)
    game_class = description.game_type()

    for _, opponents in make_fixed_opponents(n_players - 1, n_rounds):
        player = LLMPlayer("test", Gene("dummy", COLLECTIVE),
                           description, strategy_class, max_errors=0)
        for _ in range(n_games):
            game_class([player] + opponents, description).play_game()


def _run_fixed_opponents(strategy_class, game_name, n_players=256):
    """Cheap scaling check at large n: a few mixtures, one game each."""
    description = STANDARD_GENERATORS[game_name + "_default"](n_players=n_players)
    game_class = description.game_type()
    player = LLMPlayer("test", Gene("dummy", COLLECTIVE),
                       description, strategy_class, max_errors=0)

    # Just enough to flush O(n²) bugs, indexing issues, and one stochastic opponent
    mixtures = [
        [SimplePlayer(f"c_{i}", Cooperator) for i in range(n_players - 1)],
        [SimplePlayer(f"d_{i}", Defector)   for i in range(n_players - 1)],
        [SimplePlayer(f"r_{i}", Random)     for i in range(n_players - 1)],
        [SimplePlayer(f"r_{i}", RandomCooperator)     for i in range(n_players - 1)],
        [SimplePlayer(f"r_{i}", RandomDefector)     for i in range(n_players - 1)],
        [SimplePlayer(f"alternating_{i}", PeriodicDefector(2)) for i in range(n_players - 1)],
        [
            SimplePlayer(f"grad_{i}", GradualDefector(10 + i))
            for i in range(n_players - 1)
        ],
        [
            SimplePlayer(f"period_{i}", PeriodicDefector(2 + i))
            for i in range(n_players - 1)
        ]]
    for opps in mixtures:
        game_class([player] + opps, description).play_game()


def test_strategy_class(strategy_class: type[BaseStrategy],
                        game_name: str,
                        allowed_time: float | None) -> float:
    start = time.time()
    _run_exhaustive_sweep(strategy_class, game_name,
                         n_players=4,
                         n_rounds=5,
                         n_games=1)
    _run_fixed_opponents(strategy_class, game_name, n_players=256)
    total = time.time() - start
    if allowed_time and total > allowed_time:
        raise RuntimeError(f"Strategy took {total:.1f}s")
    return total
