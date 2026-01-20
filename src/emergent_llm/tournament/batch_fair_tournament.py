"""Multi-group fair tournament for testing strategy generalization across group sizes."""
import logging
from pathlib import Path

from emergent_llm.players import StrategySpec
from emergent_llm.tournament.configs import BaseTournamentConfig, BatchTournamentConfig
from emergent_llm.tournament.fair_tournament import FairTournament
from emergent_llm.tournament.results import BatchFairTournamentResults, FairTournamentResults


class BatchFairTournament:
    """Tournament that tests strategy generalization across multiple group sizes."""

    def __init__(self, strategies: list[StrategySpec],
                 config: BatchTournamentConfig):

        self.strategies = strategies
        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initialised batch fair tournament with {len(strategies)} strategies"
        )

        # Validate we have enough strategies for the largest group size to have diversity
        max_group_size = max(config.group_sizes)
        required_population = max_group_size * 4

        if len(strategies) < required_population:
            raise ValueError(
                f"Suggest you have at least {required_population} strategies for largest group size "
                f"({max_group_size}), got {len(strategies)}")

        self.results: dict[int, FairTournamentResults] = {}

    def _get_group_dir(self, group_size: int) -> Path:
        """Get directory for a specific group size's results."""
        return self.config.output_dir / f"group_{group_size}"

    def _get_completed_groups(self) -> dict[int, FairTournamentResults]:
        """Find which group sizes have already completed successfully."""
        completed = {}

        for group_size in self.config.group_sizes:
            group_dir = self._get_group_dir(group_size)
            if not group_dir.exists():
                continue

            try:
                result = FairTournamentResults.load(group_dir)
                completed[group_size] = result
                self.logger.info(f"Loaded existing results for group size {group_size}")
            except Exception as e:
                self.logger.warning(
                    f"Group {group_size} dir exists but invalid: {e}")

        return completed

    def run_tournament(self) -> BatchFairTournamentResults:
        """Run fair tournaments across all group sizes, loading completed ones."""
        self.logger.info("Checking for completed group sizes")

        # Load any existing results
        self.results = self._get_completed_groups()
        completed = set(self.results.keys())
        pending = [gs for gs in self.config.group_sizes if gs not in completed]

        self.logger.info(
            f"Batch status: {len(completed)}/{len(self.config.group_sizes)} complete, "
            f"{len(pending)} pending")

        if not pending:
            self.logger.info("All group sizes already completed")
        else:
            self._run_pending(pending)

        return BatchFairTournamentResults(self.config, self.results)

    def _run_pending(self, pending: list[int]):
        """Run tournaments for pending group sizes."""
        for group_size in pending:
            self.logger.info(f"Running fair tournament for group size {group_size}")

            result = self._run_single_group(group_size)

            # Save immediately after completion
            group_dir = self._get_group_dir(group_size)
            result.save(group_dir, self.config.output_style)
            self.logger.info(f"Saved results for group size {group_size} to {group_dir}")

            self.results[group_size] = result

    def _run_single_group(self, group_size: int) -> FairTournamentResults:
        """Run fair tournament for a single group size."""
        game_description = self.config.game_description_generator(group_size)

        tournament_config = BaseTournamentConfig(
            game_description=game_description,
            repetitions=self.config.repetitions,
            n_processes=self.config.n_processes)

        players = [
            spec.create_player(f"player_{i}", game_description)
            for i, spec in enumerate(self.strategies)
        ]

        fair_tournament = FairTournament(players, tournament_config)
        return fair_tournament.run_tournament()
