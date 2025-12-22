"""Test generated LLM strategies for correctness and safety."""
import time

from emergent_llm.common import COLLECTIVE, Gene
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


def test_strategy_class(strategy_class: type[BaseStrategy], game_name: str, allowed_time: float | None) -> float:

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
        if allowed_time and total_time > allowed_time:
            raise RuntimeError(f"Strategy took {total_time:.1f} to run all mixtures")

    return total_time
