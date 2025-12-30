"""Batch tournament that runs mixture tournaments across different group sizes."""
import logging

from emergent_llm.players import StrategySpec
from emergent_llm.tournament.base_tournament import BaseTournamentConfig
from emergent_llm.tournament.configs import BatchTournamentConfig
from emergent_llm.tournament.mixture_tournament import MixtureTournament
from emergent_llm.tournament.results import BatchMixtureTournamentResults, MixtureTournamentResults


class BatchMixtureTournament:
    """Tournament that runs mixture tournaments across multiple group sizes."""

    def __init__(self, collective_specs: list[StrategySpec],
                 exploitative_specs: list[StrategySpec],
                 config: BatchTournamentConfig):

        self.collective_specs = collective_specs
        self.exploitative_specs = exploitative_specs
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initialised multi-group tournament with {len(collective_specs)} collective "
            f"and {len(exploitative_specs)} exploitative strategies")

        # Validate we have enough strategies for largest group size
        max_group_size = max(config.group_sizes)
        if len(collective_specs) < max_group_size:
            raise ValueError(
                f"Need at least {max_group_size} collective players for largest group size, "
                f"got {len(collective_specs)}")
        if len(exploitative_specs) < max_group_size:
            raise ValueError(
                f"Need at least {max_group_size} exploitative players for largest group size, "
                f"got {len(exploitative_specs)}")

        self.all_results: dict[int, MixtureTournamentResults] = {}

    def run_tournament(self) -> BatchMixtureTournamentResults:
        """Run tournaments across all group sizes."""
        for group_size in self.config.group_sizes:
            self.logger.info(f"Running tournament for group size {group_size}")

            # Generate game description for this group size
            game_description = self.config.game_description_generator(
                n_players=group_size)

            # Create mixture tournament config for this group size
            mixture_config = BaseTournamentConfig(
                game_description=game_description,
                repetitions=self.config.repetitions)

            collective_players = [
                spec.create_player(f"{spec.gene.attitude}_{i}",
                                   game_description)
                for i, spec in enumerate(self.collective_specs)
            ]
            exploitative_players = [
                spec.create_player(f"{spec.gene.attitude}_{i}",
                                   game_description)
                for i, spec in enumerate(self.exploitative_specs)
            ]

            # Run mixture tournament for this group size
            mixture_tournament = MixtureTournament(
                collective_players=collective_players,
                exploitative_players=exploitative_players,
                config=mixture_config)

            result = mixture_tournament.run_tournament()
            self.all_results[group_size] = result

        return BatchMixtureTournamentResults(self.config, self.all_results)
