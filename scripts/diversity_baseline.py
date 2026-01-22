"""
Behaviour diversity with baseline opponent pools.

Compared to scripts/diversity.py (fixed action sequences), this script:
* Builds a pool of hand-crafted baseline strategies (from sample_players.py).
* Enumerates all opponent combinations (with replacement, orderless) for n_players-1 slots.
* For each LLM strategy, plays repeated games against every opponent combo.
* Feature vector: cooperation probability per (opponent combo, round).
* Runs a shared PCA and reports diversity metrics; baselines are projected as anchors.
"""

import argparse
import pickle
import random
from dataclasses import dataclass
from itertools import combinations_with_replacement
from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA

from emergent_llm.common import (
    Action,
    Attitude,
    C,
    D,
    GameHistory,
    GameState,
    Gene,
    setup,
)
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import (
    SimplePlayer,
    LLMPlayer,
    ConditionalCooperator,
    HistoricalCooperator,
    GradualDefector,
    PeriodicDefector,
    Grim,
    SpecialRounds,
    Random,
    RandomCooperator,
    RandomDefector,
    Cooperator,
    Defector,
    Altenator,
)

FIGSIZE, FORMAT = setup('fullscreen')


# =============================================================================
# ARGUMENTS
# =============================================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Behaviour diversity via baseline opponent pools (PCA)")
    parser.add_argument(
        "--games",
        type=str,
        nargs="+",
        default=["public_goods", "collective_risk", "common_pool"],
        choices=["public_goods", "collective_risk", "common_pool"],
        help="Game type(s) to analyse")
    parser.add_argument("--strategies_dir",
                        type=str,
                        default="strategies",
                        help="Base directory containing strategy files")
    parser.add_argument("--models",
                        nargs="*",
                        default=None,
                        help="Only include these models")
    parser.add_argument("--exclude_models",
                        nargs="*",
                        default=None,
                        help="Exclude these models")
    parser.add_argument("--n_strategies",
                        type=int,
                        default=256,
                        help="Limit strategies per gene")

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
                        help="Repeated games per opponent combo")
    parser.add_argument("--seed",
                        type=int,
                        default=42,
                        help="Random seed for reproducibility")

    # Execution
    parser.add_argument("--n_processes",
                        type=int,
                        default=1,
                        help="Number of parallel processes")
    parser.add_argument("--recompute",
                        action="store_true",
                        help="Force recomputation even if cached")
    parser.add_argument("--plot_extrema",
                        action="store_true",
                        help="Annotate PCA extrema")

    return parser.parse_args()


# =============================================================================
# BASELINE POOL
# =============================================================================


@dataclass(frozen=True)
class BaselineSpec:
    name: str
    factory: callable


def build_baseline_pool(n_rounds: int) -> list[BaselineSpec]:
    """
    Baseline opponents drawn from sample_players.py.
    Factories return callables: f(GameState, PlayerHistory|None) -> Action
    """
    return [
        BaselineSpec("All-C", lambda: Cooperator),
        BaselineSpec("All-D", lambda: Defector),
        BaselineSpec("Random-50", lambda: Random),
        BaselineSpec("RandomCoop-90", lambda: RandomCooperator),
        BaselineSpec("RandomDefect-90", lambda: RandomDefector),
        BaselineSpec("Alternator-C", lambda: Altenator(C)),
        BaselineSpec("Periodic-D-2", lambda: PeriodicDefector(2)),
        BaselineSpec("Gradual-3", lambda: GradualDefector(3)),
        BaselineSpec("Conditional-1", lambda: ConditionalCooperator(C, 1)),
        BaselineSpec("Historical-1", lambda: HistoricalCooperator(C, 1)),
        BaselineSpec("Grim-1", lambda: Grim(C, 1)),
        BaselineSpec("LR-All-C",
                     lambda: SpecialRounds(Cooperator, Defector,
                                           [n_rounds - 1])),
    ]


def create_baseline_players(n_players: int,
                            n_rounds: int) -> list[SimplePlayer]:
    _ = n_players
    baseline_players = [
        SimplePlayer("All-D", Defector),
        SimplePlayer("All-C", Cooperator),
        SimplePlayer("All-C,LR-D",
                     SpecialRounds(Cooperator, Defector, [n_rounds - 1])),
        SimplePlayer("All-D,LR-C",
                     SpecialRounds(Defector, Cooperator, [n_rounds - 1])),
    ]
    baseline_players += [
        SimplePlayer(f"CC-{i}", ConditionalCooperator(C, i)) for i in [2]
    ]
    baseline_players += [
        SimplePlayer(
            f"CC-{i},LR-D",
            SpecialRounds(ConditionalCooperator(C, i), Defector,
                          [n_rounds - 1])) for i in [2]
    ]
    return baseline_players


# =============================================================================
# CACHING
# =============================================================================


def get_cache_path(game_name: str, gene: Gene, args) -> Path:
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    filename = f"baseline_{game_name}_{gene}_p{args.n_players}_r{args.n_rounds}_g{args.n_games}"
    if args.n_strategies:
        filename += f"_s{args.n_strategies}"
    return cache_dir / f"{filename}.pkl"


def save_features(features_dict, game_name: str, gene: Gene, args):
    cache_path = get_cache_path(game_name, gene, args)
    with open(cache_path, "wb") as f:
        pickle.dump(features_dict, f)
    print(f"Saved features to {cache_path}")


def load_features(game_name: str, gene: Gene,
                  args) -> dict[str, dict[tuple, float]] | None:
    cache_path = get_cache_path(game_name, gene, args)
    if not cache_path.exists():
        return None
    with open(cache_path, "rb") as f:
        features_dict = pickle.load(f)
    print(f"Loaded features from {cache_path}")
    return features_dict


# =============================================================================
# FEATURE COMPUTATION
# =============================================================================


def set_global_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def play_games(player: SimplePlayer | LLMPlayer, opponents: list[SimplePlayer],
               n_games: int) -> list[GameHistory]:
    players = [player] + opponents
    histories = [
        game_class(players, description).play_game().history
        for _ in range(n_games)
    ]
    return histories


def combo_key(combo: tuple[BaselineSpec, ...]) -> tuple[str, ...]:
    return tuple(spec.name for spec in combo)


def compute_features_for_player(
    player: SimplePlayer | LLMPlayer,
    combos: tuple[tuple[BaselineSpec, ...], ...],
    n_games: int,
) -> dict[tuple, float]:
    """
    Returns dict keyed by ((opp1,...,oppK), round) -> cooperation rate.
    """
    features: dict[tuple, float] = {}
    for combo in combos:
        opponents = [
            SimplePlayer(f"opponent_{i+1}", spec.factory())
            for i, spec in enumerate(combo)
        ]
        try:
            histories = play_games(player, opponents, n_games)
        except Exception as exc:  # defensive
            print(f"  !! Failed on combo {combo_key(combo)}: {exc}")
            continue

        key = combo_key(combo)
        for r in range(args.n_rounds):
            actions = [Action(history.actions[r, 0]) for history in histories]
            features[(key, r)] = float(Action.to_bool_array(actions).mean())
    return features


def compute_gene(gene: Gene) -> dict[str, dict[tuple, float]]:
    if not args.recompute:
        cached = load_features(game_name, gene, args)
        if cached is not None:
            return cached

    strategy_features = {}
    specs = registry.get_all_specs(gene)[:args.n_strategies]
    for strategy_spec in specs:
        try:
            player = LLMPlayer("tested", gene, description,
                               strategy_spec.strategy_class)
            features = compute_features_for_player(player, unique_combos,
                                                   args.n_games)
        except Exception as exc:
            print(f"!! Skipping {strategy_spec.strategy_class.__name__}: {exc}")
            continue

        strategy_features[strategy_spec.strategy_class.__name__] = features
        print(
            f"{gene.model} {strategy_spec.strategy_class.__name__}: {np.mean(list(features.values())):.3f}"
        )

    save_features(strategy_features, game_name, gene, args)
    return strategy_features


def compute_baselines(
        baseline_players: list[SimplePlayer],
        combos: tuple[tuple[BaselineSpec, ...], ...]) -> dict[str, dict[tuple,
                                                                        float]]:
    baseline_features = {}
    for player in baseline_players:
        features = compute_features_for_player(player, combos, args.n_games)
        baseline_features[player.id.name] = features
        mean = np.mean(list(features.values()))
        print(f"{player.id.name}: {mean:.3f}")
    return baseline_features


# =============================================================================
# METRICS
# =============================================================================


@dataclass
class DiversityMetrics:
    gene: Gene
    n_strategies: int
    mean_pairwise_distance: float
    mean_pairwise_distance_normalised: float
    participation_ratio: float

    def __str__(self):
        return (f"{self.gene}: n={self.n_strategies}, "
                f"MPD={self.mean_pairwise_distance:.3f} "
                f"(norm={self.mean_pairwise_distance_normalised:.2f}), "
                f"PR={self.participation_ratio:.2f}")


@dataclass
class BetweenSetMetrics:
    game: str
    model: str
    centroid_distance: float
    cohens_d: float

    def __str__(self):
        return (f"{self.game}/{self.model}: "
                f"centroid_dist={self.centroid_distance:.3f}, "
                f"Cohen's d={self.cohens_d:.2f}")


def compute_random_baseline_distance(n_features: int,
                                     n_samples: int = 500) -> float:
    random_X = np.random.uniform(0, 1, (n_samples, n_features))
    distances = pdist(random_X, metric="euclidean")
    return float(np.mean(distances))


def compute_within_set_metrics(X: np.ndarray,
                               random_baseline: float) -> tuple[float, float]:
    if len(X) < 2:
        return 0.0, 0.0
    distances = pdist(X, metric="euclidean")
    mpd = float(np.mean(distances))
    return mpd, mpd / random_baseline


def compute_participation_ratio(X: np.ndarray) -> float:
    if len(X) < 2:
        return 1.0
    X_centered = X - X.mean(axis=0)
    cov = np.cov(X_centered.T)
    eigenvalues = np.linalg.eigvalsh(cov)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    if len(eigenvalues) == 0:
        return 1.0
    return (eigenvalues.sum()**2) / (eigenvalues**2).sum()


def compute_between_set_metrics(X_collective: np.ndarray,
                                X_exploitative: np.ndarray) -> tuple[float,
                                                                     float]:
    if len(X_collective) == 0 or len(X_exploitative) == 0:
        return np.nan, np.nan

    centroid_c = X_collective.mean(axis=0)
    centroid_e = X_exploitative.mean(axis=0)
    centroid_distance = np.linalg.norm(centroid_c - centroid_e)

    var_c = np.var(X_collective, axis=0).mean() if len(X_collective) > 1 else 0
    var_e = np.var(X_exploitative,
                   axis=0).mean() if len(X_exploitative) > 1 else 0

    n_c, n_e = len(X_collective), len(X_exploitative)
    pooled_var = ((n_c - 1) * var_c +
                  (n_e - 1) * var_e) / (n_c + n_e - 2) if (n_c + n_e) > 2 else 1
    pooled_std = np.sqrt(pooled_var * X_collective.shape[1])

    cohens_d = centroid_distance / pooled_std if pooled_std > 0 else np.nan
    return centroid_distance, cohens_d


# =============================================================================
# PLOTTING
# =============================================================================


def plot_covariance_ellipse(ax, mean, cov, n_std=1.0, **kwargs):
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(np.maximum(eigenvalues, 0))
    ellipse = Ellipse(mean, width, height, angle=angle, **kwargs)
    ax.add_patch(ellipse)
    return ellipse


def plot_pca_by_gene(ax, X_pca, genes, labels, baseline_pca, baseline_labels,
                     title, pca):
    colors = plt.colormaps.get_cmap("tab10")(np.linspace(0, 1, len(genes)))
    handles = []

    for i, gene in enumerate(genes):
        mask = labels == str(gene)
        points = X_pca[mask, :2]
        scatter = ax.scatter(points[:, 0],
                             points[:, 1],
                             alpha=0.3,
                             s=10,
                             color=colors[i])
        if len(points) > 0:
            mean_pt = points.mean(axis=0)
            ax.scatter(mean_pt[0],
                       mean_pt[1],
                       marker="o",
                       s=100,
                       color=colors[i],
                       edgecolors="black",
                       linewidths=1.5,
                       zorder=5)
            if len(points) > 2:
                cov = np.cov(points.T)
                plot_covariance_ellipse(ax,
                                        mean_pt,
                                        cov,
                                        n_std=1.0,
                                        facecolor=colors[i],
                                        alpha=0.15,
                                        edgecolor=colors[i],
                                        linewidth=1.5)
        handles.append((scatter, str(gene)))

    for i, name in enumerate(baseline_labels):
        ax.scatter(baseline_pca[i, 0],
                   baseline_pca[i, 1],
                   marker="X",
                   s=120,
                   edgecolors="black",
                   linewidths=1,
                   zorder=6)
        ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]), fontsize=6)

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_title(title)
    ax.legend([h[0] for h in handles], [h[1] for h in handles], fontsize=6)


def plot_pca_by_model(ax, X_pca, model_labels, models, baseline_pca,
                      baseline_labels, title, pca):
    colors = plt.colormaps.get_cmap("tab20")(np.linspace(0, 1, len(models)))
    handles = []

    for i, model in enumerate(models):
        mask = model_labels == model
        points = X_pca[mask, :2]
        scatter = ax.scatter(points[:, 0],
                             points[:, 1],
                             alpha=0.3,
                             s=10,
                             color=colors[i])
        if len(points) > 0:
            mean_pt = points.mean(axis=0)
            ax.scatter(mean_pt[0],
                       mean_pt[1],
                       marker="o",
                       s=100,
                       color=colors[i],
                       edgecolors="black",
                       linewidths=1.5,
                       zorder=5)
            if len(points) > 2:
                cov = np.cov(points.T)
                plot_covariance_ellipse(ax,
                                        mean_pt,
                                        cov,
                                        n_std=1.0,
                                        facecolor=colors[i],
                                        alpha=0.15,
                                        edgecolor=colors[i],
                                        linewidth=1.5)
        handles.append((scatter, model))

    for i, name in enumerate(baseline_labels):
        ax.scatter(baseline_pca[i, 0],
                   baseline_pca[i, 1],
                   marker="X",
                   s=120,
                   edgecolors="black",
                   linewidths=1,
                   zorder=6)
        ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]), fontsize=6)

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_title(title)
    ax.legend([h[0] for h in handles], [h[1] for h in handles], fontsize=6)


# =============================================================================
# MAIN
# =============================================================================


if __name__ == "__main__":
    args = parse_args()
    set_global_seed(args.seed)
    pca_dir = Path("pca")
    pca_dir.mkdir(exist_ok=True)

    # Baseline pool and opponent combinations (orderless)
    baseline_specs = build_baseline_pool(args.n_rounds)
    unique_combos: tuple[tuple[BaselineSpec, ...], ...] = tuple(
        combinations_with_replacement(baseline_specs, args.n_players - 1))
    combo_keys = [combo_key(c) for c in unique_combos]

    print(
        f"Using {len(baseline_specs)} baseline opponents -> {len(unique_combos)} combos for {args.n_players-1} slots."
    )
    print(f"Feature dimension = combos * rounds = {len(unique_combos)} x "
          f"{args.n_rounds} = {len(unique_combos)*args.n_rounds}")
    print("Combos (opponent pools):")
    for idx, ck in enumerate(combo_keys):
        print(f"  {idx+1:02d}: {ck}")

    pca_data = {}

    # ======================================================================
    # PHASE 1: Load/compute features per game
    # ======================================================================
    for game_name in args.games:
        game_class, _ = get_game_type(game_name)
        description = STANDARD_GENERATORS[game_name + "_default"](
            n_players=args.n_players, n_rounds=args.n_rounds)
        registry = StrategyRegistry(strategies_dir=args.strategies_dir,
                                    game_name=game_name,
                                    models=args.models)
        genes = sorted(list(registry.available_genes), key=str)

        if args.exclude_models:
            genes = [
                g for g in genes if g.model not in set(args.exclude_models)
            ]

        if not genes:
            print(f"[warn] No genes found for {game_name}; skipping.")
            continue

        with Pool(processes=args.n_processes,
                  initializer=set_global_seed,
                  initargs=(args.seed, )) as pool:
            results = pool.map(compute_gene, genes)
            results_dict = dict(zip(genes, results))

        print(
            f"Loaded {len(results_dict.values())} genes, with {sum(len(v) for v in results_dict.values())} strategies for {game_name}"
        )

        X_game = []
        labels_gene = []
        labels_model = []
        labels_attitude = []
        metadata_game = []

        for gene, strategy_features in results_dict.items():
            for strategy_name, feature_dict in strategy_features.items():
                vector = []
                for ck in combo_keys:
                    for r in range(args.n_rounds):
                        vector.append(feature_dict.get((ck, r), 0.0))
                X_game.append(vector)
                labels_gene.append(str(gene))
                labels_model.append(gene.model)
                labels_attitude.append(str(gene.attitude))
                metadata_game.append((gene, strategy_name, feature_dict))

        pca_data[game_name] = {
            "X": np.array(X_game),
            "labels_gene": np.array(labels_gene),
            "labels_model": np.array(labels_model),
            "labels_attitude": np.array(labels_attitude),
            "metadata": metadata_game,
            "genes": genes,
        }

    # ======================================================================
    # PHASE 2: Baseline anchors
    # ======================================================================
    print(f"\n{'='*60}")
    print("COMPUTING BASELINE ANCHORS")
    print(f"{'='*60}")
    baseline_players = create_baseline_players(args.n_players, args.n_rounds)
    baseline_features = compute_baselines(baseline_players, unique_combos)
    baseline_labels = list(baseline_features.keys()) + ["Random 0.5"]
    baseline_X = []
    for feature_dict in baseline_features.values():
        vector = []
        for ck in combo_keys:
            for r in range(args.n_rounds):
                vector.append(feature_dict.get((ck, r), 0.0))
        baseline_X.append(vector)
    n_features = len(baseline_X[0])
    baseline_X = np.array(baseline_X + [[0.5] * n_features])

    # ======================================================================
    # PHASE 3: Combined PCA
    # ======================================================================
    print(f"\n{'='*60}")
    print("COMBINED PCA ANALYSIS")
    print(f"{'='*60}")

    X_all = np.vstack([pca_data[g]["X"] for g in args.games if g in pca_data])
    labels_all_gene = np.concatenate(
        [pca_data[g]["labels_gene"] for g in args.games if g in pca_data])
    labels_all_model = np.concatenate(
        [pca_data[g]["labels_model"] for g in args.games if g in pca_data])
    labels_all_attitude = np.concatenate(
        [pca_data[g]["labels_attitude"] for g in args.games if g in pca_data])
    game_labels = np.concatenate([[g] * len(pca_data[g]["X"])
                                  for g in args.games if g in pca_data])

    if len(X_all) == 0:
        raise SystemExit("No strategies loaded; aborting.")

    n_components = min(10, X_all.shape[1], X_all.shape[0])
    pca_combined = PCA(n_components=n_components)
    X_pca_combined = pca_combined.fit_transform(X_all)
    baseline_pca_combined = pca_combined.transform(baseline_X)

    # Scree plot
    cumulative = np.cumsum(pca_combined.explained_variance_ratio_)
    plt.figure()
    plt.plot(range(1, len(cumulative) + 1), cumulative, "o-")
    plt.axhline(y=0.9, color="r", linestyle="--", label="90% threshold")
    plt.xlabel("Component")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("Combined PCA Scree Plot")
    plt.legend()
    plt.savefig(pca_dir / f"scree_combined_baseline.{FORMAT}",
                format=FORMAT,
                bbox_inches="tight")
    plt.close()

    # Per-game plots (by gene)
    for game_name in args.games:
        if game_name not in pca_data:
            continue
        mask = game_labels == game_name
        X_game_pca = X_pca_combined[mask]
        labels_game = labels_all_gene[mask]
        genes = pca_data[game_name]["genes"]
        metadata = pca_data[game_name]["metadata"]

        fig, ax = plt.subplots(figsize=FIGSIZE)
        plot_pca_by_gene(ax, X_game_pca, genes, labels_game,
                         baseline_pca_combined, baseline_labels, game_name,
                         pca_combined)

        if args.plot_extrema:
            extrema_indices = {
                'top_left': np.argmin(X_game_pca[:, 0] - X_game_pca[:, 1]),
                'top_right': np.argmax(X_game_pca[:, 0] + X_game_pca[:, 1]),
                'bottom_left': np.argmin(X_game_pca[:, 0] + X_game_pca[:, 1]),
                'bottom_right': np.argmax(X_game_pca[:, 0] - X_game_pca[:, 1]),
            }
            for pos, idx in extrema_indices.items():
                gene, strategy_name, feature_dict = metadata[idx]
                print(
                    f"[{game_name}] {pos}: {gene} / {strategy_name} -> PC ({X_game_pca[idx,0]:.3f}, {X_game_pca[idx,1]:.3f}) "
                    f"coop={np.mean(list(feature_dict.values())):.2%}")

        plt.tight_layout()
        plt.savefig(pca_dir / f"pca_{game_name}_baseline.{FORMAT}",
                    format=FORMAT,
                    bbox_inches="tight")
        plt.close()

    # Per-game plots (by model, attitudes merged)
    for game_name in args.games:
        if game_name not in pca_data:
            continue
        mask = game_labels == game_name
        X_game_pca = X_pca_combined[mask]
        labels_model_game = labels_all_model[mask]
        models_game = sorted(list(set(labels_model_game)))

        fig, ax = plt.subplots(figsize=FIGSIZE)
        plot_pca_by_model(ax, X_game_pca, labels_model_game, models_game,
                          baseline_pca_combined, baseline_labels,
                          f"{game_name} (by model)", pca_combined)
        plt.tight_layout()
        plt.savefig(pca_dir / f"pca_{game_name}_models_baseline.{FORMAT}",
                    format=FORMAT,
                    bbox_inches="tight")
        plt.close()

    # Per-game plots (by model, split by attitude)
    for game_name in args.games:
        if game_name not in pca_data:
            continue
        mask = game_labels == game_name
        for attitude in (Attitude.COLLECTIVE, Attitude.EXPLOITATIVE):
            attitude_mask = mask & (labels_all_attitude == str(attitude))
            if not attitude_mask.any():
                continue
            X_game_pca = X_pca_combined[attitude_mask]
            labels_model_game = labels_all_model[attitude_mask]
            models_game = sorted(list(set(labels_model_game)))

            fig, ax = plt.subplots(figsize=FIGSIZE)
            plot_pca_by_model(
                ax,
                X_game_pca,
                labels_model_game,
                models_game,
                baseline_pca_combined,
                baseline_labels,
                f"{game_name} ({attitude})",
                pca_combined,
            )
            plt.tight_layout()
            plt.savefig(
                pca_dir / f"pca_{game_name}_models_{attitude}_baseline.{FORMAT}",
                format=FORMAT,
                bbox_inches="tight",
            )
            plt.close()

    # ======================================================================
    # PHASE 4: Metrics
    # ======================================================================
    print(f"\n{'='*60}")
    print("DIVERSITY METRICS (Within-set)")
    print(f"{'='*60}")

    random_baseline_dist = compute_random_baseline_distance(X_all.shape[1])

    for game_name in args.games:
        if game_name not in pca_data:
            continue
        print(f"\n  {game_name}:")
        mask = game_labels == game_name
        for gene in pca_data[game_name]["genes"]:
            gene_mask = mask & (labels_all_gene == str(gene))
            X_gene = X_all[gene_mask]
            mpd, mpd_norm = compute_within_set_metrics(
                X_gene, random_baseline_dist)
            pr = compute_participation_ratio(X_gene)
            print(
                f"    {gene}: MPD={mpd:.3f} (norm={mpd_norm:.2f}), PR={pr:.2f}")

    print(f"\n{'='*60}")
    print("BETWEEN-SET METRICS (Collective vs Exploitative)")
    print(f"{'='*60}")

    for game_name in args.games:
        if game_name not in pca_data:
            continue
        print(f"\n  {game_name}:")
        genes = pca_data[game_name]["genes"]
        models_in_game = set(gene.model for gene in genes)

        for model in sorted(models_in_game):
            collective_genes = [
                g for g in genes
                if g.model == model and g.attitude == Attitude.COLLECTIVE
            ]
            exploitative_genes = [
                g for g in genes
                if g.model == model and g.attitude == Attitude.EXPLOITATIVE
            ]
            if not collective_genes or not exploitative_genes:
                continue

            mask = game_labels == game_name
            X_collective = X_all[mask & np.isin(
                labels_all_gene, [str(g) for g in collective_genes])]
            X_exploitative = X_all[mask & np.isin(
                labels_all_gene, [str(g) for g in exploitative_genes])]
            if len(X_collective) == 0 or len(X_exploitative) == 0:
                continue

            centroid_dist, cohens_d = compute_between_set_metrics(
                X_collective, X_exploitative)
            metrics = BetweenSetMetrics(game=game_name,
                                        model=model,
                                        centroid_distance=centroid_dist,
                                        cohens_d=cohens_d)
            print(f"    {metrics}")
