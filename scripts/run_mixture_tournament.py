"""Run mixture tournament testing cooperative vs aggressive player ratios."""

import argparse
import importlib.util
import inspect
import logging
import os
import sys
from pathlib import Path

import pandas as pd

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from emergent_llm.tournament.mixture_tournament import MixtureTournament
from emergent_llm.players.base_player import BaseStrategy
from emergent_llm.games.public_goods import PublicGoodsGame, PublicGoodsDescription
from emergent_llm.games.collective_risk import CollectiveRiskGame, CollectiveRiskDescription


def load_strategies_from_file(file_path: str):
    """Load strategy classes from a Python file."""
    if not file_path.endswith(".py"):
        file_path += ".py"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Strategy file not found: {file_path}")

    # Load the module
    spec = importlib.util.spec_from_file_location("strategies", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Extract strategy classes
    cooperative_strategies = []
    aggressive_strategies = []

    for name, cls in inspect.getmembers(module):
        if (inspect.isclass(cls) and
            issubclass(cls, BaseStrategy) and
            cls != BaseStrategy):

            if "COOPERATIVE" in name:
                cooperative_strategies.append(cls)
            elif "AGGRESSIVE" in name:
                aggressive_strategies.append(cls)

    return cooperative_strategies, aggressive_strategies


def create_game_description(game_type: str):
    """Create game description based on type."""
    if game_type == "public_goods":
        return PublicGoodsDescription(
            n_players=6,
            n_rounds=20,
            k=2.0
        )
    elif game_type == "collective_risk":
        return CollectiveRiskDescription(
            n_players=6,
            n_rounds=20,
            m=3,
            k=2.0
        )
    else:
        raise ValueError(f"Unknown game type: {game_type}")


def get_game_class(game_type: str):
    """Get game class based on type."""
    if game_type == "public_goods":
        return PublicGoodsGame
    elif game_type == "collective_risk":
        return CollectiveRiskGame
    else:
        raise ValueError(f"Unknown game type: {game_type}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run mixture tournament")

    parser.add_argument("--strategies", type=str, required=True,
                       help="Path to Python file containing strategy classes")
    parser.add_argument("--game", choices=["public_goods", "collective_risk"],
                       default="public_goods", help="Game type")
    parser.add_argument("--matches", type=int, default=100,
                       help="Number of matches per mixture ratio")
    parser.add_argument("--output", type=str,
                       help="Output CSV file for results (optional)")
    parser.add_argument("--log-file", type=str, default=None,
                       help="Details logs of results (optional)")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    # Setup logging
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')

    try:
        # Load strategies
        print(f"Loading strategies from {args.strategies}...")
        cooperative_strategies, aggressive_strategies = load_strategies_from_file(args.strategies)

        print(f"Found {len(cooperative_strategies)} cooperative strategies")
        print(f"Found {len(aggressive_strategies)} aggressive strategies")

        if not cooperative_strategies or not aggressive_strategies:
            raise ValueError("Need both cooperative and aggressive strategies")

        # Create game components
        game_description = create_game_description(args.game)
        game_class = get_game_class(args.game)

        print(f"Game: {game_description}")
        print(f"Matches per mixture: {args.matches}")

        # Create and run tournament
        tournament = MixtureTournament(
            cooperative_strategies=cooperative_strategies,
            aggressive_strategies=aggressive_strategies,
            game_class=game_class,
            game_description=game_description,
            matches_per_mixture=args.matches,
            log_file=args.log_file,
        )


        print("\nRunning tournament...")
        results_df = tournament.run_mixture_tournament()

        # Print summary
        tournament.print_summary(results_df)  # Pass results_df here

        # Print DataFrame
        print("\nDetailed Results:")
        print(results_df.to_string(index=False, float_format='%.3f'))

        # Save results if requested
        if args.output:
            results_df.to_csv(args.output, index=False)
            print(f"\nResults saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
