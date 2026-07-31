"""Run mixture tournament testing collective vs selfish player ratios."""

import argparse
import logging
import sys
from pathlib import Path

from emergent_llm.generation import StrategyRegistry
from emergent_llm.tournament import (
    BatchMixtureTournament,
    BatchTournamentConfig,
    POOL_SEPARATOR,
)

sys.setrecursionlimit(10000)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run mixture tournament")

    parser.add_argument("--strategies", type=str, nargs="+", required=True,
                        help="Path to Python file containing strategy classes. "
                             "Passing more than one file pools strategies "
                             "across models into a single cross-play "
                             "tournament; the intended use is one file.")
    parser.add_argument("--game", choices=["public_goods", "collective_risk", "common_pool"],
                       default="public_goods", help="Game type")
    parser.add_argument("--matches", type=int, default=100,
                       help="Number of matches per mixture ratio")
    parser.add_argument("--group-sizes", type=int, nargs="+", default=[4, 16, 64],
                       help="Group sizes to test")
    parser.add_argument("--n_processes", type=int, default=1,
                        help="Number of processes to use")
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--output_style", choices=["full", "compressed", "summary"],
                        default="full", help="What compression to apply to the results")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose logging")

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()

    # Extract model name(s) from strategies path(s)
    strategies_paths = [Path(p) for p in args.strategies]
    for path in strategies_paths:
        assert path.suffix == ".py", "strategies file must end in '.py'"

    model_names = sorted(path.stem for path in strategies_paths)
    assert len(set(model_names)) == len(model_names), \
        "duplicate strategy files would double-weight a model in the pool"

    # Single file is self-play, the intended use. Several files pool the
    # strategies of different models into one population: cross-play.
    play_mode = "self_play" if len(model_names) == 1 else "cross_play"
    model_name = POOL_SEPARATOR.join(model_names)

    config = BatchTournamentConfig(
        group_sizes=args.group_sizes,
        repetitions=args.matches,
        generator_name=args.game + "_default",
        n_processes=args.n_processes,
        results_dir=args.results_dir,
        output_style=args.output_style,
        game_name=args.game,
        model_name=model_name,
        play_mode=play_mode,
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

    # Load strategy classes
    collective_specs, selfish_specs = [], []
    for path in strategies_paths:
        logger.info(f"Loading strategies from {path}...")
        collective, selfish = StrategyRegistry.load_file(path)
        logger.info(f"{path.stem}: {len(collective)} collective, "
                    f"{len(selfish)} selfish")
        collective_specs.extend(collective)
        selfish_specs.extend(selfish)

    logger.info(f"Found {len(collective_specs)} collective strategy classes")
    logger.info(f"Found {len(selfish_specs)} selfish strategy classes")

    if not collective_specs or not selfish_specs:
        raise ValueError("Need both collective and selfish strategy classes")

    # Create and run tournament (automatically loads completed groups)
    tournament = BatchMixtureTournament(
        collective_specs=collective_specs,
        selfish_specs=selfish_specs,
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
