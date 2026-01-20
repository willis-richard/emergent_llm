"""Run mixture tournament testing collective vs exploitative player ratios."""

import argparse
import logging
import sys
from pathlib import Path

from emergent_llm.generation import StrategyRegistry
from emergent_llm.tournament import (
    BatchMixtureTournament,
    BatchTournamentConfig,
)

sys.setrecursionlimit(10000)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run mixture tournament")

    parser.add_argument("--strategies", type=str, required=True,
                       help="Path to Python file containing strategy classes")
    parser.add_argument("--game", choices=["public_goods", "collective_risk", "common_pool"],
                       default="public_goods", help="Game type")
    parser.add_argument("--matches", type=int, default=100,
                       help="Number of matches per mixture ratio")
    parser.add_argument("--group-sizes", type=int, nargs="+", default=[4, 16, 64],
                       help="Group sizes to test")
    parser.add_argument("--n_processes", type=int, default=1,
                        help="Number of processes to use")
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--output_style", choices=["full", "compress", "summary"],
                        default="full", help="What compression to apply to the results")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose logging")

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    # Extract model name from strategies path
    strategies_path = Path(args.strategies)
    assert strategies_path.suffix == ".py", "strategies file must end in '.py'"
    model_name = strategies_path.stem

    config = BatchTournamentConfig(
        group_sizes=args.group_sizes,
        repetitions=args.matches,
        generator_name=args.game + "_default",
        n_processes=args.n_processes,
        results_dir=args.results_dir,
        output_style=args.output_style,
        game_name=args.game,
        model_name=model_name,
    )

    # Setup logging
    logs_dir = config.output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "tournament.log"

    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Starting batch mixture tournament: {args.game}")
    logger.info(f"Output directory: {config.output_dir}")

    # Load strategy classes
    logger.info(f"Loading strategies from {args.strategies}...")
    collective_specs, exploitative_specs = StrategyRegistry.load_file(args.strategies)

    logger.info(f"Found {len(collective_specs)} collective strategy classes")
    logger.info(f"Found {len(exploitative_specs)} exploitative strategy classes")

    if not collective_specs or not exploitative_specs:
        raise ValueError("Need both collective and exploitative strategy classes")

    # Create and run tournament (automatically loads completed groups)
    tournament = BatchMixtureTournament(
        collective_specs=collective_specs,
        exploitative_specs=exploitative_specs,
        config=config
    )

    logger.info("Running tournament...")
    results = tournament.run_tournament()

    results.save()
    logger.info(f"Saved batch results to {config.output_dir}")

    results.create_schelling_diagrams()
    results.create_relative_schelling_diagram()
    results.create_social_welfare_diagram()

    logger.info(f"\nRun complete {args.strategies}...")


if __name__ == "__main__":
    main()
