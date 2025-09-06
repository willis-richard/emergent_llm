"""Multi-group fair tournament for testing strategy generalization across group sizes."""
import logging
from pathlib import Path

from emergent_llm.common import Attitude, GameDescription
from emergent_llm.players import BaseStrategy, LLMPlayer
from emergent_llm.tournament.configs import (BaseTournamentConfig,
                                             BatchTournamentConfig)
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.results import (BatchFairTournamentResults,
                                             FairTournamentResults)
from tqdm import tqdm


class BatchFairTournament:
    """Tournament that tests strategy generalization across multiple group sizes."""

    def __init__(self,
                 cooperative_strategies: list[type[BaseStrategy]],
                 aggressive_strategies: list[type[BaseStrategy]],
                 config: BatchTournamentConfig):

        self.cooperative_strategies = cooperative_strategies
        self.aggressive_strategies = aggressive_strategies
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)
        n_strategies = len(cooperative_strategies) + len(aggressive_strategies)
        self.logger.info(f"Initialised batch fair tournament with {n_strategies} strategies")

        # Validate we have enough strategies for largest group size with population multiplier
        max_group_size = max(config.group_sizes)
        required_population = max_group_size * 4

        if n_strategies < required_population:
            raise ValueError(
                f"Suggest you have at least {required_population} strategies for largest group size "
                f"({max_group_size}), got {n_strategies}"
            )

        # Storage for all results
        self.results: dict[int, FairTournamentResults] = {}

    def run_tournament(self) -> BatchFairTournamentResults:
        """Run fair tournaments across all group sizes."""
        for group_size in tqdm(self.config.group_sizes, desc="Group sizes"):
            self.logger.info(f"Running fair tournament for group size {group_size}")

            # Generate game description for this group size
            game_description = self.config.game_description_generator(group_size)

            # Create tournament config for this group size
            tournament_config = BaseTournamentConfig(
                game_description=game_description,
                repetitions=self.config.repetitions
            )

            players = self.create_players_from_strategies(game_description)

            # Run fair tournament for this group size
            fair_tournament = FairTournament(players, tournament_config)
            result = fair_tournament.run_tournament()
            self.results[group_size] = result

            output_file = Path(self.config.results_dir) / "group_results" / f"group_size_{group_size}.csv"
            result.save(output_file)
            self.logger.info(f"Group {group_size} results saved: {output_file}")

        return BatchFairTournamentResults(self.config, self.results)

    def create_players_from_strategies(self, game_description: GameDescription) -> list[LLMPlayer]:
        """Create player instances from strategy classes."""
        players = []

        for i, strategy_class in enumerate(self.cooperative_strategies):
            player = LLMPlayer(f"coop_{strategy_class.__name__}",
                            Attitude.COOPERATIVE,
                            game_description,  # Just for initialization
                            strategy_class)
            players.append(player)

        for i, strategy_class in enumerate(self.aggressive_strategies):
            player = LLMPlayer(f"agg_{strategy_class.__name__}",
                            Attitude.AGGRESSIVE,
                            game_description,  # Just for initialization
                            strategy_class)
            players.append(player)

        return players
