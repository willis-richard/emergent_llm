# pylint: disable=redefined-outer-name,missing-function-docstring,missing-class-docstring,possibly-used-before-assignment

import argparse
import logging
import pickle
from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
from emergent_llm.tournament import pretty_model

FIGSIZE, FORMAT, FONTSIZE = setup('1_col_slide')

GAME_MAPPING = {
    'public_goods': 'Public Goods Game',
    'collective_risk': 'Collective Risk Dilemma',
    'common_pool': 'Common Pool Resource',
}

GAME_SHORT = {
    'public_goods': 'PGG',
    'collective_risk': 'CRD',
    'common_pool': 'CPR',
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
                        default=7,
                        help="Number of rounds per game")
    parser.add_argument("--n_games",
                        type=int,
                        default=30,
                        help="Number of games for each trajectory")

    # Execution parameters
    parser.add_argument("--log_level",
                        type=str,
                        default="INFO",
                        help="Logging level to use")
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
    parser.add_argument("--plot_baselines",
                        action='store_true',
                        help="Label the baseline strategies")
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


def compute_features(player: BasePlayer, n_games: int) -> dict[CooperatorCounts, float]:
    sums: dict[CooperatorCounts, float] = {}
    counts: dict[CooperatorCounts, int] = {}
    for combo, opponents in zip(unique_combos, fixed_opponents):
        players = [player] + opponents
        game = game_class(players, description)
        histories = [game.play_game().history for _ in range(n_games)]
        player_actions = np.array([h.actions[:, 0] for h in histories])
        for r in range(args.n_rounds):
            key = combo[:r]
            sums[key] = sums.get(key, 0.0) + float(player_actions[:, r].mean())
            counts[key] = counts.get(key, 0) + 1
    return {k: sums[k] / counts[k] for k in sums}


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
        # for i in range(1, args.n_players)
        for i in range(2, 3)
    ]
    baseline_players += [
        SimplePlayer(f"CD({i})", ConditionalDefector(D, i))
        # for i in range(1, args.n_players)
        for i in range(2, 3)
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
# AGGREGATION HELPERS
# =============================================================================


def aggregate_by_base_family(
    X_all: np.ndarray,
    labels_all: np.ndarray,
    game_labels: np.ndarray,
    pca_data: dict,
    game: str,
    model: str,
    base_attitude: Attitude,
    exclude_synonym: Attitude | None = None,
) -> np.ndarray:
    """
    Get feature vectors for all synonyms mapping to base_attitude in (game, model).

    If exclude_synonym is given, omit that synonym (used for leave-one-out).
    """
    genes = pca_data[game]['genes']
    matching = [
        g for g in genes
        if g.model == model
        and g.attitude.to_base_attitude() == base_attitude
        and (exclude_synonym is None or g.attitude != exclude_synonym)
    ]
    if not matching:
        return np.empty((0, X_all.shape[1]))
    gene_strs = [str(g) for g in matching]
    mask = (game_labels == game) & np.isin(labels_all, gene_strs)
    return X_all[mask]


def get_feature_vectors_for_synonym(
    X_all: np.ndarray,
    labels_all: np.ndarray,
    game_labels: np.ndarray,
    pca_data: dict,
    game: str,
    model: str,
    attitude: Attitude,
) -> np.ndarray:
    """Feature vectors for one specific (game, model, attitude) gene."""
    genes = pca_data[game]['genes']
    matching = [g for g in genes if g.model == model and g.attitude == attitude]
    if not matching:
        return np.empty((0, X_all.shape[1]))
    gene_strs = [str(g) for g in matching]
    mask = (game_labels == game) & np.isin(labels_all, gene_strs)
    return X_all[mask]


# =============================================================================
# METRICS
# =============================================================================


def compute_random_baseline_distance(n_features: int,
                                     n_samples: int = 500) -> float:
    rng = np.random.default_rng(0)
    random_X = rng.uniform(0, 1, (n_samples, n_features))
    return float(np.mean(pdist(random_X, metric='euclidean')))


def compute_within_set_metrics(X: np.ndarray,
                               random_baseline: float) -> tuple[float, float]:
    """Returns (mean_pairwise_distance, normalised_distance)."""
    if len(X) < 2:
        return 0.0, 0.0
    distances = pdist(X, metric='euclidean')
    mpd = float(np.mean(distances))
    return mpd, mpd / random_baseline


def compute_participation_ratio(X: np.ndarray) -> float:
    """PR = (sum of eigenvalues)^2 / sum of eigenvalues^2."""
    if len(X) < 2:
        return 1.0
    X_centered = X - X.mean(axis=0)
    cov = np.cov(X_centered.T)
    eigenvalues = np.linalg.eigvalsh(cov)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    if len(eigenvalues) == 0:
        return 1.0
    return (eigenvalues.sum()**2) / (eigenvalues**2).sum()


def compute_delta(X_a: np.ndarray, X_b: np.ndarray) -> float:
    """
    Standardised centroid distance:
        Delta = ||centroid_a - centroid_b|| / pooled_within_set_std

    Pooled std: sqrt(pooled_var * n_features), so Delta = 1 means the centroid
    gap equals one typical strategy-distance under the within-set covariance.
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


def compute_game_variance_explained(X: np.ndarray,
                                    game_labels: np.ndarray) -> float:
    """Multivariate η² = trace(S_between) / trace(S_total)."""
    games = np.unique(game_labels)
    global_centroid = X.mean(axis=0)
    ss_total = np.sum((X - global_centroid)**2)
    ss_between = 0.0
    for game in games:
        mask = game_labels == game
        n_game = mask.sum()
        game_centroid = X[mask].mean(axis=0)
        ss_between += n_game * np.sum((game_centroid - global_centroid)**2)
    return ss_between / ss_total if ss_total > 0 else 0.0


# =============================================================================
# DATAFRAME BUILDERS
# =============================================================================


def build_main_dataframe(
    X_all: np.ndarray,
    labels_all: np.ndarray,
    game_labels: np.ndarray,
    pca_data: dict,
    games: list[str],
    random_baseline_dist: float,
) -> pd.DataFrame:
    """
    Main metrics table: aggregated by base attitude family.

    Columns: (game, metric) where metric in {coop, mpd_norm, delta, pr}.
    Rows: (model, attitude_family).
    Delta is per (model, game) and repeated across both attitude rows.
    """
    rows = []
    for game in games:
        genes = pca_data[game]['genes']
        models = sorted(set(g.model for g in genes))
        for model in models:
            X_by_attitude = {}
            for base_att in Attitude.base_attitudes():
                X_by_attitude[base_att] = aggregate_by_base_family(
                    X_all, labels_all, game_labels, pca_data,
                    game, model, base_att,
                )

            # Between-set Delta (shared across both attitude rows for this model+game)
            X_c = X_by_attitude[Attitude.COLLECTIVE]
            X_s = X_by_attitude[Attitude.SELFISH]
            delta = compute_delta(X_c, X_s) if len(X_c) > 0 and len(X_s) > 0 else np.nan

            for base_att in Attitude.base_attitudes():
                X_set = X_by_attitude[base_att]
                if len(X_set) == 0:
                    continue
                coop = float(X_set.mean())
                # SE of the family mean coop rate, treating each strategy as
                # one observation (its mean over the feature vector). This
                # collapses within-strategy correlation between features and
                # also absorbs Monte Carlo noise from the n_games-sample
                # estimates, since both end up in the per-strategy mean.
                strategy_means = X_set.mean(axis=1)
                coop_se = (float(strategy_means.std(ddof=1) / np.sqrt(len(strategy_means)))
                           if len(strategy_means) > 1 else np.nan)
                _, mpd_norm = compute_within_set_metrics(X_set, random_baseline_dist)
                pr = compute_participation_ratio(X_set)
                rows.append({
                    'game': game,
                    'model': model,
                    'attitude': base_att.value,
                    'coop': coop,
                    'coop_se': coop_se,
                    'mpd_norm': mpd_norm,
                    'delta': delta,
                    'pr': pr,
                })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # Pivot: index = (model, attitude), columns = (game, metric)
    df_pivot = df.pivot_table(
        index=['model', 'attitude'],
        columns='game',
        values=['coop', 'coop_se', 'mpd_norm', 'delta', 'pr'],
        aggfunc='first',
    )
    # Reorder columns: (game, metric) instead of (metric, game)
    df_pivot = df_pivot.swaplevel(axis=1)
    # Reorder games and metrics
    metric_order = ['coop', 'coop_se', 'mpd_norm', 'delta', 'pr']
    game_order = [g for g in games if g in df_pivot.columns.get_level_values(0).unique()]
    new_cols = [(g, m) for g in game_order for m in metric_order
                if (g, m) in df_pivot.columns]
    df_pivot = df_pivot[new_cols]

    # Reorder index: attitude in Attitude.base_attitudes() order
    df_pivot = df_pivot.reindex(
        sorted(df_pivot.index,
               key=lambda x: (x[0], 0 if x[1] == Attitude.COLLECTIVE.value else 1))
    )
    return df_pivot


def build_appendix_dataframe(
    X_all: np.ndarray,
    labels_all: np.ndarray,
    game_labels: np.ndarray,
    pca_data: dict,
    games: list[str],
) -> pd.DataFrame:
    """
    Appendix table: each synonym vs its own family (LOO) and the other family.

    For synonym X with base family F_X:
        own_family   = F_X excluding X (leave-one-out, avoids self-inclusion bias)
        other_family = full F_~X
        d_own   = Delta(X, own_family)
        d_other = Delta(X, other_family)
        ratio   = d_own / d_other  (< 1 means X clusters with its semantic family)
    """
    rows = []
    for game in games:
        genes = pca_data[game]['genes']
        models_in_game = sorted(set(g.model for g in genes))
        for model in models_in_game:
            for synonym in Attitude:
                X_syn = get_feature_vectors_for_synonym(
                    X_all, labels_all, game_labels, pca_data,
                    game, model, synonym,
                )
                if len(X_syn) < 2:
                    continue

                own_base = synonym.to_base_attitude()
                other_base = (Attitude.SELFISH if own_base == Attitude.COLLECTIVE
                              else Attitude.COLLECTIVE)

                X_own = aggregate_by_base_family(
                    X_all, labels_all, game_labels, pca_data,
                    game, model, own_base, exclude_synonym=synonym,
                )
                X_other = aggregate_by_base_family(
                    X_all, labels_all, game_labels, pca_data,
                    game, model, other_base,
                )

                d_own = compute_delta(X_syn, X_own)
                d_other = compute_delta(X_syn, X_other)
                ratio = d_own / d_other if d_other > 0 else np.nan

                rows.append({
                    'game': game,
                    'model': model,
                    'synonym': synonym.value,
                    'base_family': own_base.value,
                    'd_own': d_own,
                    'd_other': d_other,
                    'ratio': ratio,
                })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df_pivot = df.pivot_table(
        index=['base_family', 'synonym', 'model'],
        columns='game',
        values=['d_own', 'd_other', 'ratio'],
        aggfunc='first',
    )
    df_pivot = df_pivot.swaplevel(axis=1)
    metric_order = ['d_own', 'd_other', 'ratio']
    game_order = [g for g in games if g in df_pivot.columns.get_level_values(0).unique()]
    new_cols = [(g, m) for g in game_order for m in metric_order
                if (g, m) in df_pivot.columns]
    df_pivot = df_pivot[new_cols]
    return df_pivot

def build_per_round_cooperation_df(pca_data: dict, games: list[str],
                                   n_rounds: int) -> pd.DataFrame:
    """
    Per-round cooperation rate for each (game, model, attitude) gene.

    The value for round r is the mean cooperation probability over all
    strategies of that gene and over all opponent-history prefixes of
    length r. NOTE: prefixes are weighted uniformly, not by their
    likelihood under any opponent distribution — consistent with how
    `coop` is computed in the main table, but it is *not* an empirical
    in-play cooperation rate.
    """
    rows = []
    for game in games:
        for gene, _strategy_name, feature_dict in pca_data[game]['metadata']:
            sums = np.zeros(n_rounds)
            counts = np.zeros(n_rounds, dtype=int)
            for key, value in feature_dict.items():
                r = len(key)
                sums[r] += value
                counts[r] += 1
            rows.append({
                'game': game,
                'model': gene.model,
                'attitude': gene.attitude.value,
                **{f'round_{r}': sums[r] / counts[r] for r in range(n_rounds)},
            })

    df = pd.DataFrame(rows)
    round_cols = [f'round_{r}' for r in range(n_rounds)]
    # Mean over strategies; every strategy contributes the same number of
    # prefixes per round, so this equals the flat mean over (strategy, prefix).
    return df.groupby(['game', 'model', 'attitude'])[round_cols].mean()


def plot_per_round_cooperation(df_rounds: pd.DataFrame, games: list[str],
                               n_rounds: int, output_dir: Path):
    """One subplot per game; colour = model, linestyle = base attitude.

    Synonym genes are collapsed to their base family by averaging the
    gene-level curves. This weights each gene equally, which equals
    per-strategy weighting as long as every gene has the same number of
    strategies (true by construction of the generation pipeline).
    """
    round_cols = [f'round_{r}' for r in range(n_rounds)]
    rounds = range(n_rounds)

    # Collapse synonyms to base attitude
    df = df_rounds.reset_index()
    df['base_attitude'] = df['attitude'].map(
        lambda a: Attitude(a).to_base_attitude().value)
    df_base = df.groupby(['game', 'model', 'base_attitude'])[round_cols].mean()

    models = sorted(df['model'].unique())
    cmap = plt.colormaps.get_cmap('tab10')
    model_colors = {m: cmap(i) for i, m in enumerate(models)}
    linestyles = {Attitude.COLLECTIVE: '-', Attitude.SELFISH: '--'}

    fig, axes = plt.subplots(1, len(games), figsize=FIGSIZE,
                             sharex=True, sharey=True)
    axes = np.atleast_1d(axes)

    for ax, game in zip(axes, games):
        sub = df_base.loc[game]
        for (model, base_value), row in sub.iterrows():
            base = Attitude(base_value)
            ax.plot(rounds, row[round_cols].to_numpy(dtype=float),
                    color=model_colors[model], linestyle=linestyles[base],
                    lw=1.25, marker='o', alpha=0.8)
        ax.set_title(GAME_MAPPING.get(game, game))
        ax.set_ylim(0, 1)
        ax.set_xticks(list(rounds))

    fig.supxlabel('Round', y=0.02)
    fig.supylabel('Cooperation rate', x=0.03)

    # Single two-row legend: row 1 = models, row 2 = attitudes.
    # Matplotlib fills legends column-major (down, then across), so with
    # ncol = n_models we interleave (model_i, attitude_or_blank_i) pairs.
    model_handles = [plt.Line2D([0], [0], color=model_colors[m], lw=2,
                                label=pretty_model(m)) for m in models]
    attitude_handles = [plt.Line2D([0], [0], color='gray', lw=2, linestyle=ls,
                                   label=att.value.capitalize())
                        for att, ls in linestyles.items()]
    blank = lambda: plt.Line2D([0], [0], color='none', label=' ')

    n_cols = max(len(model_handles), len(attitude_handles))
    model_handles += [blank() for _ in range(n_cols - len(model_handles))]
    attitude_handles += [blank() for _ in range(n_cols - len(attitude_handles))]

    interleaved = [h for pair in zip(model_handles, attitude_handles)
                   for h in pair]

    fig.legend(handles=interleaved, loc='upper center', frameon=False,
               bbox_to_anchor=(0.5, 1.22), ncol=n_cols)

    plt.tight_layout()
    plt.savefig(output_dir / f"per_round_cooperation.{FORMAT}",
                format=FORMAT, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved per_round_cooperation.{FORMAT}")


# =============================================================================
# LATEX WRITERS
# =============================================================================


def _fmt(x, precision=1):
    if pd.isna(x):
        return '--'
    return f"{x:.{precision}f}"

def _fmt_pm(val, se, _precision=None):
    """Compact uncertainty notation in percent: '68(1)\\%' = 0.68 ± 0.01."""
    if pd.isna(val):
        return '--'
    pct = round(val * 100)
    if pd.isna(se):
        return f"{pct}\\%"
    return f"{pct}({round(se * 100)})\\%"

def write_main_latex(df_pivot: pd.DataFrame, output_path: Path):
    """
    Main metrics table with multirow for Model and Δ.

    Layout: per game we show Coop, MPD, Δ, PR; Δ spans both attitude rows.
    """
    if df_pivot.empty:
        logger.warning("Main DataFrame empty; skipping LaTeX write.")
        return

    games = sorted(set(df_pivot.columns.get_level_values(0)))
    games = [g for g in ['public_goods', 'collective_risk', 'common_pool'] if g in games]
    n_games = len(games)
    cols_per_game = 4  # Coop, MPD, Δ, PR

    # column spec
    inner = '|'.join(['cccc'] * n_games)
    col_spec = 'll|' + inner

    # Group rows by model
    models = list(dict.fromkeys(df_pivot.index.get_level_values(0)))

    lines = []
    lines.append('% Auto-generated; copy into paper.')
    lines.append('\\begin{table*}[t]')
    lines.append('\\caption{Strategic variation in the generated algorithms.}')
    lines.append('\\centering')
    lines.append('\\setlength{\\tabcolsep}{2pt}')
    lines.append(f'\\begin{{tabular}}{{{col_spec}}}')
    lines.append('\\hline')

    # Header row 1: game group names
    header_groups = ['', '']  # Model, Attitude
    for i, g in enumerate(games):
        sep = '|' if i < n_games - 1 else ''
        header_groups.append(f'\\multicolumn{{{cols_per_game}}}{{c{sep}}}{{{GAME_MAPPING[g]}}}')
    lines.append('Model & Attitude & ' + ' & '.join(header_groups[2:]) + ' \\\\')

    # Header row 2: metric names
    metric_headers = ['', '']
    for _ in games:
        metric_headers += ['Coop', 'MPD', '$\\Delta$', 'PR']
    lines.append(' & '.join(metric_headers) + ' \\\\')
    lines.append('\\hline')

    # Body
    for model in models:
        sub = df_pivot.loc[model]
        attitudes = list(sub.index)
        n_att = len(attitudes)

        for row_idx, attitude in enumerate(attitudes):
            cells = []
            # Model column (multirow on first row)
            if row_idx == 0:
                cells.append(f'\\multirow{{{n_att}}}{{*}}{{{pretty_model(model)}}}')
            else:
                cells.append('')
            # Attitude column
            cells.append(attitude.capitalize())
            # Per-game metrics
            for g in games:
                coop = sub.loc[attitude, (g, 'coop')] if (g, 'coop') in sub.columns else np.nan
                coop_se = sub.loc[attitude, (g, 'coop_se')] if (g, 'coop_se') in sub.columns else np.nan
                mpd = sub.loc[attitude, (g, 'mpd_norm')] if (g, 'mpd_norm') in sub.columns else np.nan
                delta = sub.loc[attitude, (g, 'delta')] if (g, 'delta') in sub.columns else np.nan
                pr = sub.loc[attitude, (g, 'pr')] if (g, 'pr') in sub.columns else np.nan

                cells.append(_fmt_pm(coop, coop_se, 2))
                cells.append(_fmt(mpd, 1))
                # Delta: multirow on first row, blank otherwise
                if row_idx == 0:
                    cells.append(f'\\multirow{{{n_att}}}{{*}}{{{_fmt(delta, 1)}}}')
                else:
                    cells.append('')
                cells.append(_fmt(pr, 1))
            lines.append(' & '.join(cells) + ' \\\\')
        lines.append('\\hline')

    lines.append('\\end{tabular}')
    lines.append('\\label{tab:pca}')
    lines.append('\\end{table*}')

    output_path.write_text('\n'.join(lines) + '\n')
    logger.info(f"Wrote main LaTeX table to {output_path}")


def write_appendix_latex(df_pivot: pd.DataFrame, output_path: Path):
    """Synonym comparison table for the appendix."""
    if df_pivot.empty:
        logger.warning("Appendix DataFrame empty; skipping LaTeX write.")
        return

    games = sorted(set(df_pivot.columns.get_level_values(0)))
    games = [g for g in ['public_goods', 'collective_risk', 'common_pool'] if g in games]
    n_games = len(games)
    cols_per_game = 3

    inner = '|'.join(['ccc'] * n_games)
    col_spec = 'lll|' + inner

    lines = []
    lines.append('% Auto-generated synonym comparison table.')
    lines.append('\\begin{table*}[t]')
    lines.append('\\caption{Synonym placement relative to base-attitude families. '
                 '$d_{\\text{own}}$ uses leave-one-out (synonym excluded from own family centroid).}')
    lines.append('\\centering')
    lines.append('\\setlength{\\tabcolsep}{3pt}')
    lines.append(f'\\begin{{tabular}}{{{col_spec}}}')
    lines.append('\\hline')

    header_groups = ['', '', '']
    for i, g in enumerate(games):
        sep = '|' if i < n_games - 1 else ''
        header_groups.append(f'\\multicolumn{{{cols_per_game}}}{{c{sep}}}{{{GAME_SHORT[g]}}}')
    lines.append('Attitude & Synonym & Model & ' + ' & '.join(header_groups[3:]) + ' \\\\')

    metric_headers = ['', '', '']
    for _ in games:
        metric_headers += ['$d_{\\text{own}}$', '$d_{\\text{other}}$', 'ratio']
    lines.append(' & '.join(metric_headers) + ' \\\\')
    lines.append('\\hline')

    # Group by (family, synonym)
    last_family = None
    last_synonym = None
    for (family, synonym, model), row in df_pivot.iterrows():
        cells = []
        # Family with horizontal rule on change
        if family != last_family:
            if last_family is not None:
                lines.append('\\hline')
            last_family = family
            last_synonym = None
            cells.append(family.capitalize())
        else:
            cells.append('')

        if synonym != last_synonym:
            last_synonym = synonym
            cells.append(synonym)
        else:
            cells.append('')

        cells.append(pretty_model(model))

        for g in games:
            d_own = row.get((g, 'd_own'), np.nan)
            d_other = row.get((g, 'd_other'), np.nan)
            ratio = row.get((g, 'ratio'), np.nan)
            cells.append(_fmt(d_own, 2))
            cells.append(_fmt(d_other, 2))
            cells.append(_fmt(ratio, 2))
        lines.append(' & '.join(cells) + ' \\\\')

    lines.append('\\hline')
    lines.append('\\end{tabular}')
    lines.append('\\label{tab:synonyms}')
    lines.append('\\end{table*}')

    output_path.write_text('\n'.join(lines) + '\n')
    logger.info(f"Wrote appendix LaTeX table to {output_path}")


# =============================================================================
# PCA HELPERS
# =============================================================================


def fit_pca_on_all(X_all: np.ndarray) -> tuple[PCA, np.ndarray]:
    """Fit PCA on all data; return fitted PCA and transformed data."""
    n_components = min(10, X_all.shape[1], X_all.shape[0])
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_all)
    logger.info(
        f"Fitted PCA on {len(X_all)} strategies (all attitudes). "
        f"First 5 components explain: {pca.explained_variance_ratio_[:5]}"
    )
    return pca, X_pca


# =============================================================================
# PLOTTING HELPERS
# =============================================================================

BASELINE_LABELS_LEFT = {"A-D", "CD(1)", "CC(3)"}
BASELINE_LABELS_RIGHT = {"CD(2)", "CC(2)"}


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
        # ha = 'right' if name in BASELINE_LABELS_LEFT else 'left'
        # offset = -5 if name in BASELINE_LABELS_LEFT else 5
        ha = 'right' if name in BASELINE_LABELS_RIGHT else 'center'
        x_offset = -5 if name in BASELINE_LABELS_RIGHT else 0
        y_offset = -7 if name in BASELINE_LABELS_RIGHT else 7
        ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]),
                    ha=ha,
                    xytext=(x_offset, y_offset),
                    textcoords='offset points')


def _legend_top_reservation(n_handles: int, ncol: int) -> float:
    """Return the `top` value for tight_layout rect to leave room for legend above."""
    n_rows = max(1, (n_handles + ncol - 1) // ncol)
    return max(0.80, 1.0 - 0.05 * n_rows - 0.03)


def _aggregate_points_for_family(
    X_pca_combined, labels_all, game_mask, genes_for_game, model, base_attitude
):
    """Get PCA-projected points for (model, base_attitude family) within one game."""
    matching = [
        g for g in genes_for_game
        if g.model == model and g.attitude.to_base_attitude() == base_attitude
    ]
    if not matching:
        return np.empty((0, 2))
    gene_strs = [str(g) for g in matching]
    mask = game_mask & np.isin(labels_all, gene_strs)
    return X_pca_combined[mask, :2]

def plot_pca_single_game(
    axes, X_pca_combined, labels_all, game_mask, genes_for_game,
    baseline_pca, baseline_labels, pca,
):
    """Single-game PCA plot: 1 row × 2 cols (Collective | Selfish).

    Mirrors the aggregation in plot_pca_by_game. Returns legend handles
    for the caller to place a figure-level legend.
    """
    models = sorted(set(g.model for g in genes_for_game))
    cmap = plt.colormaps.get_cmap('tab10')
    model_colors = {m: cmap(i) for i, m in enumerate(models)}

    handles = []
    seen_models = set()
    for col, base_att in enumerate(Attitude.base_attitudes()):
        ax = axes[col]
        for model in models:
            points = _aggregate_points_for_family(
                X_pca_combined, labels_all, game_mask,
                genes_for_game, model, base_att,
            )
            if len(points) == 0:
                continue

            color = model_colors[model]
            ax.scatter(points[:, 0], points[:, 1],
                       alpha=0.5, s=FONTSIZE*1.25, color=color)
            mean_pt = points.mean(axis=0)
            ax.scatter(mean_pt[0], mean_pt[1], alpha=0.7,
                       marker='o', s=FONTSIZE*12.5, color=color,
                       edgecolors='black', linewidths=1.5, zorder=5)

            if model not in seen_models:
                handles.append(plt.Line2D(
                    [0], [0], marker='o', color='w',
                    markerfacecolor=color, markersize=10,
                    label=pretty_model(model),
                ))
                seen_models.add(model)

        if args.plot_baselines:
            plot_baselines(ax, baseline_pca, baseline_labels)
        ax.set_title(base_att.capitalize())

    return handles


def plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca, baseline_labels, games, pca, output_dir):
    """2×3 grid: rows=base attitude family, columns=games. One ellipse per model.

    For each (model, base_attitude) cell, aggregates all synonyms in that
    base-attitude family (matches plot_pca_single_game / plot_pca_by_model).
    """
    all_genes = []
    for g in games:
        all_genes.extend(pca_data[g]['genes'])
    models = sorted(set(g.model for g in all_genes))
    cmap = plt.colormaps.get_cmap('tab10')
    model_colors = {m: cmap(i) for i, m in enumerate(models)}

    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE, sharex=True, sharey=True)

    for col, game in enumerate(games):
        game_mask = game_labels == game
        genes_for_game = pca_data[game]['genes']

        for row, base_att in enumerate(Attitude.base_attitudes()):
            ax = axes[row, col]

            for model in models:
                # Aggregate all synonyms whose base attitude == base_att
                points = _aggregate_points_for_family(
                    X_pca_combined, labels_all, game_mask,
                    genes_for_game, model, base_att,
                )
                if len(points) == 0:
                    continue

                color = model_colors[model]
                ax.scatter(points[:, 0], points[:, 1],
                           alpha=0.5, s=10, color=color)

                mean_pt = points.mean(axis=0)
                ax.scatter(mean_pt[0], mean_pt[1],
                           marker='o', s=70, color=color, alpha=0.7,
                           edgecolors='black', linewidths=1.5, zorder=5)

                # if len(points) > 2:
                #     cov = np.cov(points.T)
                #     plot_covariance_ellipse(
                #         ax, mean_pt, cov, n_std=1.0,
                #         facecolor=color, alpha=0.45,
                #         edgecolor=color, linewidth=1.5,
                #     )

            if args.plot_baselines:
                plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)

            if row == 0:
                ax.set_title(GAME_MAPPING[game])
            if col == 0:
                ax.set_ylabel(f"{base_att.capitalize()}")
            # if row == 1:
            #     ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    fig.supxlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', y=0.05)
    fig.supylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', x=0.03)

    # Pad shared axes once (sharex/sharey propagates)
    if args.plot_baselines:
        ax0 = axes[0, 0]
        xlim = ax0.get_xlim()
        ylim = ax0.get_ylim()
        x_pad_0 = 0.15 * (xlim[1] - xlim[0])
        x_pad_1 = 0.15 * (xlim[1] - xlim[0])
        y_pad = 0.02 * (ylim[1] - ylim[0])
        for ax in axes.flat:
            ax.set_xlim(xlim[0] - x_pad_0, xlim[1] + x_pad_1)
            ax.set_ylim(ylim[0] - y_pad, ylim[1] + y_pad)

    for ax in axes[0, :]:
        ax.tick_params(axis='x', which='both', bottom=False)
    for ax in axes[:, 1:].flat:
        ax.tick_params(axis='y', which='both', left=False)

    legend_handles = [
        plt.Line2D([0], [0], marker='o', color='w',
                   markerfacecolor=model_colors[m], markersize=10,
                   label=pretty_model(m))
        for m in models
    ]
    ncol = len(legend_handles) // 2 if len(legend_handles) > 4 else len(legend_handles)
    fig.legend(handles=legend_handles,
               loc='upper center', frameon=False,
               bbox_to_anchor=(0.5, 1.05) if len(legend_handles) <= 4 else (0.5, 1.1),
               ncol=ncol)

    plt.tight_layout(w_pad=0.07, h_pad=0.07)
    plt.savefig(output_dir / f"pca_by_game.{FORMAT}",
                format=FORMAT, bbox_inches='tight')
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

            for base_att in Attitude.base_attitudes():
                points = _aggregate_points_for_family(
                    X_pca_combined, labels_all, game_mask,
                    genes_for_game, model, base_att,
                )
                if len(points) == 0:
                    continue
                marker = attitude_markers[base_att]
                ax.scatter(points[:, 0], points[:, 1],
                           alpha=0.5, s=10, color=color, marker=marker)
                mean_pt = points.mean(axis=0)
                ax.scatter(mean_pt[0], mean_pt[1],
                           marker=marker, s=70, color=color, alpha=0.7,
                           edgecolors='black', linewidths=1.5, zorder=5)
                if len(points) > 2:
                    cov = np.cov(points.T)
                    plot_covariance_ellipse(
                        ax, mean_pt, cov, n_std=1.0,
                        facecolor=color, alpha=0.45,
                        edgecolor=color, linewidth=1.5,
                    )

        if args.plot_baselines:
            plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)
        ax.set_title(pretty_model(model))
        # if col == 0:
        #     ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        # if row == n_rows - 1:
        #     ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    fig.supxlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', y=0.05)
    fig.supylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', x=0.04)

    for idx in range(n_models, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row, col].set_visible(False)

    # Pad shared axes once
    if args.plot_baselines:
        ax0 = axes[0, 0]
        xlim = ax0.get_xlim()
        ylim = ax0.get_ylim()
        x_pad_0 = 0.05 * (xlim[1] - xlim[0])
        x_pad_1 = 0.09 * (xlim[1] - xlim[0])
        y_pad = 0.03 * (ylim[1] - ylim[0])
        ax0.set_xlim(xlim[0] - x_pad_0, xlim[1] + x_pad_1)
        ax0.set_ylim(ylim[0] - y_pad, ylim[1] + y_pad)

    legend_handles = []
    for game in games:
        legend_handles.append(plt.Line2D(
            [0], [0], marker='o', color='w',
            markerfacecolor=game_colors[game], markersize=10,
            label=GAME_MAPPING[game],
        ))
    legend_handles.append(plt.Line2D([0], [0], marker='o', color='gray',
                                     markersize=8, label='Collective'))
    legend_handles.append(plt.Line2D([0], [0], marker='s', color='gray',
                                     markersize=8, label='Selfish'))

    ncol = len(games) + 2
    fig.legend(handles=legend_handles, loc='upper center', frameon=False,
               bbox_to_anchor=(0.5, 1.02),
               ncol=ncol, columnspacing=0.6, handletextpad=0.5)

    top = _legend_top_reservation(len(legend_handles), ncol)
    plt.tight_layout(rect=[0, 0, 1, top])
    plt.savefig(output_dir / f"pca_by_model.{FORMAT}",
                format=FORMAT, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved pca_by_model.{FORMAT}")


# =============================================================================
# CENTROID-NEAREST STRATEGIES (for inspection)
# =============================================================================


def find_centroid_strategies(X, labels, game_labels, pca_data, games):
    """For each (game, model, base_attitude_family), find strategy nearest centroid."""
    for game_name in games:
        logger.info(f"\n  {game_name}:")
        mask = game_labels == game_name
        genes = pca_data[game_name]['genes']
        metadata = pca_data[game_name]['metadata']
        X_game = X[mask]
        labels_game = labels[mask]
        game_indices = np.where(mask)[0]

        models = sorted(set(g.model for g in genes))
        for model in models:
            for base_att in Attitude.base_attitudes():
                matching_genes = [
                    g for g in genes
                    if g.model == model
                    and g.attitude.to_base_attitude() == base_att
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

                game_local_indices = np.where(gene_mask)[0]
                metadata_idx = game_local_indices[local_idx]
                gene, strategy_name, feature_dict = metadata[metadata_idx]
                coop_rate = np.mean(list(feature_dict.values()))
                logger.info(
                    f"    {model}/{base_att.value} "
                    f"(actual: {gene}): {strategy_name} "
                    f"(dist={dists[local_idx]:.3f}, coop={coop_rate:.2%})"
                )


# =============================================================================
# EXTREMA ANALYSIS
# =============================================================================


def find_extrema(X_pca, metadata):
    extrema_indices = {
        'top_left': np.argmin(X_pca[:, 0] - X_pca[:, 1]),
        'top_right': np.argmax(X_pca[:, 0] + X_pca[:, 1]),
        'bottom_left': np.argmin(X_pca[:, 0] + X_pca[:, 1]),
        'bottom_right': np.argmax(X_pca[:, 0] - X_pca[:, 1]),
        'top': np.argmax(X_pca[:, 1]),
        'right': np.argmax(X_pca[:, 0]),
        'bottom': np.argmin(X_pca[:, 1]),
        'left': np.argmin(X_pca[:, 0]),
    }
    results = {}
    for position, idx in extrema_indices.items():
        gene, strategy_name, feature_dict = metadata[idx]
        results[position] = {
            'idx': idx,
            'gene': str(gene),
            'strategy': strategy_name,
            'coords': (X_pca[idx, 0], X_pca[idx, 1]),
            'features': feature_dict,
        }
        logger.info(f"\n{position.upper().replace('_', ' ')}:")
        logger.info(f"  Gene: {gene}")
        logger.info(f"  Strategy: {strategy_name}")
        logger.info(f"  PC1: {X_pca[idx, 0]:.3f}, PC2: {X_pca[idx, 1]:.3f}")
        coop_rate = np.mean(list(feature_dict.values()))
        logger.info(f"  Overall cooperation rate: {coop_rate:.2%}")
    return results


def plot_extrema(extrema_info, ax):
    for position, info in extrema_info.items():
        ax.annotate(f"{info['strategy']}\n({info['gene']})",
                    xy=info['coords'], xytext=(10, 10),
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5',
                              facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->',
                                    connectionstyle='arc3,rad=0', lw=1.5),
                    fontsize=8, zorder=10)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    args = parse_args()
    output_dir = get_output_dir(args)

    log_file = output_dir / "logs" / "diversity.log"
    setup_logging(log_file, args.log_level)
    logger = logging.getLogger(__name__)

    logger.info(f"Running diversity.py for games: {args.games}")

    # Globals shared across all games
    n_opponents = args.n_players - 1
    unique_combos: tuple[CooperatorCounts] = tuple(
        combo for combo, _ in make_fixed_opponents(n_opponents, args.n_rounds)
    )
    fixed_opponents: tuple[tuple[SimplePlayer]] = tuple(
        opponents for _, opponents in make_fixed_opponents(n_opponents, args.n_rounds)
    )

    # ==========================================================================
    # PHASE 1: Load/compute features
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

            if args.n_processes == 1:
                chunk_results = [compute_strategy_chunk(c) for c in chunks]
            else:
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
    # PHASE 2: Baselines
    # ==========================================================================
    logger.info(f"\n{'='*60}\nCOMPUTING BASELINES\n{'='*60}")
    game_class, _ = get_game_type(args.games[0])
    description = STANDARD_GENERATORS[args.games[0] + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    baseline_features = compute_baselines(args.n_players, args.n_rounds)
    # baseline_labels = list(baseline_features.keys()) + ['Rnd']
    baseline_labels = list(baseline_features.keys())
    baseline_X = [list(d.values()) for d in baseline_features.values()]
    n_features = len(baseline_X[0])
    # baseline_X = np.array(baseline_X + [[0.5] * n_features])

    logger.info(
        f"Features: {len(unique_combos)} unique opponent action combinations "
        f"of length {args.n_rounds - 1}, giving {n_features} features total "
        f"(including histories of shorter length)."
    )

    # ==========================================================================
    # PHASE 3: PCA on all data
    # ==========================================================================
    logger.info(f"\n{'='*60}\nCOMBINED PCA (fitted on all attitudes)\n{'='*60}")

    X_all = np.vstack([pca_data[g]['X'] for g in args.games])
    labels_all = np.concatenate([pca_data[g]['labels'] for g in args.games])
    game_labels = np.concatenate(
        [[g] * len(pca_data[g]['X']) for g in args.games])

    pca_combined, X_pca_combined = fit_pca_on_all(X_all)
    baseline_pca_combined = pca_combined.transform(baseline_X)

    random_baseline_dist = compute_random_baseline_distance(X_all.shape[1])

    # Scree plot
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

    # Shared axis limits across individual game plots
    all_xy = np.vstack([X_pca_combined[:, :2], baseline_pca_combined[:, :2]])
    x_min, x_max = all_xy[:, 0].min(), all_xy[:, 0].max()
    y_min, y_max = all_xy[:, 1].min(), all_xy[:, 1].max()
    if args.plot_baselines:
        x_pad_0 = 0.12 * (x_max - x_min)
        x_pad_1 = 0.08 * (x_max - x_min)
        y_pad_0 = 0.05 * (y_max - y_min)
        y_pad_1 = 0.05 * (y_max - y_min)
    else:
        x_pad_0 = 0
        x_pad_1 = 0
        y_pad_0 = 0
        y_pad_1 = 0
    shared_xlim = (x_min - x_pad_0, x_max + x_pad_1)
    shared_ylim = (y_min - y_pad_0, y_max + y_pad_1)


    # Per-game plots
    for game_name in args.games:
        mask = game_labels == game_name
        genes = pca_data[game_name]['genes']
        metadata = pca_data[game_name]['metadata']

        fig, axes = plt.subplots(1, 2, figsize=FIGSIZE, sharex=True, sharey=True)
        handles = plot_pca_single_game(
            axes, X_pca_combined, labels_all, mask, genes,
            baseline_pca_combined, baseline_labels, pca_combined,
        )

        # Apply shared limits (sharex/sharey propagates from axes[0])
        axes[0].set_xlim(shared_xlim)
        axes[0].set_ylim(shared_ylim)

        if args.plot_extrema:
            X_pca_game = X_pca_combined[mask]
            extrema_info = find_extrema(X_pca_game, metadata)
            # Route each extremum to its attitude's column
            for position, info in extrema_info.items():
                gene_obj, _, _ = metadata[info['idx']]
                col = 0 if gene_obj.attitude.to_base_attitude() == Attitude.COLLECTIVE else 1
                plot_extrema({position: info}, axes[col])

        fig.supxlabel(f'PC1 ({pca_combined.explained_variance_ratio_[0]:.1%})', y=0.09)
        fig.supylabel(f'PC2 ({pca_combined.explained_variance_ratio_[1]:.1%})', x=0.06)
        fig.legend(handles=handles, loc='upper center', frameon=False,
                   bbox_to_anchor=(0.5, 1.05),
                   ncol=min(len(handles), 4))

        plt.tight_layout(w_pad=0.07, h_pad=0.07)
        plt.savefig(output_dir / f"pca_{game_name}.{FORMAT}",
                    format=FORMAT, bbox_inches='tight')
        plt.close()


    # Combined 2x3 grid plot (attitudes × games)
    plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca_combined, baseline_labels, args.games,
                     pca_combined, output_dir)

    plot_pca_by_model(pca_data, X_pca_combined, labels_all, game_labels,
                      baseline_pca_combined, baseline_labels, args.games,
                      pca_combined, output_dir)

    # ==========================================================================
    # PHASE 4: Main metrics table
    # ==========================================================================
    logger.info(f"\n{'='*60}\nMAIN METRICS (aggregated by base family)\n{'='*60}")

    df_main = build_main_dataframe(
        X_all, labels_all, game_labels, pca_data,
        args.games, random_baseline_dist,
    )
    if not df_main.empty:
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', 200,
                               'display.float_format', '{:.2f}'.format):
            logger.info("\n" + df_main.to_string())
        df_main.to_csv(output_dir / "main_metrics.csv")
        write_main_latex(df_main, output_dir / "main_metrics.tex")

    # Per-round cooperation per gene × game
    logger.info(f"\n{'='*60}\nPER-ROUND COOPERATION\n{'='*60}")
    df_rounds = build_per_round_cooperation_df(pca_data, args.games, args.n_rounds)
    with pd.option_context('display.max_rows', None, 'display.width', 200,
                           'display.float_format', '{:.3f}'.format):
        logger.info("\n" + df_rounds.to_string())
    df_rounds.to_csv(output_dir / "per_round_cooperation.csv")
    plot_per_round_cooperation(df_rounds, args.games, args.n_rounds, output_dir)

    # Variance explained by game membership (per model)
    logger.info(f"\n{'='*60}\nVARIANCE EXPLAINED BY GAME MEMBERSHIP\n{'='*60}")
    all_genes_flat = []
    for g in args.games:
        all_genes_flat.extend(pca_data[g]['genes'])
    models_all = sorted(set(g.model for g in all_genes_flat))
    for model in models_all:
        model_mask = np.array([label.startswith(f"{model}[")
                               for label in labels_all])
        if model_mask.sum() == 0:
            continue
        eta_sq = compute_game_variance_explained(X_all[model_mask],
                                                 game_labels[model_mask])
        logger.info(f"  {pretty_model(model)}: η² = {eta_sq:.3f}")

    logger.info(f"\n{'='*60}\nCENTROID-NEAREST STRATEGIES\n{'='*60}")
    find_centroid_strategies(X_all, labels_all, game_labels, pca_data, args.games)

    # ==========================================================================
    # PHASE 5: Appendix synonym comparison
    # ==========================================================================
    logger.info(f"\n{'='*60}\nAPPENDIX: SYNONYM PLACEMENT\n{'='*60}")
    df_appendix = build_appendix_dataframe(
        X_all, labels_all, game_labels, pca_data, args.games,
    )
    if not df_appendix.empty:
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', 200,
                               'display.float_format', '{:.2f}'.format):
            logger.info("\n" + df_appendix.to_string())
        df_appendix.to_csv(output_dir / "appendix_synonyms.csv")
        write_appendix_latex(df_appendix, output_dir / "appendix_synonyms.tex")
    else:
        logger.info("No non-base synonyms found in data.")
