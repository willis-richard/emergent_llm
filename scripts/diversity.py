# pylint: disable=redefined-outer-name,missing-function-docstring,missing-class-docstring,possibly-used-before-assignment

import argparse
from functools import partial
from itertools import combinations_with_replacement, product
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA

from emergent_llm.common import (
    Action,
    C,
    D,
    GameDescription,
    GameHistory,
    GameState,
    Gene,
    PlayerHistory,
)
from emergent_llm.games import STANDARD_GENERATORS, get_game_types
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import (
    ConditionalCooperator,
    Cooperator,
    Defector,
    HistoricalCooperator,
    LLMPlayer,
    SimplePlayer,
    SpecialRounds,
)

OpponentActions = tuple[tuple[Action, ...], ...]


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run PCA for strategies")

    parser.add_argument(
        "--game",
        type=str,
        required=True,
        choices=["public_goods", "collective_risk", "common_pool"],
        help="Game type")
    parser.add_argument("--strategies_dir",
                        type=str,
                        default="strategies",
                        help="Base directory containing strategy files")
    parser.add_argument("--models",
                        nargs='*',
                        default=None,
                        help="List of models to use, filter out all others")
    parser.add_argument("--n_strategies",
                        type=int,
                        default=None,
                        help="Limit the analysis to this many strategies")

    # Game parameters
    parser.add_argument("--n_players",
                        type=int,
                        default=4,
                        help="Number of players per game")
    parser.add_argument("--n_rounds",
                        type=int,
                        default=5,
                        help="Number of rounds per game")
    parser.add_argument("--n_games",
                        type=int,
                        default=20,
                        help="Number of games for each trajectory")

    # Parallel execution parameters
    parser.add_argument("--n_processes",
                        type=int,
                        default=1,
                        help="Number of parallel processes")

    return parser.parse_args()


class FixedOpponent:

    def __init__(self, fixed_actions):
        self.fixed_actions: list[Action] = fixed_actions

    def __call__(self, state: GameState, _: PlayerHistory | None):
        return self.fixed_actions[state.round_number]


def context_to_key(arr: list[list[Action]]) -> OpponentActions:
    return tuple(map(tuple, arr))


def play_games(player: LLMPlayer, n_games: int,
               combo: OpponentActions) -> list[GameHistory]:
    # last round action of opponents does not matter
    opponents = [
        SimplePlayer(f"opponent_{i+1}", FixedOpponent(list(actions) + [C]))
        for i, actions in enumerate(combo)
    ]

    players = [player] + opponents
    histories = [
        game_class(players, description).play_game().history
        for _ in range(n_games)
    ]
    return histories


def compute_features(player: LLMPlayer, n_games: int) -> dict[OpponentActions, float]:
    features = {}
    for combo in unique_combos:
        histories = play_games(player, n_games, combo)
        player_history = histories[0].for_player(0)
        for r in range(0, args.n_rounds):
            context = Action.from_bool_array(
                player_history.opponent_actions[:r])
            actions = [Action(history.actions[r, 0]) for history in histories]
            features[context_to_key(context)] = float(
                Action.to_bool_array(actions).mean())
    return features


def compute_gene(gene: Gene) -> dict[str, dict[OpponentActions, float]]:
    strategy_features = {}
    for strategy_spec in registry.get_all_specs(gene)[0:args.n_strategies]:
        algo = strategy_spec.strategy_class
        player = LLMPlayer("testing", gene, description, algo)

        features = compute_features(player, args.n_games)
        strategy_features[algo.__name__] = features

        print(
            f"{gene.model} {algo.__name__}: {np.mean(list(features.values()))}")
    return strategy_features


# yapf: disable
def create_baseline_players():
    baseline_players = [
        SimplePlayer("All-D", Defector),
        SimplePlayer("All-C", Cooperator),
        SimplePlayer("LR-All-C", SpecialRounds(Cooperator, Defector, [args.n_rounds-1])),
    ]
    baseline_players += [SimplePlayer(f"CC-{i}", ConditionalCooperator(C, i)) for i in range(1, args.n_players)]
    baseline_players += [SimplePlayer(f"HC-{i}", HistoricalCooperator(C, i)) for i in range(1, args.n_players)]
    baseline_players += [SimplePlayer(f"S-CC-{i}", ConditionalCooperator(C, i, True)) for i in range(2, args.n_players+1)]
    baseline_players += [SimplePlayer(f"S-HC-{i}", HistoricalCooperator(C, i, True)) for i in range(2, args.n_players+1)]
    # baseline_players += [SimplePlayer(f"C-AntiTFT-{i}", AntiTFT(C, i)) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"D-AntiTFT-{i}", AntiTFT(D, i)) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"Grim-{i}", Grim(C, i)) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"AntiGrim-{i}", AntiGrim(D, i)) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"D-FirstImpressions-{i}", FirstImpressions(D, i)) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"1C-Flip-CC-{i}", Flipper(C, 1, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"1D-Flip-CC-{i}", Flipper(D, 1, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"2C-Flip-CC-{i}", Flipper(C, 2, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"2D-Flip-CC-{i}", Flipper(D, 2, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
    # baseline_players += [SimplePlayer(f"{a}-Alternator", Altenator(a)) for a in [C,D]]
    baseline_players += [SimplePlayer(f"LR-CC-{i}", SpecialRounds(ConditionalCooperator(C, i), Defector, [args.n_rounds-1])) for i in range(1, args.n_players)]
    baseline_players += [SimplePlayer(f"LR-HC-{i}", SpecialRounds(HistoricalCooperator(C, i), Defector, [args.n_rounds-1])) for i in range(1, args.n_players)]
    baseline_players += [SimplePlayer(f"test-3", SpecialRounds(HistoricalCooperator(C, 3, True), ConditionalCooperator(C, 1), [args.n_rounds-1]))]

    return baseline_players
# yapf: enable


def compute_baselines() -> dict[str, dict[OpponentActions, float]]:
    baseline_players = create_baseline_players()
    baseline_features = {}
    for player in baseline_players:
        features = compute_features(player, 1)
        baseline_features[player.id.name] = features

        mean = np.mean(list(features.values()))
        print(f"{player.id.name}: {mean}")
    return baseline_features


def plot_covariance_ellipse(ax, mean, cov, n_std=1.0, **kwargs):
    """Plot covariance ellipse at n_std standard deviations."""
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(eigenvalues)
    ellipse = Ellipse(mean, width, height, angle=angle, **kwargs)
    ax.add_patch(ellipse)
    return ellipse


def find_extrema(X_pca, metadata):
    """Find strategies at plot extrema."""
    extrema_indices = {
        'top_left': np.argmin(X_pca[:, 0] - X_pca[:, 1]),
        'top_right': np.argmax(X_pca[:, 0] + X_pca[:, 1]),
        'bottom_left': np.argmin(X_pca[:, 0] + X_pca[:, 1]),
        'bottom_right': np.argmax(X_pca[:, 0] - X_pca[:, 1]),
    }

    results = {}
    for position, idx in extrema_indices.items():
        gene, strategy_name, feature_dict = metadata[idx]

        results[position] = {
            'idx': idx,
            'gene': str(gene),
            'strategy': strategy_name,
            'coords': (X_pca[idx, 0], X_pca[idx, 1]),
            'features': feature_dict
        }

        print(f"\n{position.upper().replace('_', ' ')}:")
        print(f"  Gene: {gene}")
        print(f"  Strategy: {strategy_name}")
        print(f"  PC1: {X_pca[idx, 0]:.3f}, PC2: {X_pca[idx, 1]:.3f}")

        coop_rate = np.mean(list(feature_dict.values()))
        print(f"  Overall cooperation rate: {coop_rate:.2%}")

    return results


if __name__ == "__main__":

    args = parse_args()

    game_class, _ = get_game_types(args.game)
    description = STANDARD_GENERATORS[args.game + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    # Load strategies
    registry = StrategyRegistry(strategies_dir=args.strategies_dir,
                                game_name=args.game,
                                models=args.models)

    genes = list(registry.available_genes)

    all_actions = tuple(
        combination for combination in product([D, C], repeat=args.n_rounds -
                                               1))
    print(len(all_actions))

    unique_combos: tuple[OpponentActions, ...] = tuple(
        combinations_with_replacement(all_actions, args.n_players - 1))
    print(len(unique_combos))

    baseline_features = compute_baselines()

    with Pool(processes=args.n_processes) as pool:
        results = pool.map(compute_gene, genes)

    # PCA
    X_list = []
    labels = []
    metadata = []

    for gene, strategy_features in zip(genes, results):
        for strategy_name, feature_dict in strategy_features.items():
            X_list.append(list(feature_dict.values()))
            labels.append(str(gene))
            metadata.append((gene, strategy_name, feature_dict))

    X = np.array(X_list)
    labels = np.array(labels)

    pca = PCA(n_components=10)
    X_pca = pca.fit_transform(X)
    print(pca.explained_variance_ratio_[:5])

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot generated algorithms by behaviour
    handles = []
    colors = plt.colormaps.get_cmap('tab10')(np.linspace(0, 1, len(genes)))

    for i, gene in enumerate(genes):
        mask = labels == str(gene)
        points = X_pca[:][mask, :2]  # Only take first 2 components

        # Scatter individual points
        scatter = ax.scatter(points[:, 0],
                             points[:, 1],
                             alpha=0.3,
                             s=10,
                             color=colors[i])

        # Add mean point
        if len(points) > 0:
            mean_point = points.mean(axis=0)
            ax.scatter(mean_point[0],
                       mean_point[1],
                       marker='o',
                       s=150,
                       color=colors[i],
                       edgecolors='black',
                       linewidths=2,
                       zorder=5)

            # Add covariance ellipse (if enough points)
            if len(points) > 2:
                cov = np.cov(points.T)
                plot_covariance_ellipse(ax,
                                        mean_point,
                                        cov,
                                        n_std=1.0,
                                        facecolor=colors[i],
                                        alpha=0.15,
                                        edgecolor=colors[i],
                                        linewidth=2)

        handles.append((scatter, str(gene)))

    baseline_labels = np.array(list(baseline_features.keys()) + ['Random 0.5'])
    baseline_X = np.array([
        list(inner_dict.values()) for inner_dict in baseline_features.values()
    ] + [[0.5] * len(X[0])])
    baseline_pca = pca.transform(baseline_X)

    for i, name in enumerate(baseline_labels):
        ax.scatter(baseline_pca[i, 0],
                   baseline_pca[i, 1],
                   marker='X',
                   s=200,
                   edgecolors='black',
                   linewidths=1.5)
        ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]))

    extrema_info = find_extrema(X_pca, metadata)

    # Annotate extreme points
    for position, info in extrema_info.items():
        ax.annotate(f"{info['strategy']}\n({info['gene']})",
                    xy=info['coords'],
                    xytext=(10, 10),
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5',
                              facecolor='yellow',
                              alpha=0.7),
                    arrowprops=dict(arrowstyle='->',
                                    connectionstyle='arc3,rad=0',
                                    lw=1.5),
                    fontsize=8,
                    zorder=10)

    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')
    ax.legend([h[0] for h in handles], [h[1] for h in handles])
    plt.tight_layout()
    plt.savefig(f"pca_{args.game}.png")

    def analysis(tl):
        print(f"\n{'='*60}")
        print(f"DETAILED ANALYSIS: TOP LEFT POINT")
        print(f"{'='*60}")
        features = tl['features']
        print(f"Behavior by context (showing first 10 contexts):")
        for i, (context, coop_prob) in enumerate(list(features.items())[:20]):
            # Context is tuple of tuples, flatten and convert to string
            if len(context) == 0:
                context_str = 'Start'
            else:
                # Each element in context is a tuple representing one round's opponent actions
                context_str = '|'.join(''.join('C' if val else 'D'
                                               for val in round_actions)
                                       for round_actions in context)
            print(f"  {context_str}: {coop_prob:.1%} coop)")

    analysis(extrema_info['top_left'])
    analysis(extrema_info['bottom_right'])
