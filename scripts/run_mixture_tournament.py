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

from emergent_llm.tournament.multi_group_tournament import MultiGroupTournament, MultiGroupTournamentConfig
from emergent_llm.players.base_player import BaseStrategy
from emergent_llm.common import GameDescription
from emergent_llm.players import LLMPlayer, BasePlayer
from emergent_llm.common import Attitude
from emergent_llm.games.public_goods import PublicGoodsGame, PublicGoodsDescription
from emergent_llm.games.collective_risk import CollectiveRiskGame, CollectiveRiskDescription


def load_strategies_from_file(file_path: str):
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

    return cooperative_strategy_classes, aggressive_strategy_classes


def create_players_from_strategies(cooperative_classes, aggressive_classes, sample_game_desc):
    """Create player instances from strategy classes."""
    cooperative_players = []
    aggressive_players = []

    for i, strategy_class in enumerate(cooperative_classes):
        player = LLMPlayer(f"coop_{strategy_class.__name__}",
                          Attitude.COOPERATIVE,
                          sample_game_desc,  # Just for initialization
                          strategy_class)
        cooperative_players.append(player)

    for i, strategy_class in enumerate(aggressive_classes):
        player = LLMPlayer(f"agg_{strategy_class.__name__}",
                          Attitude.AGGRESSIVE,
                          sample_game_desc,  # Just for initialization
                          strategy_class)
        aggressive_players.append(player)

    return cooperative_players, aggressive_players


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
    parser.add_argument("--group-sizes", type=int, nargs="+", default=[2, 4, 8, 16, 32],
                       help="Group sizes to test")
    parser.add_argument("--output-prefix", type=str, required=True,
                       help="Prefix for output files (e.g., 'results/public_goods/gpt4')")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    # Setup logging
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')

    # Load strategy classes
    print(f"Loading strategies from {args.strategies}...")
    cooperative_classes, aggressive_classes = load_strategies_from_file(args.strategies)

    print(f"Found {len(cooperative_classes)} cooperative strategy classes")
    print(f"Found {len(aggressive_classes)} aggressive strategy classes")

    if not cooperative_classes or not aggressive_classes:
        raise ValueError("Need both cooperative and aggressive strategy classes")

    # Create game description generator function
    def game_description_generator(group_size: int) -> GameDescription:
        if args.game == "public_goods":
            return PublicGoodsDescription(
                n_players=group_size,
                n_rounds=20,
                k=2
            )
        elif args.game == "collective_risk":
            return CollectiveRiskDescription(
                n_players=group_size,
                n_rounds=20,
                m=group_size // 2,
                k=2
            )
        else:
            raise ValueError(f"Unknown game type: {args.game}")

    sample_desc = game_description_generator(group_size=4)

    # Create players
    cooperative_players, aggressive_players = create_players_from_strategies(
        cooperative_classes, aggressive_classes, sample_desc
    )

    # Show parameter scaling
    print(f"Game type: {args.game}")
    print(f"Group sizes: {args.group_sizes}")
    print(f"Matches per mixture: {args.matches}")

    # Create configuration
    config = MultiGroupTournamentConfig(
        game_class=get_game_class(args.game),
        group_sizes=args.group_sizes,
        matches_per_mixture=args.matches,
        output_prefix=args.output_prefix,
        game_description_generator=game_description_generator
    )

    # Create and run tournament
    tournament = MultiGroupTournament(
        cooperative_players=cooperative_players,
        aggressive_players=aggressive_players,
        config=config
    )

    print("\nRunning tournament...")
    results_df = tournament.run_tournament()

    # Save detailed results
    results_file = f"{args.output_prefix}_detailed_results.csv"
    results_df.to_csv(results_file, index=False)
    print(f"\nDetailed results saved to {results_file}")


if __name__ == "__main__":
    main()
