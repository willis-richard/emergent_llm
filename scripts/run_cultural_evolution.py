"""Run multiple cultural evolution experiments with incremental saving."""
import argparse
import logging
from pathlib import Path

from emergent_llm.games import STANDARD_GENERATORS
from emergent_llm.tournament import (
    BatchCulturalEvolutionConfig,
    BatchCulturalEvolution,
    CulturalEvolutionConfig,
)


def setup_logging(log_file: Path, loglevel=logging.INFO):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file),
                  logging.StreamHandler()])


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run parallel cultural evolution tournaments")

    parser.add_argument(
        "--game",
        type=str,
        required=True,
        choices=["public_goods", "collective_risk", "common_pool"],
        help="Game type")
    parser.add_argument("--strategies_dir",
                        type=str,
                        default="strategies",
                        help="Base directory containing strategy files")
    parser.add_argument("--models",
                        nargs='*',
                        default=None,
                        help="List of models to use, filter out all others")

    # Game parameters
    parser.add_argument("--n_players",
                        type=int,
                        default=16,
                        help="Number of players per game")
    parser.add_argument("--n_rounds",
                        type=int,
                        default=20,
                        help="Number of rounds per game")

    # Evolution parameters
    parser.add_argument("--population_size",
                        type=int,
                        default=128,
                        help="Total population size")
    parser.add_argument("--beta",
                        type=int,
                        default=1,
                        help="Selection strength")
    parser.add_argument("--mutation_rate",
                        type=float,
                        default=0.0025,
                        help="Probability of mutation")
    parser.add_argument("--n_generations",
                        type=int,
                        default=200,
                        help="Maximum number of generations")
    parser.add_argument("--final_window",
                        type=int,
                        default=50,
                        help="Number of generations to average over")
    parser.add_argument("--games_per_agent",
                        type=int,
                        default=10,
                        help="Games per player per generation")

    # Parallel execution parameters
    parser.add_argument("--n_runs",
                        type=int,
                        default=10,
                        help="Number of independent runs")
    parser.add_argument("--n_processes",
                        type=int,
                        default=4,
                        help="Number of parallel processes")

    # Output
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--output_style", choices=["full", "compress", "summary"],
                        default="full", help="What compression to apply to the results")
    parser.add_argument("--log_level",
                        type=str,
                        default="INFO",
                        help="Logging level to use")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    game_description = STANDARD_GENERATORS[f"{args.game}_default"](
        args.n_players, args.n_rounds)

    evolution_config = CulturalEvolutionConfig(
        game_description=game_description,
        population_size=args.population_size,
        beta=args.beta,
        mutation_rate=args.mutation_rate,
        n_generations=args.n_generations,
        final_window=args.final_window,
        games_per_agent=args.games_per_agent)

    batch_config = BatchCulturalEvolutionConfig(
        evolution_config=evolution_config,
        n_runs=args.n_runs,
        n_processes=args.n_processes,
        results_dir=args.results_dir,
        output_style=args.output_style,
        strategies_dir=args.strategies_dir,
        game_name=args.game,
        models=args.models)

    log_file = batch_config.output_dir / "logs" / "batch_evolution.log"
    setup_logging(log_file, args.log_level)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting batch cultural evolution: {args.game}")
    logger.info(f"Runs: {args.n_runs}, Processes: {args.n_processes}")

    tournament = BatchCulturalEvolution(batch_config)
    results = tournament.run_tournament()

    # Save aggregated results
    results.save()
    results.plots()

    print("\n" + "=" * 60)
    print(results)
    print("=" * 60)
    print(f"\nResults saved to: {batch_config.output_dir}")
