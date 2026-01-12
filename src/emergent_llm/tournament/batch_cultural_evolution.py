"""Batch cultural evolution tournament with incremental saving."""
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from emergent_llm.generation import StrategyRegistry
from emergent_llm.tournament.configs import BatchCulturalEvolutionConfig
from emergent_llm.tournament.cultural_evolution import CulturalEvolution
from emergent_llm.tournament.results import CulturalEvolutionResults, BatchCulturalEvolutionResults


def _get_run_path(output_dir: Path, run_id: int, compress: bool) -> Path:
    """Get path for a specific run's results file."""
    ext = ".json.gz" if compress else ".json"
    return Path(output_dir) / "runs" / f"run_{run_id:03d}{ext}"


def _run_single_experiment(
    run_id: int,
    config: BatchCulturalEvolutionConfig,
) -> tuple[int, CulturalEvolutionResults]:
    """
    Worker function that runs a single evolution experiment.

    Creates its own registry to avoid pickling issues with ProcessPoolExecutor.
    Saves result immediately upon completion.
    """
    logger = logging.getLogger(f"Run-{run_id}")
    logger.info(f"Starting run {run_id}")

    registry = StrategyRegistry(
        strategies_dir=Path(config.strategies_dir),
        game_name=config.game_name,
        models=config.models
    )

    tournament = CulturalEvolution(config.evolution_config, registry)
    result = tournament.run_tournament()

    output_path = _get_run_path(config.output_dir, run_id, config.compress)
    result.save(str(output_path))
    logger.info(f"Completed run {run_id} - saved to {output_path}")

    return run_id, result


class BatchCulturalEvolution:
    """Tournament that runs multiple cultural evolution experiments with incremental saving."""

    def __init__(self, config: BatchCulturalEvolutionConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        self.output_dir = Path(config.output_dir)
        self.runs_dir = self.output_dir / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def run_tournament(self) -> BatchCulturalEvolutionResults:
        """Run all experiments, skipping already completed ones."""
        self.logger.info("Checking for completed runs")

        completed = self._get_completed_runs()
        pending = [i for i in range(self.config.n_runs) if i not in completed]

        self.logger.info(
            f"Batch status: {len(completed)}/{self.config.n_runs} complete, "
            f"{len(pending)} pending"
        )

        if not pending:
            self.logger.info("All runs already completed, loading results")
        else:
            self._run_pending(pending, completed)

        return self._load_all_results()

    def _get_completed_runs(self) -> set[int]:
        """Find which runs have already completed successfully."""
        if not self.runs_dir.exists():
            return set()

        completed = set()
        for run_id in range(self.config.n_runs):
            path = _get_run_path(self.config.output_dir, run_id, self.config.compress)
            if path.exists():
                try:
                    CulturalEvolutionResults.load(str(path))
                    completed.add(run_id)
                except Exception as e:
                    self.logger.warning(f"Run {run_id} file exists but invalid: {e}")
        return completed

    def _run_pending(self, pending: list[int], completed: set[int]):
        """Run pending experiments in parallel."""
        self.logger.info(
            f"Starting {len(pending)} runs with {self.config.n_processes} processes"
        )

        with ProcessPoolExecutor(max_workers=self.config.n_processes) as executor:
            futures = {
                executor.submit(_run_single_experiment, run_id, self.config): run_id
                for run_id in pending
            }

            for future in as_completed(futures):
                run_id = futures[future]
                try:
                    future.result()
                    completed.add(run_id)
                    self.logger.info(
                        f"Run {run_id} completed ({len(completed)}/{self.config.n_runs})"
                    )
                except Exception as e:
                    self.logger.error(f"Run {run_id} failed: {e}")
                    raise

    def _load_all_results(self) -> BatchCulturalEvolutionResults:
        """Load all completed run results from disk."""
        runs = []
        for run_id in range(self.config.n_runs):
            path = _get_run_path(self.config.output_dir, run_id, self.config.compress)
            if path.exists():
                runs.append(CulturalEvolutionResults.load(str(path)))
            else:
                self.logger.warning(f"Missing result for run {run_id}")

        if not runs:
            raise ValueError("No completed runs found")

        return BatchCulturalEvolutionResults(config=self.config, runs=runs)
