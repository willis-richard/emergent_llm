"""Batch cultural evolution tournament with incremental saving."""
import logging
import signal
from multiprocessing import Pool
from pathlib import Path

from emergent_llm.generation import StrategyRegistry
from emergent_llm.tournament.configs import BatchCulturalEvolutionConfig
from emergent_llm.tournament.cultural_evolution import CulturalEvolution
from emergent_llm.tournament.results import BatchCulturalEvolutionResults, CulturalEvolutionResults


def _get_run_dir(output_dir: Path, run_id: int) -> Path:
    """Get directory for a specific run's results."""
    return Path(output_dir) / "runs" / f"run_{run_id:04d}"


def _run_single_experiment(
    run_id: int,
    config: BatchCulturalEvolutionConfig,
) -> tuple[int, CulturalEvolutionResults]:
    """Worker function that runs a single evolution experiment."""
    logger = logging.getLogger(f"Run-{run_id}")
    logger.info(f"Starting run {run_id}")

    registry = StrategyRegistry(strategies_dir=Path(config.strategies_dir),
                                game_name=config.game_name,
                                models=config.models)

    tournament = CulturalEvolution(config.evolution_config, registry)
    result = tournament.run_tournament()

    run_dir = _get_run_dir(config.output_dir, run_id)
    result.save(run_dir, config.output_style)
    logger.info(f"Completed run {run_id} - saved to {run_dir}")

    return run_id, result


def _worker_init():
    """Ignore SIGINT in workers; let parent handle it."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


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
            f"{len(pending)} pending")

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
            run_dir = _get_run_dir(self.config.output_dir, run_id)
            if run_dir.exists():
                try:
                    CulturalEvolutionResults.load(run_dir)
                    completed.add(run_id)
                except Exception as e:
                    self.logger.warning(
                        f"Run {run_id} dir exists but invalid: {e}")
        return completed

    def _run_pending(self, pending: list[int], completed: set[int]):
        """Run pending experiments in parallel."""
        self.logger.info(
            f"Starting {len(pending)} runs with {self.config.n_processes} processes"
        )

        with Pool(self.config.n_processes, initializer=_worker_init) as pool:
            try:
                results = pool.starmap(_run_single_experiment,
                                       [(rid, self.config) for rid in pending])
            except KeyboardInterrupt:
                pool.terminate()
                raise

    def _load_all_results(self) -> BatchCulturalEvolutionResults:
        """Load all completed run results from disk."""
        runs = []
        for run_id in range(self.config.n_runs):
            run_dir = _get_run_dir(self.config.output_dir, run_id)
            if run_dir.exists():
                runs.append(CulturalEvolutionResults.load(run_dir))
            else:
                self.logger.warning(f"Missing result for run {run_id}")

        if not runs:
            raise ValueError("No completed runs found")

        return BatchCulturalEvolutionResults(config=self.config, runs=runs)
