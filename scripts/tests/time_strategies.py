import argparse

from emergent_llm.generation import StrategyRegistry, test_strategy_class


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game_name", type=str, required=True,
                       choices=["public_goods", "collective_risk", "common_pool"],
                       help="Game type")
    parser.add_argument("--strategies_dir", type=str, default="strategies",
                       help="Base directory containing strategy files")
    parser.add_argument("--models", nargs='*', default=None,
                       help="List of models to use, filter out all others")
    return parser.parse_args()

def main():
    args = parse_arguments()

    registry = StrategyRegistry(
        strategies_dir=args.strategies_dir,
        game_name=args.game_name,
        models=args.models
    )

    for gene in registry.available_genes:
        print(gene, registry.count_strategies(gene))

    times = []

    for gene in registry.available_genes:
        for strategy_spec in registry.get_all_specs(gene):
            total_time = test_strategy_class(strategy_spec.strategy_class, args.game_name, None)
            print(strategy_spec.strategy_class.__name__, total_time)
            times.append((strategy_spec.strategy_class.__name__, total_time))

    times.sort(key=lambda tup: tup[1], reverse=True)
    print(times[0:10])


if __name__ == '__main__':
    main()
