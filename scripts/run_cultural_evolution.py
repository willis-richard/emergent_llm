"""Example script for running cultural evolution tournament."""
import argparse
import logging
from pathlib import Path

from emergent_llm.common import Gene, Attitude, COOPERATIVE, AGGRESSIVE
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription, CommonPoolDescription, STANDARD_GENERATORS
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.tournament.configs import CulturalEvolutionConfig
from emergent_llm.tournament.cultural_evolution import CulturalEvolutionTournament


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


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run cultural evolution tournament")

    parser.add_argument("--game", type=str, required=True,
                       choices=["public_goods", "collective_risk", "common_pool"],
                       help="Game type")
    parser.add_argument("--strategies_dir", type=str, default="strategies",
                       help="Base directory containing strategy files")
    parser.add_argument("--provider_models", nargs='*', default=None,
                       help="List of provider_models to use, filter out all others in the dir")

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


def create_game_description(args):
    """Create game description from arguments."""
    if args.game == "public_goods":
        return PublicGoodsDescription(
            n_players=args.n_players,
            n_rounds=args.n_rounds,
            k=2.0
        )
    elif args.game == "collective_risk":
        return CollectiveRiskDescription(
            n_players=args.n_players,
            n_rounds=args.n_rounds,
            m=max(2, args.n_players // 2),
            k=2.0
        )
    elif args.game == "common_pool":
        return CommonPoolDescription(
            n_players=args.n_players,
            n_rounds=args.n_rounds,
            capacity=args.n_players * 4
        )
    else:
        raise ValueError(f"Unknown game: {args.game}")


def main():
    """Main function."""
    args = parse_args()

    # Setup output directory
    output_dir = Path(args.output_dir) / args.game
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup logging
    log_file = output_dir / "logs" / "cultural_evolution.log"
    setup_logging(log_file, args.loglevel)
    logger = logging.getLogger(__name__)

    logger.info("Starting cultural evolution experiment")
    logger.info(f"Game: {args.game}")

    print(f"{args.provider_models}, {type(args.provider_models)}")
    assert False

    # Load strategies
    logger.info("Loading strategies...")
    registry = StrategyRegistry(
        strategies_dir=Path(args.strategies_dir),
        game_name=args.game,
        provider_models=args.provider_models
    )

    # Create game description
    game_description = STANDARD_GENERATORS[f"{args.game}_default"](args.n_players, args.n_rounds)
    logger.info(f"Game description: {game_description}")

    # Create tournament config
    config = CulturalEvolutionConfig(
        game_description=game_description,
        population_size=args.population_size,
        top_k=args.top_k,
        mutation_rate=args.mutation_rate,
        threshold_pct=args.threshold_pct,
        max_generations=args.max_generations,
        repetitions_per_generation=args.repetitions
    )

    # Run tournament
    logger.info("Starting tournament...")
    tournament = CulturalEvolutionTournament(config, registry)
    results = tournament.run_tournament()

    # Save results
    logger.info("Saving results...")
    results_file = output_dir / "results.json"
    results.save(str(results_file))

    # Plot gene frequencies
    logger.info("Creating plots...")
    results.plots(output_dir)

    # Print summary
    print("\n" + "="*60)
    print(results)
    print("="*60)

    logger.info("Experiment complete")

    for fair in results.generation_results:
        print(fair)


if __name__ == "__main__":
    main()
