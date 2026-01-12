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
    parser.add_argument("--processes", type=int, default=1,
                       help="Number of processes to use")
    parser.add_argument("--group-sizes", type=int, nargs="+", default=[4, 16, 64],
                       help="Group sizes to test")
    parser.add_argument("--compress",
                        action="store_true",
                        help="Whether the outputs should be compressed")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")

    return parser.parse_args()


def setup_results_directory(strategies_path: str, game_type: str) -> tuple[Path, Path]:
    """
    Setup results directory structure based on strategies file and game type.

    Returns:
        tuple: (results_dir, logs_dir)
    """
    # Extract filename without extension from strategies path
    assert Path(strategies_path).suffix == ".py", "strategies file must end in '.py'"
    strategies_filename = Path(strategies_path).stem

    # Create results directory structure
    results_base = Path("results/self_play") / game_type / strategies_filename
    logs_dir = results_base / "logs"

    # Create all directories
    results_base.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    return results_base, logs_dir


def main():
    """Main function."""
    args = parse_arguments()

    # Setup directory structure
    results_dir, logs_dir = setup_results_directory(args.strategies, args.game)

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

    # Load strategy classes
    print(f"Loading strategies from {args.strategies}...")
    collective_specs, exploitative_specs = StrategyRegistry.load_file(args.strategies)

    print(f"Found {len(collective_specs)} collective strategy classes")
    print(f"Found {len(exploitative_specs)} exploitative strategy classes")

    if not collective_specs or not exploitative_specs:
        raise ValueError("Need both collective and exploitative strategy classes")

    # Show parameter scaling
    print(f"Game type: {args.game}")
    print(f"Group sizes: {args.group_sizes}")
    print(f"Matches per mixture: {args.matches}")
    print(f"Results will be saved to: {results_dir}")

    config = BatchTournamentConfig(
        group_sizes=args.group_sizes,
        repetitions=args.matches,
        processes=args.processes,
        results_dir=str(results_dir),
        compress=args.compress,
        generator_name=args.game + "_default"
    )

    # Create and run tournament
    tournament = BatchMixtureTournament(
        collective_specs=collective_specs,
        exploitative_specs=exploitative_specs,
        config=config
    )

    print("\nRunning tournament...")
    results = tournament.run_tournament()
    results.save()

    # results = BatchMixtureTournamentResults.load(results_dir / "batch_mixture/results.json")

    results.create_schelling_diagrams()
    results.create_relative_schelling_diagram()
    results.create_social_welfare_diagram()

    print(f"\nRun complete {args.strategies}...")


if __name__ == "__main__":
    main()
