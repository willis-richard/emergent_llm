"""Batch tournament that runs mixture tournaments across different group sizes."""
import logging
from pathlib import Path

from emergent_llm.players import StrategySpec
from emergent_llm.tournament.base_tournament import BaseTournamentConfig
from emergent_llm.tournament.configs import BatchTournamentConfig
from emergent_llm.tournament.mixture_tournament import MixtureTournament
from emergent_llm.tournament.results import BatchMixtureTournamentResults, MixtureTournamentResults


def _get_group_size_dir(output_dir: Path, group_size: int) -> Path:
    """Get directory for a specific group size's results."""
    return Path(output_dir) / "group_sizes" / f"n_{group_size:04d}"


class BatchMixtureTournament:
    """Tournament that runs mixture tournaments across multiple group sizes with incremental saving."""

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

    def run_tournament(self) -> BatchMixtureTournamentResults:
        """Run tournaments across all group sizes, skipping completed ones."""
        self.logger.info("Checking for completed group sizes")

        completed = self._get_completed_group_sizes()
        pending = [gs for gs in self.config.group_sizes if gs not in completed]

        self.logger.info(
            f"Batch status: {len(completed)}/{len(self.config.group_sizes)} complete, "
            f"{len(pending)} pending")

        if not pending:
            self.logger.info("All group sizes already completed, loading results")
        else:
            self._run_pending(pending)

        return self._load_all_results()

    def _get_completed_group_sizes(self) -> set[int]:
        """Find which group sizes have already completed."""
        completed = set()
        for group_size in self.config.group_sizes:
            group_dir = _get_group_size_dir(self.config.output_dir, group_size)
            if group_dir.exists():
                try:
                    MixtureTournamentResults.load(group_dir)
                    completed.add(group_size)
                except Exception as e:
                    self.logger.warning(
                        f"Group size {group_size} dir exists but invalid: {e}")
        return completed

    def _run_pending(self, pending: list[int]):
        """Run pending group sizes and save each immediately."""
        for group_size in pending:
            self.logger.info(f"Running tournament for group size {group_size}")

            game_description = self.config.game_description_generator(
                n_players=group_size)

            mixture_config = BaseTournamentConfig(
                game_description=game_description,
                repetitions=self.config.repetitions,
                processes=self.config.processes)

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

            result = mixture_tournament.run_tournament()

            group_dir = _get_group_size_dir(self.config.output_dir, group_size)
            result.save(group_dir, self.config.output_style)
            self.logger.info(f"Completed group size {group_size} - saved to {group_dir}")

    def _load_all_results(self) -> BatchMixtureTournamentResults:
        """Load all completed results from disk."""
        results = {}
        for group_size in self.config.group_sizes:
            group_dir = _get_group_size_dir(self.config.output_dir, group_size)
            if group_dir.exists():
                results[group_size] = MixtureTournamentResults.load(group_dir)
            else:
                self.logger.warning(f"Missing result for group size {group_size}")

        if not results:
            raise ValueError("No completed group sizes found")

        return BatchMixtureTournamentResults(self.config, results)
