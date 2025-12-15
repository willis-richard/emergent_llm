import argparse
from collections import defaultdict
from itertools import combinations_with_replacement, product

from emergent_llm.common import Action, C, D, Gene
from emergent_llm.games import STANDARD_GENERATORS, get_game_class
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import LLMPlayer, SimplePlayer

import numpy as np
from sklearn.decomposition import PCA
from multiprocessing import Pool
import matplotlib.pyplot as plt


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

game_class = get_game_class(args.game)
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

    def __call__(self, round_number: int):
        return self.fixed_actions[round_number]

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
        # player = SimplePlayer("player", RandomCooperator)

        features = compute_features(player)
        player_features.append((algo.__name__, features))

        mean_features = [sum(v) / len(v) for v in features.values()]
        player_means.append(mean_features)

        all_values = [x for v in features.values() for x in Action.to_bool_array(v)]
        mean = sum(all_values) / len(all_values)
        print(f"{gene.model} {algo.__name__}: {mean}")
    return gene, player_features, player_means


gene_features = {}
gene_means = {}

with Pool(processes=args.n_processes) as pool:
    results = pool.map(compute_gene, genes)
    for gene, player_features, player_means in results:
        gene_features[gene] = player_features
        gene_means[gene] = player_means

# print(gene_features)
print(gene_means)

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

fig, ax = plt.subplots(figsize=(10, 8))

# Plot generated algorithms by behaviour
handles = []
for gene in genes:
    mask = labels == str(gene)
    scatter = ax.scatter(
        X_pca[:n_generated][mask, 0],
        X_pca[:n_generated][mask, 1],
        alpha=0.3,
        s=10
    )
    handles.append((scatter, str(gene)))

baselines = {
    'All-D': [0] * len(X[0]),
    'All-C': [1] * len(X[0]),
    }
baseline_X = np.array(list(baselines.values()))
baseline_labels = np.array(list(baselines.keys()))
baseline_pca = pca.transform(baseline_X)
X_full = np.vstack([X, baseline_X])

# Plot baselines as larger labeled points
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

ax.legend([h[0] for h in handles], [h[1] for h in handles])
ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')
ax.legend()
plt.tight_layout()
plt.savefig("pca.png")
