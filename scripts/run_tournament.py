"""Run mixture tournament testing collective vs exploitative player ratios."""

import argparse
import logging
import sys
from pathlib import Path

from emergent_llm.generation import StrategyRegistry
from emergent_llm.tournament import (
    BatchMixtureTournament,
    BatchMixtureTournamentResults,
    BatchTournamentConfig,
)

import sys
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
    parser.add_argument("--processes", type=int, default=1,
                       help="Number of processes to use")
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--output_style", choices=["full", "compress", "summary"],
                       default="full", help="What compression to apply to the results")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")
    parser.add_argument("--load", action="store_true",
                       help="Try to load instead of recomputing")

    return parser.parse_args()


def setup_output_directory(results_dir: str, strategies_path: str, game_type: str) -> tuple[Path, Path]:
    """
    Setup results directory structure based on strategies file and game type.

    Returns:
        tuple: (results_dir, logs_dir)
    """
    # Extract filename without extension from strategies path
    assert Path(strategies_path).suffix == ".py", "strategies file must end in '.py'"
    strategies_filename = Path(strategies_path).stem

    # Create results directory structure
    output_dir = Path(results_dir) / "self_play" / game_type / strategies_filename
    logs_dir = output_dir / "logs"

    # Create all directories
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    return output_dir, logs_dir


def main():
    """Main function."""
    args = parse_arguments()

    # Setup directory structure
    output_dir, logs_dir = setup_output_directory(args.results_dir, args.strategies, args.game)

    # Setup logging to file
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
    logger.info(f"Starting batch cultural evolution: {args.game}")

    if args.load:
        results = BatchMixtureTournamentResults.load(output_dir)
        logger.info(f"Loaded results from {output_dir}")
    else:

        # Load strategy classes
        logger.info(f"Loading strategies from {args.strategies}...")
        collective_specs, exploitative_specs = StrategyRegistry.load_file(args.strategies)

        logger.info(f"Found {len(collective_specs)} collective strategy classes")
        logger.info(f"Found {len(exploitative_specs)} exploitative strategy classes")

        if not collective_specs or not exploitative_specs:
            raise ValueError("Need both collective and exploitative strategy classes")

        config = BatchTournamentConfig(
            group_sizes=args.group_sizes,
            repetitions=args.matches,
            generator_name=args.game + "_default",
            processes=args.processes,
            output_dir=str(output_dir),
            output_style=args.output_style,
        )

        # Create and run tournament
        tournament = BatchMixtureTournament(
            collective_specs=collective_specs,
            exploitative_specs=exploitative_specs,
            config=config
        )

        logger.info("Running tournament...")
        results = tournament.run_tournament()
        results.save()

    results.create_schelling_diagrams()
    results.create_relative_schelling_diagram()
    results.create_social_welfare_diagram()

    logger.info(f"\nRun complete {args.strategies}...")


if __name__ == "__main__":
    main()
