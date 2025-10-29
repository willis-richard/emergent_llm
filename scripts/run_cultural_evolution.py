"""Run multiple cultural evolution experiments in parallel."""
import argparse
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from pathlib import Path

from emergent_llm.games import STANDARD_GENERATORS
from emergent_llm.generation import StrategyRegistry
from emergent_llm.tournament import (
    CulturalEvolutionConfig,
    CulturalEvolutionResults,
    CulturalEvolutionTournament,
    MultiRunCulturalEvolutionResults,
)


def setup_logging(log_file: Path, loglevel=logging.INFO):
    """Setup logging configuration."""
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def run_single_experiment(run_id: int, config: CulturalEvolutionConfig,
                         strategies_dir: Path, game_name: str,
                         models: list[str] | None) -> tuple[int, CulturalEvolutionResults]:
    """
    Run a single cultural evolution experiment.

    Args:
        run_id: Identifier for this run
        config: Tournament configuration
        strategies_dir: Base directory containing strategy files
        game_name: Name of game subdirectory
        models: Optional list of models to filter by

    Returns:
        Tuple of (run_id, results)
    """
    # Setup logging for this process
    logger = logging.getLogger(f"Run-{run_id}")
    logger.info(f"Starting run {run_id}")

    # Load strategies
    registry = StrategyRegistry(
        strategies_dir=strategies_dir,
        game_name=game_name,
        models=models
    )

    # Run tournament
    tournament = CulturalEvolutionTournament(config, registry)
    results = tournament.run_tournament()

    logger.info(f"Completed run {run_id} - Generation: {results.final_generation}")

    return run_id, results


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run parallel cultural evolution tournaments")

    parser.add_argument("--game", type=str, required=True,
                       choices=["public_goods", "collective_risk", "common_pool"],
                       help="Game type")
    parser.add_argument("--strategies_dir", type=str, default="strategies",
                       help="Base directory containing strategy files")
    parser.add_argument("--models", nargs='*', default=None,
                       help="List of models to use, filter out all others")

    # Game parameters
    parser.add_argument("--n_players", type=int, default=16,
                       help="Number of players per game")
    parser.add_argument("--n_rounds", type=int, default=20,
                       help="Number of rounds per game")

    # Evolution parameters
    parser.add_argument("--population_size", type=int, default=128,
                       help="Total population size")
    parser.add_argument("--top_k", type=int, default=16,
                       help="Number of survivors per generation")
    parser.add_argument("--mutation_rate", type=float, default=0.1,
                       help="Probability of mutation")
    parser.add_argument("--threshold_pct", type=float, default=0.75,
                       help="Termination threshold (0-1)")
    parser.add_argument("--max_generations", type=int, default=100,
                       help="Maximum number of generations")
    parser.add_argument("--repetitions", type=int, default=5,
                       help="Games per player per generation")

    # Parallel execution parameters
    parser.add_argument("--n_runs", type=int, default=10,
                       help="Number of independent runs")
    parser.add_argument("--n_processes", type=int, default=4,
                       help="Number of parallel processes")

    # Output
    parser.add_argument("--output_dir", type=str, default="results/cultural_evolution",
                       help="Output directory for results")
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.INFO,
    )

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()

    # Setup output directory
    output_dir = Path(args.output_dir) / args.game
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup logging
    log_file = output_dir / "logs" / "parallel_evolution.log"
    setup_logging(log_file, args.loglevel)
    logger = logging.getLogger(__name__)

    logger.info("Starting parallel cultural evolution experiment")
    logger.info(f"Game: {args.game}")
    logger.info(f"Runs: {args.n_runs}, Processes: {args.n_processes}")

    # Create game description
    game_description = STANDARD_GENERATORS[f"{args.game}_default"](args.n_players, args.n_rounds)
    logger.info(f"Game description: {game_description}")

    # Create tournament config (shared across all runs)
    config = CulturalEvolutionConfig(
        game_description=game_description,
        population_size=args.population_size,
        top_k=args.top_k,
        mutation_rate=args.mutation_rate,
        threshold_pct=args.threshold_pct,
        max_generations=args.max_generations,
        repetitions_per_generation=args.repetitions
    )

    # Run experiments in parallel
    logger.info("Starting parallel execution...")
    results_list = []

    # Create partial function with fixed arguments
    run_func = partial(
        run_single_experiment,
        config=config,
        strategies_dir=Path(args.strategies_dir),
        game_name=args.game,
        models=args.models
    )

    with ProcessPoolExecutor(max_workers=args.n_processes) as executor:
        # Submit all jobs
        futures = {executor.submit(run_func, run_id): run_id
                  for run_id in range(args.n_runs)}

        # Collect results as they complete
        for future in as_completed(futures):
            run_id = futures[future]
            try:
                completed_run_id, result = future.result()
                results_list.append(result)
                logger.info(f"Run {completed_run_id} completed successfully "
                          f"({len(results_list)}/{args.n_runs})")
            except Exception as e:
                logger.error(f"Run {run_id} failed with error: {e}")
                raise

    if not results_list:
        logger.error("No runs completed successfully")
        return

    logger.info(f"All runs complete. {len(results_list)}/{args.n_runs} succeeded")

    # Create multi-run results
    multi_results = MultiRunCulturalEvolutionResults(runs=results_list)

    # Save results
    logger.info("Saving results...")
    results_file = output_dir / "multi_run_results.json"
    multi_results.save(str(results_file))

    # Create termination analysis
    logger.info("Creating termination analysis...")
    termination_df = multi_results.analyze_termination()
    termination_file = output_dir / "termination_analysis.csv"
    termination_df.to_csv(termination_file, index=False)
    logger.info(f"Termination analysis saved to {termination_file}")

    # Generate plots
    logger.info("Creating plots...")
    multi_results.plots(output_dir)

    # Print summary
    print("\n" + "="*60)
    print(multi_results)
    print("="*60)
    print(f"\nResults saved to: {output_dir}")
    print(f"Termination analysis: {termination_file}")

    logger.info("Experiment complete")


if __name__ == "__main__":
    main()
