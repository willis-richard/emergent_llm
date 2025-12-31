import argparse
from collections import defaultdict
from itertools import combinations_with_replacement, product
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA

from emergent_llm.common import Action, C, D, Gene
from emergent_llm.games import STANDARD_GENERATORS, get_game_types
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import (
    Altenator,
    AntiGrim,
    ConditionalCooperator,
    Cooperator,
    Defector,
    Flipper,
    Grim,
    LLMPlayer,
    SimplePlayer,
    LastRounds,
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run PCA for strategies")

    parser.add_argument("--game", type=str, required=True,
                       choices=["public_goods", "collective_risk", "common_pool"],
                       help="Game type")
    parser.add_argument("--strategies_dir", type=str, default="strategies",
                       help="Base directory containing strategy files")
    parser.add_argument("--models", nargs='*', default=None,
                       help="List of models to use, filter out all others")

    # Game parameters
    parser.add_argument("--n_players", type=int, default=4,
                       help="Number of players per game")
    parser.add_argument("--n_rounds", type=int, default=5,
                       help="Number of rounds per game")
    parser.add_argument("--n_games", type=int, default=20,
                       help="Number of games for each trajectory")

    # Parallel execution parameters
    parser.add_argument("--n_processes", type=int, default=1,
                        help="Number of parallel processes")

    return parser.parse_args()

args = parse_args()

game_class, _ = get_game_types(args.game)
description = STANDARD_GENERATORS[args.game + "_default"](n_players=args.n_players, n_rounds=args.n_rounds)

# Load strategies
registry = StrategyRegistry(
    strategies_dir=args.strategies_dir,
    game_name=args.game,
    models=args.models
)

genes = registry.available_genes

all_actions = tuple(combination for combination in product([D, C], repeat=args.n_rounds - 1))
print(len(all_actions))

unique_combos = tuple(combinations_with_replacement(all_actions, args.n_players - 1))
print(len(unique_combos))


class FixedOpponent:
    fixed_actions = None

    def __call__(self, state, history):
        return self.fixed_actions[state.round_number]

def hashable(arr):
    return tuple(map(tuple, arr))


def compute_features(player):
    opponents = [SimplePlayer(f"opponent_{i+1}", FixedOpponent()) for i in range(args.n_players - 1)]

    features = defaultdict(list)
    for combo in unique_combos:
        for opponent, actions in zip(opponents, combo):
            # last round action of opponents does not matter
            opponent.strategy_function.fixed_actions = list(actions) + [C]
        players = [player] + opponents

        results = [game_class(players, description).play_game() for _ in range(args.n_games)]
        player_history = results[0].history.for_player(0)
        for r in range(0, args.n_rounds):
            context = Action.from_bool_array(player_history.opponent_actions[:r])
            actions = [Action(result.history.actions[r,0]) for result in results]
            features[hashable(context)] += actions
    return features

def compute_gene(gene: Gene):
    player_features = []
    player_means = []
    for strategy_spec in registry.get_all_specs(gene):
        algo = strategy_spec.strategy_class
        player = LLMPlayer("testing", gene, description, algo)

        features = compute_features(player)
        player_features.append((algo.__name__, features))

        mean_features = [sum(v) / len(v) for v in features.values()]
        player_means.append(mean_features)

        all_values = [x for v in features.values() for x in Action.to_bool_array(v)]
        mean = sum(all_values) / len(all_values)
        print(f"{gene.model} {algo.__name__}: {mean}")
    return gene, player_features, player_means

def compute_baselines(baseline_players):
    baseline_features = {}
    for player in baseline_players:
        features = compute_features(player)
        for key, value in features.items():
            if not value or len(set(value)) != 1:
                raise ValueError(f"Key '{key}' has invalid list (empty or non-uniform values)")
            features[key] = value[0]
        baseline_features[player.id.name] = features

        mean_features = [v.value for v in features.values()]
        mean = sum(mean_features) / len(mean_features)
        print(f"{player.id.name}: {mean}")
    return baseline_features


baseline_players = [
    SimplePlayer("All-D", Defector),
    SimplePlayer("All-C", Cooperator),
    SimplePlayer("LR-All-C", LastRounds(D, [args.n_rounds-1], Cooperator)),
]
baseline_players += [SimplePlayer(f"C-Conditional-{i}", ConditionalCooperator(C, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"D-Conditional-{i}", ConditionalCooperator(D, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"C-AntiTFT-{i}", AntiTFT(C, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"D-AntiTFT-{i}", AntiTFT(D, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"C-MeanActor-{i}", MeanActor(C, i)) for i in [0.25, 0.5, 0.75]]
baseline_players += [SimplePlayer(f"Grim-{i}", Grim(C, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"AntiGrim-{i}", AntiGrim(D, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"D-FirstImpressions-{i}", FirstImpressions(D, i)) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"1C-Flip-CC-{i}", Flipper(C, 1, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"1D-Flip-CC-{i}", Flipper(D, 1, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"2C-Flip-CC-{i}", Flipper(C, 2, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
# baseline_players += [SimplePlayer(f"2D-Flip-CC-{i}", Flipper(D, 2, ConditionalCooperator(C, i))) for i in range(1, args.n_players)]
baseline_players += [SimplePlayer(f"{a}-Alternator", Altenator(a)) for a in [C,D]]
baseline_players += [SimplePlayer(f"LR-CC-{i}", LastRounds(D, [args.n_rounds-1], ConditionalCooperator(C, i))) for i in range(1, args.n_players)]

baseline_features = compute_baselines(baseline_players)

gene_features = {}
gene_means = {}

with Pool(processes=args.n_processes) as pool:
    results = pool.map(compute_gene, genes)
    for gene, player_features, player_means in results:
        gene_features[gene] = player_features
        gene_means[gene] = player_means

# print(gene_features)
# print(gene_means)

# PCA
X_list = []
labels = []

for gene, mean_features in gene_means.items():
    X_list.extend(mean_features)
    labels.extend([str(gene)] * len(mean_features))

X = np.array(X_list)
labels = np.array(labels)

pca = PCA(n_components=10)
X_pca = pca.fit_transform(X)
print(pca.explained_variance_ratio_[:5])

n_generated = len(labels)

def plot_covariance_ellipse(ax, mean, cov, n_std=1.0, **kwargs):
    """Plot covariance ellipse at n_std standard deviations."""
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(eigenvalues)
    ellipse = Ellipse(mean, width, height, angle=angle, **kwargs)
    ax.add_patch(ellipse)
    return ellipse


fig, ax = plt.subplots(figsize=(10, 8))

# Plot generated algorithms by behaviour
handles = []
colors = plt.colormaps.get_cmap('tab10')(np.linspace(0, 1, len(genes)))

for i, gene in enumerate(genes):
    mask = labels == str(gene)
    points = X_pca[:n_generated][mask, :2]  # Only take first 2 components

    # Scatter individual points
    scatter = ax.scatter(
        points[:, 0],
        points[:, 1],
        alpha=0.3,
        s=10,
        color=colors[i]
    )

    # Add mean point
    if len(points) > 0:
        mean_point = points.mean(axis=0)
        ax.scatter(
            mean_point[0],
            mean_point[1],
            marker='o',
            s=150,
            color=colors[i],
            edgecolors='black',
            linewidths=2,
            zorder=5
        )

        # Add covariance ellipse (if enough points)
        if len(points) > 2:
            cov = np.cov(points.T)
            plot_covariance_ellipse(
                ax, mean_point, cov,
                n_std=1.0,
                facecolor=colors[i],
                alpha=0.15,
                edgecolor=colors[i],
                linewidth=2
            )

    handles.append((scatter, str(gene)))

baseline_labels = np.array(list(baseline_features.keys()) + ['Random 0.5'])
baseline_X = np.array([[v.value for v in inner_dict.values()] for inner_dict in baseline_features.values()] + [[0.5] * len(X[0])])
baseline_pca = pca.transform(baseline_X)

for i, name in enumerate(baseline_labels):
    ax.scatter(
        baseline_pca[i, 0],
        baseline_pca[i, 1],
        marker='X',
        s=200,
        edgecolors='black',
        linewidths=1.5
    )
    ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]))

# Find and print extreme points
def find_extrema(X_pca, labels, gene_features):
    """Find strategies at plot extrema."""
    extrema = {
        'top_left': np.argmin(X_pca[:, 0] - X_pca[:, 1]),  # min PC1, max PC2
        'top_right': np.argmax(X_pca[:, 0] + X_pca[:, 1]),  # max both
        'bottom_left': np.argmin(X_pca[:, 0] + X_pca[:, 1]),  # min both
        'bottom_right': np.argmax(X_pca[:, 0] - X_pca[:, 1]),  # max PC1, min PC2
    }

    results = {}
    for position, idx in extrema.items():
        gene_str = labels[idx]

        # Find which strategy this is by counting through genes in order
        gene = next(g for g in genes if str(g) == gene_str)

        # Count how many strategies come before this index
        count = 0
        local_idx = None
        for g in genes:
            n_strategies = len(gene_features[g])
            if count + n_strategies > idx:
                local_idx = idx - count
                break
            count += n_strategies

        if local_idx is None or local_idx >= len(gene_features[gene]):
            print(f"Error: couldn't find strategy for index {idx}")
            continue

        strategy_name = gene_features[gene][local_idx][0]
        features_dict = gene_features[gene][local_idx][1]

        results[position] = {
            'idx': idx,
            'gene': gene_str,
            'strategy': strategy_name,
            'coords': (X_pca[idx, 0], X_pca[idx, 1]),
            'features': features_dict
        }

        print(f"\n{position.upper().replace('_', ' ')}:")
        print(f"  Gene: {gene_str}")
        print(f"  Strategy: {strategy_name}")
        print(f"  PC1: {X_pca[idx, 0]:.3f}, PC2: {X_pca[idx, 1]:.3f}")

        # Print some feature statistics
        all_values = [x for v in features_dict.values() for x in Action.to_bool_array(v)]
        coop_rate = sum(all_values) / len(all_values)
        print(f"  Overall cooperation rate: {coop_rate:.2%}")

    return results

extrema_info = find_extrema(X_pca[:n_generated], labels, gene_features)

# Annotate extreme points
for position, info in extrema_info.items():
    ax.annotate(
        f"{info['strategy']}\n({info['gene']})",
        xy=info['coords'],
        xytext=(10, 10),
        textcoords='offset points',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1.5),
        fontsize=8,
        zorder=10
    )

ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')
ax.legend([h[0] for h in handles], [h[1] for h in handles])
plt.tight_layout()
plt.savefig("pca2.png")

# Detailed analysis of top-left point
tl = extrema_info['top_left']
print(f"\n{'='*60}")
print(f"DETAILED ANALYSIS: TOP LEFT POINT")
print(f"{'='*60}")
features = tl['features']
print(f"Behavior by context (showing first 10 contexts):")
for i, (context, actions) in enumerate(list(features.items())[:10]):
    # Context is tuple of tuples, flatten and convert to string
    if len(context) == 0:
        context_str = 'Start'
    else:
        # Each element in context is a tuple representing one round's opponent actions
        context_str = '|'.join(''.join('C' if val else 'D' for val in round_actions)
                               for round_actions in context)
    action_counts = {C: actions.count(C), D: actions.count(D)}
    coop_prob = action_counts[C] / (action_counts[C] + action_counts[D])
    print(f"  {context_str}: C={action_counts[C]}, D={action_counts[D]} ({coop_prob:.1%} coop)")
    if i >= 9:
        break
