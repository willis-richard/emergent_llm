"""Batch tournament that runs mixture tournaments across different group sizes."""
import logging
from pathlib import Path

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

    def _get_group_dir(self, group_size: int) -> Path:
        """Get directory for a specific group size's results."""
        return self.config.output_dir / f"group_{group_size}"

    def _get_completed_groups(self) -> dict[int, MixtureTournamentResults]:
        """Find which group sizes have already completed successfully."""
        completed = {}

        for group_size in self.config.group_sizes:
            group_dir = self._get_group_dir(group_size)
            if not group_dir.exists():
                continue

            try:
                result = MixtureTournamentResults.load(group_dir)
                completed[group_size] = result
                self.logger.info(f"Loaded existing results for group size {group_size}")
            except Exception as e:
                self.logger.warning(
                    f"Group {group_size} dir exists but invalid: {e}")

        return completed

    def run_tournament(self) -> BatchMixtureTournamentResults:
        """Run tournaments across all group sizes, loading completed ones."""
        self.logger.info("Checking for completed group sizes")

        # Load any existing results
        self.all_results = self._get_completed_groups()
        completed = set(self.all_results.keys())
        pending = [gs for gs in self.config.group_sizes if gs not in completed]

        self.logger.info(
            f"Batch status: {len(completed)}/{len(self.config.group_sizes)} complete, "
            f"{len(pending)} pending")

        if not pending:
            self.logger.info("All group sizes already completed")
        else:
            self._run_pending(pending)

        return BatchMixtureTournamentResults(self.config, self.all_results)

    def _run_pending(self, pending: list[int]):
        """Run tournaments for pending group sizes."""
        for group_size in pending:
            self.logger.info(f"Running tournament for group size {group_size}")

            result = self._run_single_group(group_size)

            # Save immediately after completion
            group_dir = self._get_group_dir(group_size)
            result.save(group_dir, self.config.output_style)
            self.logger.info(f"Saved results for group size {group_size} to {group_dir}")

            self.all_results[group_size] = result

    def _run_single_group(self, group_size: int) -> MixtureTournamentResults:
        """Run mixture tournament for a single group size."""
        game_description = self.config.game_description_generator(
            n_players=group_size)

        mixture_config = BaseTournamentConfig(
            game_description=game_description,
            repetitions=self.config.repetitions,
            n_processes=self.config.n_processes)

        collective_players = [
            spec.create_player(f"{spec.gene.attitude}_{i}", game_description)
            for i, spec in enumerate(self.collective_specs)
        ]
        exploitative_players = [
            spec.create_player(f"{spec.gene.attitude}_{i}", game_description)
            for i, spec in enumerate(self.exploitative_specs)
        ]

        mixture_tournament = MixtureTournament(
            collective_players=collective_players,
            exploitative_players=exploitative_players,
            config=mixture_config)

        return mixture_tournament.run_tournament()
