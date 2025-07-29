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
from emergent_llm.common import GameDescription
from emergent_llm.players import LLMPlayer, BasePlayer
from emergent_llm.common import Attitude
from emergent_llm.games.public_goods import PublicGoodsGame, PublicGoodsDescription
from emergent_llm.games.collective_risk import CollectiveRiskGame, CollectiveRiskDescription



def load_strategies_from_file(file_path: str, game_description: GameDescription):
    """Load strategy classes and create player instances."""
    if not file_path.endswith(".py"):
        file_path += ".py"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Strategy file not found: {file_path}")

    # Load the module
    spec = importlib.util.spec_from_file_location("strategies", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Extract strategy classes
    cooperative_strategy_classes = []
    aggressive_strategy_classes = []

    for name, cls in inspect.getmembers(module):
        if (inspect.isclass(cls) and
            issubclass(cls, BaseStrategy) and
            cls != BaseStrategy):

            if "COOPERATIVE" in name:
                cooperative_strategy_classes.append(cls)
            elif "AGGRESSIVE" in name:
                aggressive_strategy_classes.append(cls)

    # Create player instances from strategy classes
    cooperative_players = []
    aggressive_players = []

    for i, strategy_class in enumerate(cooperative_strategy_classes):
        player = LLMPlayer(f"coop_{strategy_class.__name__}",
                          Attitude.COOPERATIVE,
                          game_description,
                          strategy_class)
        cooperative_players.append(player)

    for i, strategy_class in enumerate(aggressive_strategy_classes):
        player = LLMPlayer(f"agg_{strategy_class.__name__}",
                          Attitude.AGGRESSIVE,
                          game_description,
                          strategy_class)
        aggressive_players.append(player)

    return cooperative_players, aggressive_players



def create_game_description(game_type: str):
    """Create game description based on type."""
    if game_type == "public_goods":
        return PublicGoodsDescription(
            n_players=2,
            n_rounds=20,
            k=1.5
        )
    elif game_type == "collective_risk":
        return CollectiveRiskDescription(
            n_players=6,
            n_rounds=20,
            m=4,
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
        # Create game components first
        game_description = create_game_description(args.game)
        game_class = get_game_class(args.game)

        # Load players (passing game_description)
        print(f"Loading strategies from {args.strategies}...")
        cooperative_players, aggressive_players = load_strategies_from_file(args.strategies, game_description)

        print(f"Found {len(cooperative_players)} cooperative players")
        print(f"Found {len(aggressive_players)} aggressive players")

        if not cooperative_players or not aggressive_players:
            raise ValueError("Need both cooperative and aggressive players")

        print(f"Game: {game_description}")
        print(f"Matches per mixture: {args.matches}")

        # Create and run tournament
        tournament = MixtureTournament(
            cooperative_players=cooperative_players,
            aggressive_players=aggressive_players,
            game_class=game_class,
            game_description=game_description,
            matches_per_mixture=args.matches,
            log_file=args.log_file,
        )

        print("\nRunning tournament...")
        results_df = tournament.run_mixture_tournament()

        # Print summary
        tournament.print_summary(results_df)

        # Save results if requested
        if args.output:
            results_df.to_csv(args.output, index=False)
            print(f"\nResults saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
