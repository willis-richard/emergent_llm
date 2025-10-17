"""Run mixture tournament testing cooperative vs aggressive player ratios."""

import argparse
import importlib.util
import inspect
import logging
import os
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from emergent_llm.games import (CollectiveRiskGame, CommonPoolGame,
                                PublicGoodsGame)
from emergent_llm.players import BaseStrategy
from emergent_llm.tournament import (BatchMixtureTournament,
                                     BatchTournamentConfig)
from emergent_llm.generation import StrategyRegistry


def get_game_class(game_type: str):
    """Get game class based on type."""
    if game_type == "public_goods":
        return PublicGoodsGame
    elif game_type == "collective_risk":
        return CollectiveRiskGame
    elif game_type == "common_pool":
        return CommonPoolGame
    else:
        raise ValueError(f"Unknown game type: {game_type}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run mixture tournament")

    parser.add_argument("--strategies", type=str, required=True,
                       help="Path to Python file containing strategy classes")
    parser.add_argument("--game", choices=["public_goods", "collective_risk", "common_pool"],
                       default="public_goods", help="Game type")
    parser.add_argument("--matches", type=int, default=100,
                       help="Number of matches per mixture ratio")
    parser.add_argument("--group-sizes", type=int, nargs="+", default=[2, 4, 8, 16, 32],
                       help="Group sizes to test")
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
    results_base = Path("results") / game_type / strategies_filename
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
    cooperative_specs, aggressive_specs = StrategyRegistry.load_file(args.strategies)

    print(f"Found {len(cooperative_specs)} cooperative strategy classes")
    print(f"Found {len(aggressive_specs)} aggressive strategy classes")

    if not cooperative_specs or not aggressive_specs:
        raise ValueError("Need both cooperative and aggressive strategy classes")

    # Show parameter scaling
    print(f"Game type: {args.game}")
    print(f"Group sizes: {args.group_sizes}")
    print(f"Matches per mixture: {args.matches}")
    print(f"Results will be saved to: {results_dir}")

    config = BatchTournamentConfig(
        group_sizes=args.group_sizes,
        repetitions=args.matches,
        results_dir=str(results_dir),
        generator_name=args.game + "_default"
    )

    # Create and run tournament
    tournament = BatchMixtureTournament(
        cooperative_specs=cooperative_specs,
        aggressive_specs=aggressive_specs,
        config=config
    )

    print("\nRunning tournament...")
    results = tournament.run_tournament()
    results.save()
    results.create_schelling_diagrams()
    results.create_social_welfare_diagram()


if __name__ == "__main__":
    main()
