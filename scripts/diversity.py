# pylint: disable=redefined-outer-name,missing-function-docstring,missing-class-docstring,possibly-used-before-assignment

import argparse
import logging
import pickle
from collections import defaultdict
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from scipy.spatial.distance import cdist, pdist
from sklearn.decomposition import PCA

from emergent_llm.common import (
    Action,
    Attitude,
    C,
    D,
    GameHistory,
    Gene,
    setup,
)
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import (
    CooperatorCounts,
    FixedCooperatorCount,
    StrategyRegistry,
    make_fixed_opponents,
)
from emergent_llm.players import (
    BasePlayer,
    ConditionalCooperator,
    ConditionalDefector,
    Cooperator,
    Defector,
    LLMPlayer,
    SimplePlayer,
)

FIGSIZE, FORMAT = setup('fullscreen')

GAME_MAPPING = {
    'public_goods': ' Public Goods Game',
    'collective_risk': 'Collective Risk Dilemma',
    'common_pool': 'Common Pool Resource',
    'public_goods_prompt': 'Public Goods'
}

MODELS_MAPPING = {
    "gpt-5-mini": "GPT 5 Mini",
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "claude-haiku-4-5": "Claude Haiku 4.5",
    "llama3.1-70b": "Llama 3.1 70b",
    "mistral-7b": "Mistral 7b",
    "deepseek-r1-distill-llama-70b": "DeepSeek R1"
}

# =============================================================================
# ARGUMENT PARSING
# =============================================================================


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run PCA for strategies")

    parser.add_argument(
        "--games",
        type=str,
        nargs='+',
        default=["public_goods", "collective_risk", "common_pool"],
        choices=[
            "public_goods", "collective_risk", "common_pool",
            "public_goods_prompt"
        ],
        help="Game type(s) to analyse")
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
                        default=50,
                        help="Number of games for each trajectory")

    # Execution parameters
    parser.add_argument("--n_processes",
                        type=int,
                        default=1,
                        help="Number of parallel processes")
    parser.add_argument("--recompute",
                        action='store_true',
                        help="Force recomputation of features even if cached")
    parser.add_argument("--plot_extrema",
                        action='store_true',
                        help="Label the corner strategies")
    parser.add_argument("--results_dir", type=str, default="results")

    return parser.parse_args()


def setup_logging(log_file: Path, loglevel=logging.INFO):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file),
                  logging.StreamHandler()])


# =============================================================================
# CACHING
# =============================================================================


def get_output_dir(args) -> Path:
    return Path(args.results_dir) / "diversity"


def get_cache_path(game_name: str, gene: Gene, args) -> Path:
    cache_dir = get_output_dir(args) / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{game_name}_{gene}_p{args.n_players}_r{args.n_rounds}_g{args.n_games}"
    if args.n_strategies:
        filename += f"_s{args.n_strategies}"
    return cache_dir / f"{filename}.pkl"


def save_features(features_dict, game_name: str, gene: Gene, args):
    cache_path = get_cache_path(game_name, gene, args)
    with open(cache_path, 'wb') as f:
        pickle.dump(features_dict, f)
    logger.info(f"Saved features to {cache_path}")


def load_features(game_name: str, gene: Gene,
                  args) -> dict[str, dict[CooperatorCounts, float]] | None:
    cache_path = get_cache_path(game_name, gene, args)
    if not cache_path.exists():
        logger.info(f"Could not find existing cache at {cache_path}")
        return None
    with open(cache_path, 'rb') as f:
        features_dict = pickle.load(f)
    logger.info(
        f"Loaded features for {len(features_dict.keys())} strategies from {cache_path}"
    )
    return features_dict


# =============================================================================
# FEATURE COMPUTATION (uses globals set per-game in main)
# =============================================================================


def play_games(player: LLMPlayer, n_games: int,
               combo: CooperatorCounts) -> list[GameHistory]:
    n_opponents = args.n_players - 1
    # Append a dummy count for the final round (opponent actions don't
    # affect the feature we record for that round)
    counts_with_final = list(combo) + [0]
    # last round action of opponents does not matter
    opponents = [
        SimplePlayer(f"opponent_{i}", FixedCooperatorCount(i, counts_with_final))
        for i in range(n_opponents)
    ]

    players = [player] + opponents
    histories = [
        game_class(players, description).play_game().history
        for _ in range(n_games)
    ]
    return histories


def compute_features(player: BasePlayer, n_games: int) -> dict[CooperatorCounts, float]:
    features: dict[CooperatorCounts, float] = {}
    for combo, opponents in make_fixed_opponents(args.n_players - 1, args.n_rounds):
        players = [player] + opponents
        histories = [game_class(players, description).play_game().history
                     for _ in range(n_games)]
        for r in range(args.n_rounds):
            context: CooperatorCounts = combo[:r]
            actions = [Action(history.actions[r, 0]) for history in histories]
            features[context] = float(Action.to_bool_array(actions).mean())
    return features


def chunk_indices(n_items: int, n_chunks: int) -> list[list[int]]:
    """Split indices into approximately equal chunks."""
    chunk_size = (n_items + n_chunks - 1) // n_chunks
    return [
        list(range(i, min(i + chunk_size, n_items)))
        for i in range(0, n_items, chunk_size)
    ]


def compute_strategy_chunk(
    strategy_indices: list[int]
) -> list[tuple[str, dict[CooperatorCounts, float]]]:
    """Compute features for a chunk of strategies. Runs in worker process."""
    worker_registry = StrategyRegistry(args.strategies_dir, game_name,
                                       [gene.model])
    specs = worker_registry.get_all_specs(gene)

    results = []
    for idx in strategy_indices:
        spec = specs[idx]
        player = LLMPlayer("testing", gene, description, spec.strategy_class)
        features = compute_features(player, args.n_games)
        results.append((spec.strategy_class.__name__, features))
        logger.debug(
            f"{gene.model} {spec.strategy_class.__name__}: {np.mean(list(features.values())):.3f}"
        )

    return results


# =============================================================================
# BASELINE STRATEGIES
# =============================================================================


def create_baseline_players(n_players: int,
                            n_rounds: int) -> list[SimplePlayer]:
    baseline_players = [
        SimplePlayer("A-D", Defector),
        SimplePlayer("A-C", Cooperator),
    ]
    baseline_players += [
        SimplePlayer(f"CC({i})", ConditionalCooperator(C, i))
        for i in range(1, args.n_players)
    ]
    baseline_players += [
        SimplePlayer(f"CD({i})", ConditionalDefector(D, i))
        for i in range(1, args.n_players)
    ]
    return baseline_players


def compute_baselines(n_players: int,
                      n_rounds: int) -> dict[str, dict[CooperatorCounts, float]]:
    baseline_players = create_baseline_players(n_players, n_rounds)
    baseline_features = {}
    for player in baseline_players:
        features = compute_features(player, 1)
        baseline_features[player.id.name] = features

        mean = np.mean(list(features.values()))
        logger.info(f"{player.id.name}: {mean:.3f}")
    return baseline_features


# =============================================================================
# METRICS
# =============================================================================


@dataclass
class DiversityMetrics:
    """Metrics for a single gene."""
    gene: Gene
    n_strategies: int
    mean_pairwise_distance: float
    mean_pairwise_distance_normalised: float  # relative to random baseline
    participation_ratio: float

    def __str__(self):
        return (f"{self.gene}: n={self.n_strategies}, "
                f"MPD={self.mean_pairwise_distance:.3f} "
                f"(norm={self.mean_pairwise_distance_normalised:.2f}), "
                f"PR={self.participation_ratio:.2f}")


@dataclass
class BetweenSetMetrics:
    """Metrics comparing attitudes within a game/model."""
    game: str
    model: str
    centroid_distance: float
    cohens_d: float

    def __str__(self):
        return (f"{self.game}/{self.model}: "
                f"centroid_dist={self.centroid_distance:.3f}, "
                f"Cohen's d={self.cohens_d:.2f}")


@dataclass
class AttitudeComparisonMetrics:
    """Metrics comparing a non-base attitude to both base attitudes."""
    game: str
    model: str
    attitude: Attitude
    n_strategies: int
    # vs collective
    d_vs_collective: float
    d_vs_collective_ci_lower: float
    d_vs_collective_ci_upper: float
    centroid_dist_collective: float
    # vs selfish
    d_vs_selfish: float
    d_vs_selfish_ci_lower: float
    d_vs_selfish_ci_upper: float
    centroid_dist_selfish: float
    # ratio: d_to_own_base / d_to_other_base (< 1 means closer to own base)
    proximity_ratio: float

    def __str__(self):
        return (
            f"{self.game}/{self.model}/{self.attitude.value} "
            f"(n={self.n_strategies}): "
            f"d_coll={self.d_vs_collective:.2f} "
            f"[{self.d_vs_collective_ci_lower:.2f}, {self.d_vs_collective_ci_upper:.2f}], "
            f"d_expl={self.d_vs_selfish:.2f} "
            f"[{self.d_vs_selfish_ci_lower:.2f}, {self.d_vs_selfish_ci_upper:.2f}], "
            f"ratio(own/other)={self.proximity_ratio:.2f}"
        )


def compute_random_baseline_distance(n_features: int,
                                     n_samples: int = 500) -> float:
    """Compute mean pairwise distance for random [0,1] vectors."""
    random_X = np.random.uniform(0, 1, (n_samples, n_features))
    distances = pdist(random_X, metric='euclidean')
    return float(np.mean(distances))


def compute_within_set_metrics(X: np.ndarray,
                               random_baseline: float) -> tuple[float, float]:
    """
    Compute within-set diversity metrics.

    Returns:
        (mean_pairwise_distance, normalized_distance)
    """
    if len(X) < 2:
        return 0.0, 0.0
    distances = pdist(X, metric='euclidean')
    mpd = float(np.mean(distances))
    return mpd, mpd / random_baseline


def compute_participation_ratio(X: np.ndarray) -> float:
    """
    Compute participation ratio from data matrix.
    PR = (sum of eigenvalues)^2 / sum of eigenvalues^2
    """
    if len(X) < 2:
        return 1.0
    # Center the data
    X_centered = X - X.mean(axis=0)
    # Compute covariance eigenvalues
    cov = np.cov(X_centered.T)
    eigenvalues = np.linalg.eigvalsh(cov)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]  # numerical stability

    if len(eigenvalues) == 0:
        return 1.0

    return (eigenvalues.sum()**2) / (eigenvalues**2).sum()


def compute_between_set_metrics(
        X_collective: np.ndarray,
        X_selfish: np.ndarray) -> tuple[float, float]:
    """
    Compute between-set metrics.

    Returns:
        (centroid_distance, cohens_d)
    """
    if len(X_collective) == 0 or len(X_selfish) == 0:
        return np.nan, np.nan

    centroid_c = X_collective.mean(axis=0)
    centroid_e = X_selfish.mean(axis=0)
    centroid_distance = np.linalg.norm(centroid_c - centroid_e)

    # Cohen's d: centroid distance / pooled within-set std
    # Pooled std: sqrt of average variance across both sets
    var_c = np.var(X_collective, axis=0).mean() if len(X_collective) > 1 else 0
    var_e = np.var(X_selfish,
                   axis=0).mean() if len(X_selfish) > 1 else 0

    n_c, n_e = len(X_collective), len(X_selfish)
    pooled_var = ((n_c - 1) * var_c +
                  (n_e - 1) * var_e) / (n_c + n_e - 2) if (n_c + n_e) > 2 else 1
    pooled_std = np.sqrt(pooled_var *
                         X_collective.shape[1])  # scale by sqrt(dimensions)

    cohens_d = centroid_distance / pooled_std if pooled_std > 0 else np.nan

    return centroid_distance, cohens_d


def compute_cohens_d(X_a: np.ndarray, X_b: np.ndarray) -> float:
    """
    Multivariate Cohen's d: centroid distance / pooled within-set std.

    Same formulation as compute_between_set_metrics for consistency.
    """
    if len(X_a) < 2 or len(X_b) < 2:
        return np.nan

    centroid_distance = np.linalg.norm(X_a.mean(axis=0) - X_b.mean(axis=0))

    n_a, n_b = len(X_a), len(X_b)
    var_a = np.var(X_a, axis=0).mean()
    var_b = np.var(X_b, axis=0).mean()

    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)
    pooled_std = np.sqrt(pooled_var * X_a.shape[1])

    return centroid_distance / pooled_std if pooled_std > 0 else np.nan


def bootstrap_cohens_d(
    X_a: np.ndarray,
    X_b: np.ndarray,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
) -> tuple[float, float, float]:
    """
    Bootstrap confidence interval for multivariate Cohen's d.

    Returns:
        (point_estimate, ci_lower, ci_upper)
    """
    point = compute_cohens_d(X_a, X_b)
    if np.isnan(point):
        return np.nan, np.nan, np.nan

    rng = np.random.default_rng(42)
    boot_ds = []
    for _ in range(n_bootstrap):
        idx_a = rng.choice(len(X_a), size=len(X_a), replace=True)
        idx_b = rng.choice(len(X_b), size=len(X_b), replace=True)
        d = compute_cohens_d(X_a[idx_a], X_b[idx_b])
        if not np.isnan(d):
            boot_ds.append(d)

    if len(boot_ds) < 10:
        return point, np.nan, np.nan

    alpha = (1 - confidence) / 2
    ci_lower = float(np.percentile(boot_ds, 100 * alpha))
    ci_upper = float(np.percentile(boot_ds, 100 * (1 - alpha)))
    return point, ci_lower, ci_upper


def compute_attitude_comparison(
    X_nonbase: np.ndarray,
    X_collective: np.ndarray,
    X_selfish: np.ndarray,
    game: str,
    model: str,
    attitude: Attitude,
    n_bootstrap: int = 1000,
) -> AttitudeComparisonMetrics:
    """Compare a non-base attitude to both base attitudes in original feature space."""

    d_c, ci_c_lo, ci_c_hi = bootstrap_cohens_d(X_nonbase, X_collective, n_bootstrap)
    d_e, ci_e_lo, ci_e_hi = bootstrap_cohens_d(X_nonbase, X_selfish, n_bootstrap)

    centroid_c = float(np.linalg.norm(
        X_nonbase.mean(axis=0) - X_collective.mean(axis=0)
    )) if len(X_nonbase) > 0 and len(X_collective) > 0 else np.nan

    centroid_e = float(np.linalg.norm(
        X_nonbase.mean(axis=0) - X_selfish.mean(axis=0)
    )) if len(X_nonbase) > 0 and len(X_selfish) > 0 else np.nan

    # Proximity ratio: distance to own base / distance to other base
    own_base = attitude.to_base_attitude()
    if own_base == Attitude.COLLECTIVE:
        ratio = d_c / d_e if d_e > 0 else np.nan
    else:
        ratio = d_e / d_c if d_c > 0 else np.nan

    return AttitudeComparisonMetrics(
        game=game,
        model=model,
        attitude=attitude,
        n_strategies=len(X_nonbase),
        d_vs_collective=d_c,
        d_vs_collective_ci_lower=ci_c_lo,
        d_vs_collective_ci_upper=ci_c_hi,
        centroid_dist_collective=centroid_c,
        d_vs_selfish=d_e,
        d_vs_selfish_ci_lower=ci_e_lo,
        d_vs_selfish_ci_upper=ci_e_hi,
        centroid_dist_selfish=centroid_e,
        proximity_ratio=ratio,
    )


def get_feature_vectors_for_gene(
    X_all: np.ndarray,
    labels_all: np.ndarray,
    game_labels: np.ndarray,
    game_name: str,
    pca_data: dict,
    model: str,
    attitude: Attitude,
) -> np.ndarray:
    """Extract feature vectors for a specific (game, model, attitude) combination."""
    mask = game_labels == game_name
    genes = pca_data[game_name]['genes']
    matching = [g for g in genes if g.model == model and g.attitude == attitude]
    if not matching:
        return np.empty((0, X_all.shape[1]))
    gene_strs = [str(g) for g in matching]
    gene_mask = mask & np.isin(labels_all, gene_strs)
    return X_all[gene_mask]


def compute_game_variance_explained(X: np.ndarray,
                                    game_labels: np.ndarray) -> float:
    """
    Compute proportion of variance explained by game membership.

    Multivariate η² = trace(S_between) / trace(S_total)
    """
    games = np.unique(game_labels)
    global_centroid = X.mean(axis=0)

    # Total sum of squares
    ss_total = np.sum((X - global_centroid)**2)

    # Between-group sum of squares
    ss_between = 0.0
    for game in games:
        mask = game_labels == game
        n_game = mask.sum()
        game_centroid = X[mask].mean(axis=0)
        ss_between += n_game * np.sum((game_centroid - global_centroid)**2)

    return ss_between / ss_total if ss_total > 0 else 0.0


# =============================================================================
# PCA HELPERS
# =============================================================================


def fit_base_attitude_pca(X_all, labels_all, game_labels, pca_data, games):
    """
    Fit PCA on base attitudes only, return transformer and transformed data.

    Returns:
        pca: fitted PCA object
        X_pca_all: all data projected into base-attitude PCA space
        base_mask: boolean mask for base attitude rows
    """
    base_attitude_set = set(Attitude.base_attitudes())
    base_mask = np.zeros(len(X_all), dtype=bool)

    for game_name in games:
        game_mask = game_labels == game_name
        for gene in pca_data[game_name]['genes']:
            if gene.attitude in base_attitude_set:
                gene_mask = game_mask & (labels_all == str(gene))
                base_mask |= gene_mask

    X_base = X_all[base_mask]
    logger.info(
        f"Fitting PCA on {base_mask.sum()} base-attitude strategies "
        f"(out of {len(X_all)} total)"
    )

    n_components = min(10, X_base.shape[1], X_base.shape[0])
    pca = PCA(n_components=n_components)
    pca.fit(X_base)

    # Transform ALL data (base + non-base) into this space
    X_pca_all = pca.transform(X_all)

    return pca, X_pca_all, base_mask


# =============================================================================
# PLOTTING HELPERS
# =============================================================================

# Baselines with labels on the left (defector-ish strategies)
BASELINE_LABELS_LEFT = {"A-D", "A-D,LR-C", "CD(1)", "CC(3)"}


def plot_covariance_ellipse(ax, mean, cov, n_std=1.0, **kwargs):
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(np.maximum(eigenvalues, 0))
    ellipse = Ellipse(mean, width, height, angle=angle, **kwargs)
    ax.add_patch(ellipse)
    return ellipse


def plot_baselines(ax, baseline_pca, baseline_labels, marker_size=120):
    """Plot baseline strategies with positioned labels."""
    for i, name in enumerate(baseline_labels):
        ax.scatter(baseline_pca[i, 0],
                   baseline_pca[i, 1],
                   marker='X',
                   s=marker_size,
                   color='gray',
                   edgecolors='black',
                   linewidths=1,
                   zorder=6)
        ha = 'right' if name in BASELINE_LABELS_LEFT else 'left'
        offset = -5 if name in BASELINE_LABELS_LEFT else 5
        ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]),
                    ha=ha,
                    xytext=(offset, 0),
                    textcoords='offset points')


def plot_pca(ax, X_pca, genes, labels, baseline_pca, baseline_labels, title,
             pca):
    """Plot PCA scatter with ellipses for each gene."""
    colors = plt.colormaps.get_cmap('tab10')(np.linspace(0, 1, len(genes)))
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
                       marker='o',
                       s=100,
                       color=colors[i],
                       edgecolors='black',
                       linewidths=1.5,
                       zorder=5)

            if len(points) > 2:
                cov = np.cov(points.T)
                plot_covariance_ellipse(ax,
                                        mean_pt,
                                        cov,
                                        n_std=1.0,
                                        facecolor=colors[i],
                                        alpha=0.25,
                                        edgecolor=colors[i],
                                        linewidth=1.5)
        handles.append((scatter, str(gene)))

    plot_baselines(ax, baseline_pca, baseline_labels)

    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
    ax.set_title(title)
    ax.legend([h[0] for h in handles], [h[1] for h in handles],
              loc='upper center',
              frameon=False,
              bbox_to_anchor=(0.4, 1.05),
              ncol=2)


def plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca, baseline_labels, games, pca, output_dir):
    """
    Create a 2×3 grid: rows=attitudes, columns=games.
    Each subplot shows all models for that game/attitude combination.
    """
    attitudes = Attitude.base_attitudes()
    attitude_names = {
        Attitude.COLLECTIVE: "Collective",
        Attitude.SELFISH: "Selfish"
    }

    # Extract unique models across all genes
    all_genes = []
    for g in games:
        all_genes.extend(pca_data[g]['genes'])
    models = sorted(set(gene.model for gene in all_genes))
    cmap = plt.colormaps.get_cmap('tab10')
    model_colors = {model: cmap(i) for i, model in enumerate(models)}

    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE, sharex=True, sharey=True)

    for col, game in enumerate(games):
        game_mask = game_labels == game
        genes_for_game = pca_data[game]['genes']

        for row, attitude in enumerate(attitudes):
            ax = axes[row, col]

            # Filter genes for this attitude
            genes_this_attitude = [
                g for g in genes_for_game if g.attitude == attitude
            ]
            handles = []

            for model in models:
                # Find the gene for this model+attitude (if exists)
                matching_genes = [
                    g for g in genes_this_attitude if g.model == model
                ]
                if not matching_genes:
                    continue
                gene = matching_genes[0]

                mask = game_mask & (labels_all == str(gene))
                points = X_pca_combined[mask, :2]

                if len(points) == 0:
                    continue

                color = model_colors[model]
                scatter = ax.scatter(points[:, 0],
                                     points[:, 1],
                                     alpha=0.3,
                                     s=10,
                                     color=color)

                # Centroid
                mean_pt = points.mean(axis=0)
                ax.scatter(mean_pt[0],
                           mean_pt[1],
                           marker='o',
                           s=100,
                           color=color,
                           edgecolors='black',
                           linewidths=1.5,
                           zorder=5)

                # Ellipse
                if len(points) > 2:
                    cov = np.cov(points.T)
                    plot_covariance_ellipse(ax,
                                            mean_pt,
                                            cov,
                                            n_std=1.0,
                                            facecolor=color,
                                            alpha=0.25,
                                            edgecolor=color,
                                            linewidth=1.5)

                handles.append((scatter, model))

            # Baselines (smaller markers for grid)
            plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)

            # Labels
            if row == 0:
                ax.set_title(GAME_MAPPING[game])
            if col == 0:
                ax.set_ylabel(
                    f"{attitude_names[attitude]}\nPC2 ({pca.explained_variance_ratio_[1]:.1%})"
                )
            if row == 1:
                ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')

    # Shared legend for models (outside the grid on the right)
    legend_handles = [
        plt.Line2D([0], [0],
                   marker='o',
                   color='w',
                   markerfacecolor=model_colors[m],
                   markersize=10,
                   label=m) for m in models
    ]
    fig.legend(handles=legend_handles,
               loc='upper center',
               frameon=False,
               bbox_to_anchor=(0.4, 1.05),
               ncol=len(registry.available_models))

    plt.tight_layout(rect=[0, 0, 0.95, 1])  # Leave space for legend
    plt.savefig(output_dir / f"pca_by_game.{FORMAT}",
                format=FORMAT,
                bbox_inches='tight')
    plt.close()
    logger.info(
        f"Saved combined PCA grid to {output_dir / f'pca_by_game.{FORMAT}'}")


def plot_pca_by_model(pca_data, X_pca_combined, labels_all, game_labels,
                      baseline_pca, baseline_labels, games, pca, output_dir):
    """
    Create a grid with one subplot per model.
    Each subplot shows all games and attitudes for that model.
    """
    # Extract unique models
    all_genes = []
    for g in games:
        all_genes.extend(pca_data[g]['genes'])
    models = sorted(set(gene.model for gene in all_genes))

    # Grid layout based on number of models
    n_models = len(models)
    n_cols = 3
    n_rows = (n_models + n_cols - 1) // n_cols

    # Color by game, marker style by attitude
    game_colors = dict(
        zip(games,
            plt.colormaps.get_cmap('Set1')(np.linspace(0, 1, len(games)))))
    attitude_markers = {Attitude.COLLECTIVE: 'o', Attitude.SELFISH: 's'}

    fig, axes = plt.subplots(n_rows,
                             n_cols,
                             figsize=FIGSIZE,
                             sharex=True,
                             sharey=True)
    axes = np.atleast_2d(axes)

    for idx, model in enumerate(models):
        row, col = divmod(idx, n_cols)
        ax = axes[row, col]

        for game in games:
            game_mask = game_labels == game
            genes_for_game = pca_data[game]['genes']
            color = game_colors[game]

            for attitude in [Attitude.COLLECTIVE, Attitude.SELFISH]:
                matching_genes = [
                    g for g in genes_for_game
                    if g.model == model and g.attitude == attitude
                ]
                if not matching_genes:
                    continue
                gene = matching_genes[0]

                mask = game_mask & (labels_all == str(gene))
                points = X_pca_combined[mask, :2]

                if len(points) == 0:
                    continue

                marker = attitude_markers[attitude]
                ax.scatter(points[:, 0],
                           points[:, 1],
                           alpha=0.3,
                           s=10,
                           color=color,
                           marker=marker)

                # Centroid
                mean_pt = points.mean(axis=0)
                ax.scatter(mean_pt[0],
                           mean_pt[1],
                           marker=marker,
                           s=100,
                           color=color,
                           edgecolors='black',
                           linewidths=1.5,
                           zorder=5)

                # Ellipse
                if len(points) > 2:
                    cov = np.cov(points.T)
                    plot_covariance_ellipse(ax,
                                            mean_pt,
                                            cov,
                                            n_std=1.0,
                                            facecolor=color,
                                            alpha=0.25,
                                            edgecolor=color,
                                            linewidth=1.5)

        plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)
        ax.set_title(MODELS_MAPPING[model])

        if col == 0:
            ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        if row == n_rows - 1:
            ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')

    # Hide unused subplots
    for idx in range(n_models, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row, col].set_visible(False)

    # Legend: games (colors) + attitudes (markers)
    legend_handles = []
    for game in games:
        legend_handles.append(
            plt.Line2D([0], [0],
                       marker='o',
                       color='w',
                       markerfacecolor=game_colors[game],
                       markersize=10,
                       label=GAME_MAPPING[game]))
    legend_handles.append(
        plt.Line2D([0], [0],
                   marker='o',
                   color='gray',
                   markersize=8,
                   label='Collective'))
    legend_handles.append(
        plt.Line2D([0], [0],
                   marker='s',
                   color='gray',
                   markersize=8,
                   label='Selfish'))

    fig.legend(handles=legend_handles,
               loc='upper center',
               frameon=False,
               bbox_to_anchor=(0.5, 1.02),
               ncol=len(games) + 2,
               columnspacing=0.6,
               handletextpad=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_dir / f"pca_by_model.{FORMAT}",
                format=FORMAT,
                bbox_inches='tight')
    plt.close()
    logger.info(
        f"Saved per-model PCA grid to {output_dir / f'pca_by_model.{FORMAT}'}")


def find_centroid_strategies(X, labels, game_labels, pca_data, games):
    """For each (game, attitude, model), find the strategy closest to the group centroid."""
    for game_name in games:
        logger.info(f"\n  {game_name}:")
        mask = game_labels == game_name
        genes = pca_data[game_name]['genes']
        metadata = pca_data[game_name]['metadata']
        X_game = X[mask]
        labels_game = labels[mask]

        # Build index mapping from game-local index to metadata
        game_indices = np.where(mask)[0]

        models = sorted(set(g.model for g in genes))
        for model in models:
            for attitude in [Attitude.COLLECTIVE, Attitude.SELFISH]:
                matching_genes = [
                    g for g in genes
                    if g.model == model and g.attitude == attitude
                ]
                if not matching_genes:
                    continue

                gene_strs = [str(g) for g in matching_genes]
                gene_mask = np.isin(labels_game, gene_strs)
                X_group = X_game[gene_mask]

                if len(X_group) == 0:
                    continue

                centroid = X_group.mean(axis=0, keepdims=True)
                dists = cdist(centroid, X_group, metric='euclidean')[0]
                local_idx = np.argmin(dists)

                # Map back to metadata
                game_local_indices = np.where(gene_mask)[0]
                metadata_idx = game_local_indices[local_idx]
                gene, strategy_name, feature_dict = metadata[metadata_idx]

                coop_rate = np.mean(list(feature_dict.values()))
                logger.info(
                    f"    {gene}: {strategy_name} "
                    f"(dist={dists[local_idx]:.3f}, coop={coop_rate:.2%})"
                )


# =============================================================================
# EXTREMA ANALYSIS
# =============================================================================


def find_extrema(X_pca, metadata):
    """Find strategies at plot extrema."""
    extrema_indices = {
        'top_left': np.argmin(X_pca[:, 0] - X_pca[:, 1]),
        'top_right': np.argmax(X_pca[:, 0] + X_pca[:, 1]),
        'bottom_left': np.argmin(X_pca[:, 0] + X_pca[:, 1]),
        'bottom_right': np.argmax(X_pca[:, 0] - X_pca[:, 1]),
        'top': np.argmin(X_pca[:, 0]),
        'right': np.argmax(X_pca[:, 1]),
        'bottom': np.argmin(X_pca[:, 0]),
        'left': np.argmin(X_pca[:, 1]),
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

        logger.info(f"\n{position.upper().replace('_', ' ')}:")
        logger.info(f"  Gene: {gene}")
        logger.info(f"  Strategy: {strategy_name}")
        logger.info(f"  PC1: {X_pca[idx, 0]:.3f}, PC2: {X_pca[idx, 1]:.3f}")

        coop_rate = np.mean(list(feature_dict.values()))
        logger.info(f"  Overall cooperation rate: {coop_rate:.2%}")

    return results


def extrema_analysis(tl):
    logger.info(f"\n{'='*60}")
    logger.info(f"EXTREMA ANALYSIS")
    logger.info(f"{'='*60}")
    features = tl['features']
    logger.info(f"Behavior by context (showing first 20 contexts):")
    for i, (context, coop_prob) in enumerate(list(features.items())[:20]):
        # Context is tuple of tuples, flatten and convert to string
        if len(context) == 0:
            context_str = 'Start'
        else:
            context_str = '|'.join(str(c) for c in context)
        logger.info(f"  {context_str}: {coop_prob:.1%} coop)")


def plot_extrema(extrema_info, ax):
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


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    args = parse_args()
    output_dir = get_output_dir(args)

    log_file = output_dir / "logs" / "diversity.log"
    setup_logging(log_file)
    logger = logging.getLogger(__name__)

    logger.info(f"Running diversity.py for games: {args.games}")

    # ==========================================================================
    # PHASE 1: Load/compute features for each game (with caching)
    # ==========================================================================
    pca_data = {}

    for game_name in args.games:
        game_class, _ = get_game_type(game_name)
        description = STANDARD_GENERATORS[game_name + "_default"](
            n_players=args.n_players, n_rounds=args.n_rounds)
        registry = StrategyRegistry(strategies_dir=args.strategies_dir,
                                    game_name=game_name,
                                    models=args.models)
        genes = sorted(list(registry.available_genes), key=str)

        results_dict = {}

        for gene in genes:
            # Check cache first
            if not args.recompute:
                cached_data = load_features(game_name, gene, args)
                if cached_data is not None:
                    results_dict[gene] = cached_data
                    continue

            all_specs = registry.get_all_specs(gene)
            n_strategies = len(all_specs) if args.n_strategies is None else min(
                len(all_specs), args.n_strategies)
            chunks = chunk_indices(n_strategies, args.n_processes)

            logger.info(
                f"Computing {n_strategies} strategies for {gene} in {len(chunks)} chunks"
            )

            with Pool(processes=args.n_processes) as pool:
                chunk_results = pool.map(compute_strategy_chunk, chunks)

            # Aggregate results
            strategy_features = {}
            for chunk_result in chunk_results:
                for strategy_name, features in chunk_result:
                    strategy_features[strategy_name] = features

            save_features(strategy_features, game_name, gene, args)
            results_dict[gene] = strategy_features

        logger.info(f"Results for {len(results_dict)} genes, with "
                    f"{sum(len(v) for v in results_dict.values())} strategies "
                    f"in total for {game_name}")

        X_game = []
        labels_game = []
        metadata_game = []
        for gene, strategy_features in results_dict.items():
            for strategy_name, feature_dict in strategy_features.items():
                X_game.append(list(feature_dict.values()))
                labels_game.append(str(gene))
                metadata_game.append((gene, strategy_name, feature_dict))

        pca_data[game_name] = {
            'X': np.array(X_game),
            'labels': np.array(labels_game),
            'metadata': metadata_game,
            'genes': genes,
        }

    # ==========================================================================
    # PHASE 2: Compute baselines (same for all games - depends only on n_players, n_rounds)
    # ==========================================================================
    logger.info(f"\n{'='*60}")
    logger.info("COMPUTING BASELINES")
    logger.info(f"{'='*60}")

    # Need to set globals for baseline computation (use first game's setup)
    game_class, _ = get_game_type(args.games[0])
    description = STANDARD_GENERATORS[args.games[0] + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    baseline_features = compute_baselines(args.n_players, args.n_rounds)
    baseline_labels = list(baseline_features.keys()) + ['Rnd(0.5)']
    baseline_X = [list(d.values()) for d in baseline_features.values()]
    n_features = len(baseline_X[0])
    baseline_X = np.array(baseline_X + [[0.5] * n_features])

    # ==========================================================================
    # PHASE 3: Combined PCA (fit on base attitudes only, project everything)
    # ==========================================================================
    logger.info(f"\n{'='*60}")
    logger.info("COMBINED PCA ANALYSIS (fitted on base attitudes only)")
    logger.info(f"{'='*60}")

    # Stack all games
    X_all = np.vstack([pca_data[g]['X'] for g in args.games])
    labels_all = np.concatenate([pca_data[g]['labels'] for g in args.games])
    game_labels = np.concatenate(
        [[g] * len(pca_data[g]['X']) for g in args.games])

    # Fit PCA on base attitudes only, transform everything
    pca_combined, X_pca_combined, base_mask = fit_base_attitude_pca(
        X_all, labels_all, game_labels, pca_data, args.games
    )
    baseline_pca_combined = pca_combined.transform(baseline_X)

    logger.info(
        f"PCA explained variance (base attitudes): "
        f"{pca_combined.explained_variance_ratio_[:5]}"
    )

    # Random baseline for normalization
    random_baseline_dist = compute_random_baseline_distance(X_all.shape[1])

    # Scree plot (combined)
    cumulative = np.cumsum(pca_combined.explained_variance_ratio_)
    plt.figure()
    plt.plot(range(1, len(cumulative) + 1), cumulative, 'o-')
    plt.axhline(y=0.9, color='r', linestyle='--', label='90% threshold')
    plt.xlabel('Component')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Combined PCA Scree Plot (base attitudes)')
    plt.legend()
    plt.savefig(output_dir / f"scree_combined.{FORMAT}", format=FORMAT)
    plt.close()

    # Individual plots per game (using combined PCA)
    for game_name in args.games:
        mask = game_labels == game_name
        X_game_pca = X_pca_combined[mask]
        labels_game = labels_all[mask]
        genes = pca_data[game_name]['genes']
        metadata = pca_data[game_name]['metadata']

        fig, ax = plt.subplots(figsize=FIGSIZE)
        plot_pca(ax, X_game_pca, genes, labels_game, baseline_pca_combined,
                 baseline_labels, game_name, pca_combined)

        if args.plot_extrema:
            extrema_info = find_extrema(X_game_pca, metadata)
            extrema_analysis(
                extrema_info.get('bottom_right',
                                 list(extrema_info.values())[0]))
            plot_extrema(extrema_info, ax)

        plt.tight_layout()
        plt.savefig(output_dir / f"pca_{game_name}.{FORMAT}",
                    format=FORMAT,
                    bbox_inches='tight')
        plt.close()

    # Combined 2x3 grid plot (attitudes × games)
    plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca_combined, baseline_labels, args.games,
                     pca_combined, output_dir)

    plot_pca_by_model(pca_data, X_pca_combined, labels_all, game_labels,
                      baseline_pca_combined, baseline_labels, args.games,
                      pca_combined, output_dir)

    # ==========================================================================
    # PHASE 4: Compute and display metrics (base attitudes)
    # ==========================================================================
    logger.info(f"\n{'='*60}")
    logger.info("DIVERSITY METRICS (Within-set)")
    logger.info(f"{'='*60}")

    for game_name in args.games:
        logger.info(f"\n  {game_name}:")
        mask = game_labels == game_name
        for gene in pca_data[game_name]['genes']:
            gene_mask = mask & (labels_all == str(gene))
            X_gene = X_all[gene_mask]
            coop_rate = float(X_gene.mean()) if len(X_gene) > 0 else 0.0
            mpd, mpd_norm = compute_within_set_metrics(X_gene,
                                                       random_baseline_dist)
            pr = compute_participation_ratio(X_gene)
            logger.info(
                f"    {gene}: coop={coop_rate:.3f}, MPD={mpd:.3f} (norm={mpd_norm:.2f}), PR={pr:.2f}")

    logger.info(f"\n{'='*60}")
    logger.info("VARIANCE EXPLAINED BY GAME MEMBERSHIP")
    logger.info(f"{'='*60}")

    # Per model (do strategies from the same model behave similarly across games?)
    models = sorted(set(g.model for g in pca_data[args.games[0]]['genes']))
    for model in models:
        model_mask = np.array([model in label for label in labels_all])
        eta_sq_model = compute_game_variance_explained(X_all[model_mask],
                                                       game_labels[model_mask])
        logger.info(f"  {model}: η² = {eta_sq_model:.3f}")

    logger.info(f"\n{'='*60}")
    logger.info("CENTROID-NEAREST STRATEGIES")
    logger.info(f"{'='*60}")

    find_centroid_strategies(X_all, labels_all, game_labels, pca_data, args.games)

    logger.info(f"\n{'='*60}")
    logger.info("BETWEEN-SET METRICS (Collective vs Selfish)")
    logger.info(f"{'='*60}")

    for game_name in args.games:
        logger.info(f"\n  {game_name}:")
        genes = pca_data[game_name]['genes']

        # Group genes by model
        models = set(gene.model for gene in genes)

        for model in sorted(models):
            # Get genes for this model, split by attitude
            collective_genes = [
                g for g in genes
                if g.model == model and g.attitude == Attitude.COLLECTIVE
            ]
            selfish_genes = [
                g for g in genes
                if g.model == model and g.attitude == Attitude.SELFISH
            ]

            if not collective_genes or not selfish_genes:
                continue

            # Get corresponding feature vectors
            mask = game_labels == game_name
            X_collective = X_all[
                mask & np.isin(labels_all, [str(g) for g in collective_genes])]
            X_selfish = X_all[
                mask &
                np.isin(labels_all, [str(g) for g in selfish_genes])]

            if len(X_collective) == 0 or len(X_selfish) == 0:
                continue

            centroid_dist, cohens_d = compute_between_set_metrics(
                X_collective, X_selfish)
            metrics = BetweenSetMetrics(game=game_name,
                                        model=model,
                                        centroid_distance=centroid_dist,
                                        cohens_d=cohens_d)
            logger.info(f"    {metrics}")

    # ==========================================================================
    # PHASE 5: Non-base attitude comparison
    # ==========================================================================
    non_base_attitudes = [a for a in Attitude if a not in Attitude.base_attitudes()]

    if not non_base_attitudes:
        logger.info("No non-base attitudes found, skipping Phase 5")
    else:
        logger.info(f"\n{'='*60}")
        logger.info("NON-BASE ATTITUDE COMPARISON (Cohen's d to base attitudes)")
        logger.info(f"{'='*60}")

        all_comparisons: list[AttitudeComparisonMetrics] = []

        for game_name in args.games:
            logger.info(f"\n  {game_name}:")
            genes = pca_data[game_name]['genes']
            models_in_game = sorted(set(g.model for g in genes))

            for model in models_in_game:
                # Get base attitude feature vectors
                X_collective = get_feature_vectors_for_gene(
                    X_all, labels_all, game_labels, game_name,
                    pca_data, model, Attitude.COLLECTIVE,
                )
                X_selfish = get_feature_vectors_for_gene(
                    X_all, labels_all, game_labels, game_name,
                    pca_data, model, Attitude.SELFISH,
                )

                if len(X_collective) == 0 or len(X_selfish) == 0:
                    continue

                for attitude in non_base_attitudes:
                    X_nb = get_feature_vectors_for_gene(
                        X_all, labels_all, game_labels, game_name,
                        pca_data, model, attitude,
                    )
                    if len(X_nb) < 2:
                        continue

                    metrics = compute_attitude_comparison(
                        X_nb, X_collective, X_selfish,
                        game_name, model, attitude,
                        n_bootstrap=1000,
                    )
                    all_comparisons.append(metrics)
                    logger.info(f"    {metrics}")

        # Summary table
        if all_comparisons:
            logger.info(f"\n{'='*60}")
            logger.info("ATTITUDE COMPARISON SUMMARY")
            logger.info(f"{'='*60}")

            # Group by attitude, average across games and models
            by_attitude: dict[Attitude, list[AttitudeComparisonMetrics]] = defaultdict(list)
            for m in all_comparisons:
                by_attitude[m.attitude].append(m)

            for attitude, metrics_list in sorted(by_attitude.items(), key=lambda x: x[0].value):
                own_base = attitude.to_base_attitude()
                d_own = np.mean([
                    m.d_vs_collective if own_base == Attitude.COLLECTIVE else m.d_vs_selfish
                    for m in metrics_list
                ])
                d_other = np.mean([
                    m.d_vs_selfish if own_base == Attitude.COLLECTIVE else m.d_vs_collective
                    for m in metrics_list
                ])
                ratio = np.mean([m.proximity_ratio for m in metrics_list if not np.isnan(m.proximity_ratio)])
                logger.info(
                    f"  {attitude.value} (base={own_base.value}): "
                    f"d_to_own_base={d_own:.2f}, d_to_other_base={d_other:.2f}, "
                    f"mean_ratio={ratio:.2f}"
                )
