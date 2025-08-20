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

from emergent_llm.tournament.batch_mixture_tournament import BatchMixtureTournament, BatchMixtureTournamentConfig
from emergent_llm.tournament.batch_fair_tournament import BatchFairTournament, BatchFairTournamentConfig
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
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")

    return parser.parse_args()


def setup_results_directory(strategies_path: str, game_type: str) -> tuple[Path, Path, Path]:
    """
    Setup results directory structure based on strategies file and game type.

    Returns:
        tuple: (results_dir, schelling_dir, logs_dir)
    """
    # Extract filename without extension from strategies path
    strategies_filename = Path(strategies_path).stem

    # Create results directory structure
    results_base = Path("results") / game_type / strategies_filename
    schelling_dir = results_base / "schelling"
    logs_dir = results_base / "logs"

    # Create all directories
    results_base.mkdir(parents=True, exist_ok=True)
    schelling_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    return results_base, schelling_dir, logs_dir


def main():
    """Main function."""
    args = parse_arguments()

    # Setup directory structure
    results_dir, schelling_dir, logs_dir = setup_results_directory(args.strategies, args.game)

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

    # Show parameter scaling
    print(f"Game type: {args.game}")
    print(f"Group sizes: {args.group_sizes}")
    print(f"Matches per mixture: {args.matches}")
    print(f"Results will be saved to: {results_dir}")

    # config = BatchMixtureTournamentConfig(
    #     game_class=get_game_class(args.game),
    #     group_sizes=args.group_sizes,
    #     repetitions=args.matches,
    #     results_dir=results_dir,
    #     game_description_generator=game_description_generator
    # )

    # # Create and run tournament
    # tournament = BatchMixtureTournament(
    #     cooperative_strategies=cooperative_classes,
    #     aggressive_strategies=aggressive_classes,
    #     config=config
    # )
    config = BatchFairTournamentConfig(
        game_class=get_game_class(args.game),
        group_sizes=args.group_sizes,
        repetitions=args.matches,
        results_dir=results_dir,
        game_description_generator=game_description_generator
    )

    # Create and run tournament
    tournament = BatchFairTournament(
        cooperative_strategies=cooperative_classes,
        aggressive_strategies=aggressive_classes,
        config=config
    )

    print("\nRunning tournament...")
    results_df = tournament.run_tournament()

    # Save detailed results
    results_df.to_csv(f"{results_dir}/detailed_results.csv", index=False)


if __name__ == "__main__":
    main()
