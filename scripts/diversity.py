# pylint: disable=redefined-outer-name,missing-function-docstring,missing-class-docstring,possibly-used-before-assignment

import argparse
import logging
from dataclasses import dataclass
from itertools import combinations_with_replacement, product
from multiprocessing import Pool
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from scipy.spatial.distance import pdist, cdist
from sklearn.decomposition import PCA

from emergent_llm.common import (
    Action,
    Attitude,
    C,
    D,
    GameHistory,
    GameState,
    Gene,
    PlayerHistory,
    setup,
)
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import (
    BasePlayer,
    ConditionalCooperator,
    ConditionalDefector,
    Cooperator,
    Defector,
    HistoricalCooperator,
    LLMPlayer,
    SimplePlayer,
    SpecialRounds,
)

FIGSIZE, FORMAT = setup('fullscreen')

OpponentActions = tuple[tuple[Action, ...], ...]

# =============================================================================
# ARGUMENT PARSING
# =============================================================================


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run PCA for strategies")

    parser.add_argument("--games",
                        type=str,
                        nargs='+',
                        default=["public_goods", "collective_risk", "common_pool"],
                        choices=["public_goods", "collective_risk", "common_pool", "public_goods_prompt"],
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
                        default=20,
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
    parser.add_argument("--results_dir",
                        type=str,
                        default="results")

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


def load_features(
        game_name: str, gene: Gene,
        args) -> dict[str, dict[OpponentActions, float]] | None:
    cache_path = get_cache_path(game_name, gene, args)
    if not cache_path.exists():
        logger.info(f"Could not find existing cache at {cache_path}")
        return None
    with open(cache_path, 'rb') as f:
        features_dict = pickle.load(f)
    logger.info(f"Loaded features for {len(features_dict.keys())} strategies from {cache_path}")
    return features_dict


# =============================================================================
# FEATURE COMPUTATION (uses globals set per-game in main)
# =============================================================================


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


def compute_features(player: BasePlayer, n_games: int) -> dict[OpponentActions, float]:
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


def chunk_indices(n_items: int, n_chunks: int) -> list[list[int]]:
    """Split indices into approximately equal chunks."""
    chunk_size = (n_items + n_chunks - 1) // n_chunks
    return [list(range(i, min(i + chunk_size, n_items)))
            for i in range(0, n_items, chunk_size)]


def compute_strategy_chunk(strategy_indices: list[int]) -> list[tuple[str, dict[OpponentActions, float]]]:
    """Compute features for a chunk of strategies. Runs in worker process."""
    worker_registry = StrategyRegistry(args.strategies_dir, game_name, [gene.model])
    specs = worker_registry.get_all_specs(gene)

    results = []
    for idx in strategy_indices:
        spec = specs[idx]
        player = LLMPlayer("testing", gene, description, spec.strategy_class)
        features = compute_features(player, args.n_games)
        results.append((spec.strategy_class.__name__, features))
        logger.info(f"{gene.model} {spec.strategy_class.__name__}: {np.mean(list(features.values())):.3f}")

    return results


# =============================================================================
# BASELINE STRATEGIES
# =============================================================================


def create_baseline_players(n_players: int, n_rounds: int) -> list[SimplePlayer]:
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
                      n_rounds: int) -> dict[str, dict[OpponentActions, float]]:
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


def compute_random_baseline_distance(n_features: int, n_samples: int = 500) -> float:
    """Compute mean pairwise distance for random [0,1] vectors."""
    random_X = np.random.uniform(0, 1, (n_samples, n_features))
    distances = pdist(random_X, metric='euclidean')
    return float(np.mean(distances))


def compute_within_set_metrics(X: np.ndarray, random_baseline: float) -> tuple[float, float]:
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

    return (eigenvalues.sum() ** 2) / (eigenvalues ** 2).sum()


def compute_between_set_metrics(X_collective: np.ndarray,
                                X_exploitative: np.ndarray) -> tuple[float, float]:
    """
    Compute between-set metrics.

    Returns:
        (centroid_distance, cohens_d)
    """
    if len(X_collective) == 0 or len(X_exploitative) == 0:
        return np.nan, np.nan

    centroid_c = X_collective.mean(axis=0)
    centroid_e = X_exploitative.mean(axis=0)
    centroid_distance = np.linalg.norm(centroid_c - centroid_e)

    # Cohen's d: centroid distance / pooled within-set std
    # Pooled std: sqrt of average variance across both sets
    var_c = np.var(X_collective, axis=0).mean() if len(X_collective) > 1 else 0
    var_e = np.var(X_exploitative, axis=0).mean() if len(X_exploitative) > 1 else 0

    n_c, n_e = len(X_collective), len(X_exploitative)
    pooled_var = ((n_c - 1) * var_c + (n_e - 1) * var_e) / (n_c + n_e - 2) if (n_c + n_e) > 2 else 1
    pooled_std = np.sqrt(pooled_var * X_collective.shape[1])  # scale by sqrt(dimensions)

    cohens_d = centroid_distance / pooled_std if pooled_std > 0 else np.nan

    return centroid_distance, cohens_d


def compute_game_variance_explained(X: np.ndarray, game_labels: np.ndarray) -> float:
    """
    Compute proportion of variance explained by game membership.

    Multivariate η² = trace(S_between) / trace(S_total)
    """
    games = np.unique(game_labels)
    global_centroid = X.mean(axis=0)

    # Total sum of squares
    ss_total = np.sum((X - global_centroid) ** 2)

    # Between-group sum of squares
    ss_between = 0.0
    for game in games:
        mask = game_labels == game
        n_game = mask.sum()
        game_centroid = X[mask].mean(axis=0)
        ss_between += n_game * np.sum((game_centroid - global_centroid) ** 2)

    return ss_between / ss_total if ss_total > 0 else 0.0


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
                    ha=ha, xytext=(offset, 0), textcoords='offset points')


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
                                        alpha=0.15,
                                        edgecolor=colors[i],
                                        linewidth=1.5)
        handles.append((scatter, str(gene)))

    plot_baselines(ax, baseline_pca, baseline_labels)

    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
    ax.set_title(title)
    ax.legend([h[0] for h in handles], [h[1] for h in handles], loc='upper center', frameon=False,
               bbox_to_anchor=(0.4, 1.05), ncol=2)


def plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca, baseline_labels, games, pca, output_dir):
    """
    Create a 2×3 grid: rows=attitudes, columns=games.
    Each subplot shows all models for that game/attitude combination.
    """
    attitudes = [Attitude.COLLECTIVE, Attitude.EXPLOITATIVE]
    attitude_names = {Attitude.COLLECTIVE: "Collective", Attitude.EXPLOITATIVE: "Exploitative"}

    # Extract unique models across all genes
    all_genes = []
    for g in games:
        all_genes.extend(pca_data[g]['genes'])
    models = sorted(set(gene.model for gene in all_genes))
    model_colors = dict(zip(models, plt.colormaps.get_cmap('tab10')(np.linspace(0, 1, len(models)))))

    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE,
                             sharex=True, sharey=True)

    for col, game in enumerate(games):
        game_mask = game_labels == game
        genes_for_game = pca_data[game]['genes']

        for row, attitude in enumerate(attitudes):
            ax = axes[row, col]

            # Filter genes for this attitude
            genes_this_attitude = [g for g in genes_for_game if g.attitude == attitude]
            handles = []

            for model in models:
                # Find the gene for this model+attitude (if exists)
                matching_genes = [g for g in genes_this_attitude if g.model == model]
                if not matching_genes:
                    continue
                gene = matching_genes[0]

                mask = game_mask & (labels_all == str(gene))
                points = X_pca_combined[mask, :2]

                if len(points) == 0:
                    continue

                color = model_colors[model]
                scatter = ax.scatter(points[:, 0], points[:, 1],
                                     alpha=0.3, s=10, color=color)

                # Centroid
                mean_pt = points.mean(axis=0)
                ax.scatter(mean_pt[0], mean_pt[1], marker='o', s=100,
                           color=color, edgecolors='black', linewidths=1.5, zorder=5)

                # Ellipse
                if len(points) > 2:
                    cov = np.cov(points.T)
                    plot_covariance_ellipse(ax, mean_pt, cov, n_std=1.0,
                                            facecolor=color, alpha=0.15,
                                            edgecolor=color, linewidth=1.5)

                handles.append((scatter, model))

            # Baselines (smaller markers for grid)
            plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)

            # Labels
            if row == 0:
                ax.set_title(game)
            if col == 0:
                ax.set_ylabel(f"{attitude_names[attitude]}\nPC2 ({pca.explained_variance_ratio_[1]:.1%})")
            if row == 1:
                ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')

    # Shared legend for models (outside the grid on the right)
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=model_colors[m], markersize=10,
                                  label=m) for m in models]
    fig.legend(handles=legend_handles, loc='upper center', frameon=False,
               bbox_to_anchor=(0.4, 1.05), ncol=len(registry.available_models))

    plt.tight_layout(rect=[0, 0, 0.95, 1])  # Leave space for legend
    plt.savefig(output_dir / f"pca_by_game.{FORMAT}", format=FORMAT, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved combined PCA grid to {output_dir / f'pca_by_game.{FORMAT}'}")


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

    models_map = {"gpt-5-mini": "GPT 5 Mini",
                  "gemini-2.5-flash": "Gemini 2.5 Flash",
                  "claude-haiku-4-5": "Claude Haiku 4.5",
                  "llama3.1-70b": "Llama 3.1 70b",
                  "mistral-7b": "Mistral 7b",
                  "deepseek-r1-distill-llama-70b": "DeepSeek R1"}

    # Grid layout based on number of models
    n_models = len(models)
    n_cols = 3
    n_rows = (n_models + n_cols - 1) // n_cols

    # Color by game, marker style by attitude
    game_colors = dict(zip(games, plt.colormaps.get_cmap('Set1')(np.linspace(0, 1, len(games)))))
    attitude_markers = {Attitude.COLLECTIVE: 'o', Attitude.EXPLOITATIVE: 's'}

    fig, axes = plt.subplots(n_rows, n_cols, figsize=FIGSIZE,
                             sharex=True, sharey=True)
    axes = np.atleast_2d(axes)

    for idx, model in enumerate(models):
        row, col = divmod(idx, n_cols)
        ax = axes[row, col]

        for game in games:
            game_mask = game_labels == game
            genes_for_game = pca_data[game]['genes']
            color = game_colors[game]

            for attitude in [Attitude.COLLECTIVE, Attitude.EXPLOITATIVE]:
                matching_genes = [g for g in genes_for_game
                                  if g.model == model and g.attitude == attitude]
                if not matching_genes:
                    continue
                gene = matching_genes[0]

                mask = game_mask & (labels_all == str(gene))
                points = X_pca_combined[mask, :2]

                if len(points) == 0:
                    continue

                marker = attitude_markers[attitude]
                ax.scatter(points[:, 0], points[:, 1],
                           alpha=0.3, s=10, color=color, marker=marker)

                # Centroid
                mean_pt = points.mean(axis=0)
                ax.scatter(mean_pt[0], mean_pt[1], marker=marker, s=100,
                           color=color, edgecolors='black', linewidths=1.5, zorder=5)

                # Ellipse
                if len(points) > 2:
                    cov = np.cov(points.T)
                    plot_covariance_ellipse(ax, mean_pt, cov, n_std=1.0,
                                            facecolor=color, alpha=0.15,
                                            edgecolor=color, linewidth=1.5)

        plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)
        ax.set_title(models_map[model])

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
    game_mapping = {'public_goods': ' Public Goods Game', 'collective_risk': 'Collective Risk Dilemma', 'common_pool': 'Common Pool Resource', 'public_goods_prompt': 'Public Goods'}
    for game in games:
        legend_handles.append(plt.Line2D([0], [0], marker='o', color='w',
                                         markerfacecolor=game_colors[game],
                                         markersize=10, label=game_mapping[game]))
    legend_handles.append(plt.Line2D([0], [0], marker='o', color='gray',
                                     markersize=8, label='Collective'))
    legend_handles.append(plt.Line2D([0], [0], marker='s', color='gray',
                                     markersize=8, label='Exploitative'))

    fig.legend(handles=legend_handles, loc='upper center', frameon=False,
               bbox_to_anchor=(0.5, 1.02), ncol=len(games) + 2,
               columnspacing=0.6, handletextpad=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_dir / f"pca_by_model.{FORMAT}", format=FORMAT, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved per-model PCA grid to {output_dir / f'pca_by_model.{FORMAT}'}")


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
            # Each element in context is a tuple representing one round's opponent actions
            context_str = '|'.join(''.join('C' if val else 'D'
                                            for val in round_actions)
                                    for round_actions in context)
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

    # Globals shared across all games
    all_actions = tuple(product([D, C], repeat=args.n_rounds - 1))
    unique_combos: tuple[OpponentActions, ...] = tuple(
        combinations_with_replacement(all_actions, args.n_players - 1))

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
            n_strategies = len(all_specs) if args.n_strategies is None else min(len(all_specs), args.n_strategies)
            chunks = chunk_indices(n_strategies, args.n_processes)

            logger.info(f"Computing {n_strategies} strategies for {gene} in {len(chunks)} chunks")

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

    logger.info(f"Features:\n{len(unique_combos)} unique opponent action combinations of length {args.n_rounds - 1}\nGiving rise to {n_features} features in total (including histories of shorter length)."
    )


    # ==========================================================================
    # PHASE 3: Combined PCA (all games together, plotted separately)
    # ==========================================================================
    logger.info(f"\n{'='*60}")
    logger.info("COMBINED PCA ANALYSIS")
    logger.info(f"{'='*60}")

    # Stack all games
    X_all = np.vstack([pca_data[g]['X'] for g in args.games])
    labels_all = np.concatenate([pca_data[g]['labels'] for g in args.games])
    game_labels = np.concatenate([[g] * len(pca_data[g]['X']) for g in args.games])

    # Fit combined PCA
    n_components = min(10, X_all.shape[1], X_all.shape[0])
    pca_combined = PCA(n_components=n_components)
    X_pca_combined = pca_combined.fit_transform(X_all)
    baseline_pca_combined = pca_combined.transform(baseline_X)

    # Random baseline for normalization
    random_baseline_dist = compute_random_baseline_distance(X_all.shape[1])

    # Scree plot (combined)
    cumulative = np.cumsum(pca_combined.explained_variance_ratio_)
    plt.figure()
    plt.plot(range(1, len(cumulative) + 1), cumulative, 'o-')
    plt.axhline(y=0.9, color='r', linestyle='--', label='90% threshold')
    plt.xlabel('Component')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Combined PCA Scree Plot')
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
            extrema_analysis(extrema_info.get('bottom_right', list(extrema_info.values())[0]))
            plot_extrema(extrema_info, ax)

        plt.tight_layout()
        plt.savefig(output_dir / f"pca_{game_name}.{FORMAT}", format=FORMAT, bbox_inches='tight')
        plt.close()

    # Combined 2x3 grid plot (attitudes × games)
    plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca_combined, baseline_labels, args.games,
                     pca_combined, output_dir)

    plot_pca_by_model(pca_data, X_pca_combined, labels_all, game_labels,
                      baseline_pca_combined, baseline_labels, args.games,
                      pca_combined, output_dir)

    # ==========================================================================
    # PHASE 4: Compute and display metrics
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
            mpd, mpd_norm = compute_within_set_metrics(X_gene, random_baseline_dist)
            pr = compute_participation_ratio(X_gene)
            logger.info(f"    {gene}: MPD={mpd:.3f} (norm={mpd_norm:.2f}), PR={pr:.2f}")

    logger.info(f"\n{'='*60}")
    logger.info("VARIANCE EXPLAINED BY GAME MEMBERSHIP")
    logger.info(f"{'='*60}")

    # Per model (do strategies from the same model behave similarly across games?)
    models = sorted(set(g.model for g in pca_data[args.games[0]]['genes']))
    for model in models:
        model_mask = np.array([model in label for label in labels_all])
        eta_sq_model = compute_game_variance_explained(X_all[model_mask], game_labels[model_mask])
        logger.info(f"  {model}: η² = {eta_sq_model:.3f}")

    logger.info(f"\n{'='*60}")
    logger.info("BETWEEN-SET METRICS (Collective vs Exploitative)")
    logger.info(f"{'='*60}")

    for game_name in args.games:
        logger.info(f"\n  {game_name}:")
        genes = pca_data[game_name]['genes']

        # Group genes by model
        models = set(gene.model for gene in genes)

        for model in sorted(models):
            # Get genes for this model, split by attitude
            collective_genes = [g for g in genes if g.model == model and g.attitude == Attitude.COLLECTIVE]
            exploitative_genes = [g for g in genes if g.model == model and g.attitude == Attitude.EXPLOITATIVE]

            if not collective_genes or not exploitative_genes:
                continue

            # Get corresponding feature vectors
            mask = game_labels == game_name
            X_collective = X_all[mask & np.isin(labels_all, [str(g) for g in collective_genes])]
            X_exploitative = X_all[mask & np.isin(labels_all, [str(g) for g in exploitative_genes])]

            if len(X_collective) == 0 or len(X_exploitative) == 0:
                continue

            centroid_dist, cohens_d = compute_between_set_metrics(X_collective, X_exploitative)
            metrics = BetweenSetMetrics(
                game=game_name,
                model=model,
                centroid_distance=centroid_dist,
                cohens_d=cohens_d
            )
            logger.info(f"    {metrics}")
