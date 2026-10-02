# pylint: disable=redefined-outer-name,missing-function-docstring,missing-class-docstring,possibly-used-before-assignment

import argparse
import logging
import pickle
from multiprocessing import Pool
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator, PercentFormatter
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

from emergent_llm.common import Attitude, C, D, Gene, setup
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import (
    CooperatorCounts,
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

FIGSIZE, FORMAT, _ = setup('royal_pca')

GAME_MAPPING = {
    'public_goods': 'Public Goods Game',
    'collective_risk': 'Collective Risk Dilemma',
    'common_pool': 'Common Pool Resource',
}

# Also defines the column order of the LaTeX tables.
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
    parser.add_argument("--results_dir", type=str, default="results")

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
    parser.add_argument("--weighting",
                        choices=["history", "round"],
                        default="history",
                        help="history: every history weighted equally (original). "
                             "round: every round weighted equally, histories "
                             "equally within a round")

    # Execution parameters
    parser.add_argument("--log_level",
                        type=str,
                        default="INFO",
                        help="Logging level to use")
    parser.add_argument("--n_processes",
                        type=int,
                        default=1,
                        help="Number of parallel processes")
    parser.add_argument("--n_strategies",
                        type=int,
                        default=None,
                        help="Limit the analysis to this many strategies")
    parser.add_argument("--recompute",
                        action='store_true',
                        help="Force recomputation of features even if cached")

    # Plotting parameters
    parser.add_argument("--plot_baselines",
                        action='store_true',
                        help="Label the baseline strategies")
    parser.add_argument("--plot_extrema",
                        action='store_true',
                        help="Label the corner strategies")

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
# FEATURE COMPUTATION
# Relies on module globals set in main (game_class, description, gene,
# game_name, unique_combos, fixed_opponents) so that worker processes
# inherit them via fork rather than pickling (Gene/Attitude enums).
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


def build_feature_keys(unique_combos, n_rounds) -> list[CooperatorCounts]:
    """Canonical feature order; matches the insertion order of compute_features."""
    keys = {}
    for combo in unique_combos:
        for r in range(n_rounds):
            keys.setdefault(combo[:r], None)
    return list(keys)


def feature_sqrt_weights(keys, n_rounds, n_opponents, weighting) -> np.ndarray:
    """sqrt of per-feature weights (weights sum to 1). Scaling features by this
    makes Euclidean geometry, and hence PCA and Delta, use the weighting."""
    if weighting == "history":
        w = np.full(len(keys), 1.0 / len(keys))
    else:
        w = np.array([1.0 / (n_rounds * (n_opponents + 1) ** len(k)) for k in keys])
    assert np.isclose(w.sum(), 1.0)
    return np.sqrt(w)


def weighted_coop(feature_dict) -> float:
    return float(sum(feature_dict[k] * w for k, w in zip(FEATURE_KEYS, SQRT_W**2)))


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


def create_baseline_players(n_players: int) -> list[SimplePlayer]:
    baseline_players = [
        SimplePlayer("AD", Defector),
        SimplePlayer("AC", Cooperator),
    ]
    baseline_players += [
        SimplePlayer(f"CC:{i}", ConditionalCooperator(C, i))
        for i in range(1, n_players)
    ]
    baseline_players += [
        SimplePlayer(f"CD:{i}", ConditionalDefector(D, i))
        for i in range(1, n_players)
    ]
    return baseline_players


def compute_baselines(n_players: int) -> dict[str, dict[CooperatorCounts, float]]:
    baseline_features = {}
    for player in create_baseline_players(n_players):
        features = compute_features(player, 1)
        baseline_features[player.id.name] = features
        logger.info(f"{player.id.name}: {np.mean(list(features.values())):.3f}")
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
    global_centroid = X.mean(axis=0)
    ss_total = np.sum((X - global_centroid)**2)
    ss_between = 0.0
    for game in np.unique(game_labels):
        mask = game_labels == game
        game_centroid = X[mask].mean(axis=0)
        ss_between += mask.sum() * np.sum((game_centroid - global_centroid)**2)
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
) -> pd.DataFrame:
    """
    Main metrics table: aggregated by base attitude family.

    Columns: (game, metric) where metric in {coop, coop_se, delta}.
    Rows: (model, attitude_family).
    Delta is per (model, game) and repeated across both attitude rows.
    """
    rows = []
    for game in games:
        models = sorted(set(g.model for g in pca_data[game]['genes']))
        for model in models:
            X_by_attitude = {
                base_att: aggregate_by_base_family(
                    X_all, labels_all, game_labels, pca_data,
                    game, model, base_att,
                )
                for base_att in Attitude.base_attitudes()
            }
            delta = compute_delta(X_by_attitude[Attitude.COLLECTIVE],
                                  X_by_attitude[Attitude.SELFISH])

            for base_att, X_set in X_by_attitude.items():
                if len(X_set) == 0:
                    continue
                # X_set is already scaled by SQRT_W, so this is sum_k w_k x_k.
                strategy_means = X_set @ SQRT_W
                coop = float(strategy_means.mean())
                coop_se = (float(strategy_means.std(ddof=1) / np.sqrt(len(strategy_means)))
                           if len(strategy_means) > 1 else np.nan)
                rows.append({
                    'game': game,
                    'model': model,
                    'attitude': base_att.value,
                    'coop': coop,
                    'coop_se': coop_se,
                    'delta': delta,
                })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # Pivot: index = (model, attitude), columns = (game, metric)
    df_pivot = df.pivot_table(
        index=['model', 'attitude'],
        columns='game',
        values=['coop', 'coop_se', 'delta'],
        aggfunc='first',
    ).swaplevel(axis=1)
    metric_order = ['coop', 'coop_se', 'delta']
    present = set(df_pivot.columns.get_level_values(0))
    new_cols = [(g, m) for g in games if g in present for m in metric_order
                if (g, m) in df_pivot.columns]
    df_pivot = df_pivot[new_cols]

    # Collective before selfish within each model
    return df_pivot.reindex(
        sorted(df_pivot.index,
               key=lambda x: (x[0], 0 if x[1] == Attitude.COLLECTIVE.value else 1))
    )


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
        models_in_game = sorted(set(g.model for g in pca_data[game]['genes']))
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
    ).swaplevel(axis=1)
    metric_order = ['d_own', 'd_other', 'ratio']
    present = set(df_pivot.columns.get_level_values(0))
    new_cols = [(g, m) for g in games if g in present for m in metric_order
                if (g, m) in df_pivot.columns]
    return df_pivot[new_cols]


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
                **{f'round_{r+1}': sums[r] / counts[r] for r in range(n_rounds)},
            })

    df = pd.DataFrame(rows)
    round_cols = [f'round_{r+1}' for r in range(n_rounds)]
    # Mean over strategies; every strategy contributes the same number of
    # prefixes per round, so this equals the flat mean over (strategy, prefix).
    return df.groupby(['game', 'model', 'attitude'])[round_cols].mean()


# =============================================================================
# LATEX WRITERS
# =============================================================================


def _fmt(x, precision=1):
    if pd.isna(x):
        return '--'
    return f"{x:.{precision}f}"


def _fmt_pm(val, se):
    """Compact uncertainty notation in percent: '68(1)\\%' = 0.68 ± 0.01."""
    if pd.isna(val):
        return '--'
    pct = round(val * 100)
    if pd.isna(se):
        return f"{pct}\\%"
    return f"{pct}({round(se * 100)})\\%"


def write_main_latex(df_pivot: pd.DataFrame, output_path: Path):
    """
    Main table as a bare booktabs tabular (requires booktabs, multirow, makecell).

    Per game: Coop for each attitude row, and Δ spanning both attitude rows.
    """
    if df_pivot.empty:
        logger.warning("Main DataFrame empty; skipping LaTeX write.")
        return

    present = set(df_pivot.columns.get_level_values(0))
    games = [g for g in GAME_SHORT if g in present]
    n_cols = 2 + 2 * len(games)
    models = list(dict.fromkeys(df_pivot.index.get_level_values(0)))

    lines = [
        f'\\begin{{tabular}}{{ll{"cc" * len(games)}}}',
        '\\toprule',
        'Model & Attitude & '
        + ' & '.join(f'\\multicolumn{{2}}{{c}}{{{GAME_SHORT[g]}}}' for g in games)
        + ' \\\\',
        ' & '.join(['', ''] + ['Coop', '$\\Delta$'] * len(games)) + ' \\\\',
        '\\midrule',
    ]

    for model_idx, model in enumerate(models):
        sub = df_pivot.loc[model]
        n_att = len(sub)
        for row_idx, (attitude, row) in enumerate(sub.iterrows()):
            first = row_idx == 0
            cells = [
                f'\\multirowcell{{{n_att}}}[0pt][l]{{{pretty_model(model)}}}'
                if first else '',
                attitude.capitalize(),
            ]
            for g in games:
                cells.append(_fmt_pm(row.get((g, 'coop')), row.get((g, 'coop_se'))))
                cells.append(
                    f'\\multirow{{{n_att}}}{{*}}{{{_fmt(row.get((g, "delta")), 1)}}}'
                    if first else '')
            lines.append(' & '.join(cells) + ' \\\\')
        is_last = model_idx == len(models) - 1
        lines.append('\\bottomrule' if is_last else f'\\cmidrule(lr){{1-{n_cols}}}')

    lines.append('\\end{tabular}')

    output_path.write_text('\n'.join(lines) + '\n')
    logger.info(f"Wrote main LaTeX table to {output_path}")


def write_appendix_latex(df_pivot: pd.DataFrame, output_path: Path):
    """Synonym comparison table for the appendix."""
    if df_pivot.empty:
        logger.warning("Appendix DataFrame empty; skipping LaTeX write.")
        return

    present = set(df_pivot.columns.get_level_values(0))
    games = [g for g in GAME_SHORT if g in present]
    n_games = len(games)

    col_spec = 'lll|' + '|'.join(['ccc'] * n_games)

    lines = [
        '% Auto-generated synonym comparison table.',
        '\\begin{table*}[t]',
        '\\caption{Synonym placement relative to base-attitude families. '
        '$d_{\\text{own}}$ uses leave-one-out (synonym excluded from own family centroid).}',
        '\\centering',
        '\\setlength{\\tabcolsep}{3pt}',
        f'\\begin{{tabular}}{{{col_spec}}}',
        '\\hline',
    ]

    header_groups = [
        f'\\multicolumn{{3}}{{c{"|" if i < n_games - 1 else ""}}}{{{GAME_SHORT[g]}}}'
        for i, g in enumerate(games)
    ]
    lines.append('Attitude & Synonym & Model & ' + ' & '.join(header_groups) + ' \\\\')
    metric_headers = ['', '', ''] + [
        '$d_{\\text{own}}$', '$d_{\\text{other}}$', 'ratio'] * n_games
    lines.append(' & '.join(metric_headers) + ' \\\\')
    lines.append('\\hline')

    last_family = None
    last_synonym = None
    for (family, synonym, model), row in df_pivot.iterrows():
        cells = []
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
            for metric in ('d_own', 'd_other', 'ratio'):
                cells.append(_fmt(row.get((g, metric), np.nan), 2))
        lines.append(' & '.join(cells) + ' \\\\')

    lines += [
        '\\hline',
        '\\end{tabular}',
        '\\label{tab:synonyms}',
        '\\end{table*}',
    ]

    output_path.write_text('\n'.join(lines) + '\n')
    logger.info(f"Wrote appendix LaTeX table to {output_path}")


# =============================================================================
# PCA
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
# PLOTTING
# =============================================================================

BASELINE_LABELS_LEFT = {"CC:2", "CC:3", "CD:1"}
BASELINE_LABELS_ABOVE = {"Rnd", "AD", "AC"}


def plot_baselines(ax, baseline_pca, baseline_labels, marker_size=100):
    """Plot baseline strategies with positioned labels.

    ha/va give where the point sits relative to the text. Labels not in
    LEFT/ABOVE are placed to the right.
    """
    for i, name in enumerate(baseline_labels):
        ax.scatter(baseline_pca[i, 0], baseline_pca[i, 1],
                   marker='X', s=marker_size, color='gray',
                   edgecolors='black', linewidths=1, zorder=6)
        if name in BASELINE_LABELS_LEFT:
            ha, va, xy = 'right', 'center', (-5, 0)
        elif name in BASELINE_LABELS_ABOVE:
            ha, va, xy = 'center', 'bottom', (0, 5)
        else:
            ha, va, xy = 'left', 'center', (5, 0)
        ax.annotate(name, (baseline_pca[i, 0], baseline_pca[i, 1]),
                    ha=ha, va=va, xytext=xy, textcoords='offset points')


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


def plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca, baseline_labels, games, pca, output_dir):
    """2×3 grid: rows = base attitude family, columns = games.

    For each (model, base_attitude) cell, aggregates all synonyms in that
    base-attitude family.
    """
    all_genes = [g for game in games for g in pca_data[game]['genes']]
    models = sorted(set(g.model for g in all_genes))
    cmap = plt.colormaps.get_cmap('tab10')
    model_colors = {m: cmap(i) for i, m in enumerate(models)}

    # Reserve the top strip of the figure for the legend.
    legend_rows = 2 if len(models) > 4 else 1
    legend_top = 0.92 if legend_rows == 1 else 0.86   # tune by eye

    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE, sharex=True, sharey=True,
                             layout='constrained')
    fig.get_layout_engine().set(w_pad=0.01, h_pad=0.01, wspace=0, hspace=0,
                                rect=(0, 0, 1, legend_top))

    for col, game in enumerate(games):
        game_mask = game_labels == game
        genes_for_game = pca_data[game]['genes']

        for row, base_att in enumerate(Attitude.base_attitudes()):
            ax = axes[row, col]
            ax.spines[['top', 'right']].set_visible(False)
            ax.spines['left'].set_visible(col == 0)
            ax.spines['bottom'].set_visible(row == axes.shape[0] - 1)
            ax.patch.set_visible(False)

            for model in models:
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

            if args.plot_baselines:
                plot_baselines(ax, baseline_pca, baseline_labels, marker_size=60)
                # Let labels overhang into neighbouring panels without the
                # layout making room for them.
                for t in ax.texts:
                    t.set_in_layout(False)
                    t.set_clip_on(False)

            if row == 0:
                ax.set_title(GAME_MAPPING[game])
            if col == 0:
                ax.set_ylabel(f"{base_att.capitalize()}")

        if args.plot_extrema:
            metadata = pca_data[game]['metadata']
            extrema_info = find_extrema(X_pca_combined[game_mask], metadata)
            base_order = list(Attitude.base_attitudes())
            for position, info in extrema_info.items():
                base = metadata[info['idx']][0].attitude.to_base_attitude()
                ax = axes[base_order.index(base), col]
                plot_extrema({position: info}, ax)
                # Keep constrained layout from shrinking panels to fit labels
                for t in ax.texts:
                    t.set_in_layout(False)

    fig.supxlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    fig.supylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')

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
    ncol = len(legend_handles) // 2 if legend_rows == 2 else len(legend_handles)
    fig.legend(handles=legend_handles, loc='outside upper center',
               frameon=False, ncol=ncol, borderpad=0, borderaxespad=0.3)

    out_path = output_dir / f"pca_by_game.{FORMAT}"
    plt.savefig(out_path, format=FORMAT)
    plt.close()
    logger.info(f"Saved {out_path}")


def plot_per_round_cooperation(df_rounds: pd.DataFrame, games: list[str],
                               n_rounds: int, output_dir: Path):
    """One subplot per game; colour = model, linestyle = base attitude.

    Synonym genes are collapsed to their base family by averaging the
    gene-level curves. This weights each gene equally, which equals
    per-strategy weighting as long as every gene has the same number of
    strategies (true by construction of the generation pipeline).
    """
    round_cols = [f'round_{r+1}' for r in range(n_rounds)]
    rounds = range(1, n_rounds + 1)

    # Collapse synonyms to base attitude
    df = df_rounds.reset_index()
    df['base_attitude'] = df['attitude'].map(
        lambda a: Attitude(a).to_base_attitude().value)
    df_base = df.groupby(['game', 'model', 'base_attitude'])[round_cols].mean()

    models = sorted(df['model'].unique())
    cmap = plt.colormaps.get_cmap('tab10')
    model_colors = {m: cmap(i) for i, m in enumerate(models)}
    linestyles = {Attitude.COLLECTIVE: '-', Attitude.SELFISH: '--'}

    # NOTE: resets global rcParams; call after the PCA plot.
    figsize, _, _ = setup('royal_cooperation')
    fig, axes = plt.subplots(1, len(games), figsize=figsize,
                             sharex=True, sharey=True)
    axes = np.atleast_1d(axes)

    for ax, game in zip(axes, games):
        for (model, base_value), row in df_base.loc[game].iterrows():
            ax.plot(rounds, row[round_cols].to_numpy(dtype=float),
                    color=model_colors[model],
                    linestyle=linestyles[Attitude(base_value)],
                    lw=1.25, marker='o', alpha=0.8)
        ax.set_title(GAME_MAPPING.get(game, game))
        ax.set_ylim(0, 1)
        ax.set_xticks(list(rounds))

    # sharey: setting on one axis applies to all
    axes[0].yaxis.set_major_locator(MultipleLocator(0.25))
    axes[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))
    fig.supxlabel('Round')
    fig.supylabel('Cooperation rate (%)')

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

    fig.legend(handles=interleaved, loc='outside upper center',
               frameon=False, ncol=n_cols, borderpad=0, borderaxespad=0.3)

    out_path = output_dir / f"per_round_cooperation.{FORMAT}"
    plt.savefig(out_path, format=FORMAT)
    plt.close()
    logger.info(f"Saved {out_path}")


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

        for model in sorted(set(g.model for g in genes)):
            for base_att in Attitude.base_attitudes():
                gene_strs = [
                    str(g) for g in genes
                    if g.model == model
                    and g.attitude.to_base_attitude() == base_att
                ]
                gene_mask = np.isin(labels_game, gene_strs)
                X_group = X_game[gene_mask]
                if len(X_group) == 0:
                    continue

                centroid = X_group.mean(axis=0, keepdims=True)
                dists = cdist(centroid, X_group, metric='euclidean')[0]
                local_idx = np.argmin(dists)

                metadata_idx = np.where(gene_mask)[0][local_idx]
                gene, strategy_name, feature_dict = metadata[metadata_idx]
                logger.info(
                    f"    {model}/{base_att.value} "
                    f"(actual: {gene}): {strategy_name} "
                    f"(dist={dists[local_idx]:.3f}, "
                    f"coop={weighted_coop(feature_dict):.2%})"
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
        logger.info(f"  Overall cooperation rate: {weighted_coop(feature_dict):.2%}")
    return results


def plot_extrema(extrema_info, ax):
    for info in extrema_info.values():
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


def log_df(df: pd.DataFrame, float_format: str):
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.width', 200,
                           'display.float_format', float_format.format):
        logger.info("\n" + df.to_string())


def log_section(title: str):
    logger.info(f"\n{'='*60}\n{title}\n{'='*60}")


if __name__ == "__main__":
    args = parse_args()
    output_dir = get_output_dir(args)

    setup_logging(output_dir / "logs" / "diversity.log", args.log_level)
    logger = logging.getLogger(__name__)

    logger.info(f"Running diversity.py for games: {args.games}")

    # Globals shared across all games
    n_opponents = args.n_players - 1
    fixed = list(make_fixed_opponents(n_opponents, args.n_rounds))
    unique_combos: tuple[CooperatorCounts] = tuple(combo for combo, _ in fixed)
    fixed_opponents: tuple[tuple[SimplePlayer]] = tuple(opps for _, opps in fixed)
    FEATURE_KEYS = build_feature_keys(unique_combos, args.n_rounds)
    SQRT_W = feature_sqrt_weights(FEATURE_KEYS, args.n_rounds, n_opponents,
                                  args.weighting)
    output_dir = output_dir / args.weighting
    output_dir.mkdir(parents=True, exist_ok=True)

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
        genes = sorted(registry.available_genes, key=str)
        results_dict = {}

        for gene in genes:
            if not args.recompute:
                cached_data = load_features(game_name, gene, args)
                if cached_data is not None:
                    results_dict[gene] = cached_data
                    continue

            all_specs = registry.get_all_specs(gene)
            n_strategies = (len(all_specs) if args.n_strategies is None
                            else min(len(all_specs), args.n_strategies))
            chunks = chunk_indices(n_strategies, args.n_processes)
            logger.info(
                f"Computing {n_strategies} strategies for {gene} in {len(chunks)} chunks"
            )

            if args.n_processes == 1:
                chunk_results = [compute_strategy_chunk(c) for c in chunks]
            else:
                with Pool(processes=args.n_processes) as pool:
                    chunk_results = pool.map(compute_strategy_chunk, chunks)

            strategy_features = {
                strategy_name: features
                for chunk_result in chunk_results
                for strategy_name, features in chunk_result
            }
            save_features(strategy_features, game_name, gene, args)
            results_dict[gene] = strategy_features

        logger.info(f"Results for {len(results_dict)} genes, with "
                    f"{sum(len(v) for v in results_dict.values())} strategies "
                    f"in total for {game_name}")

        X_game, labels_game, metadata_game = [], [], []
        for gene, strategy_features in results_dict.items():
            for strategy_name, feature_dict in strategy_features.items():
                X_game.append([feature_dict[k] for k in FEATURE_KEYS])
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
    log_section("COMPUTING BASELINES")
    game_class, _ = get_game_type(args.games[0])
    description = STANDARD_GENERATORS[args.games[0] + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    baseline_features = compute_baselines(args.n_players)
    baseline_labels = list(baseline_features.keys()) + ['Rnd']
    n_features = len(FEATURE_KEYS)
    baseline_X = np.array(
        [[d[k] for k in FEATURE_KEYS] for d in baseline_features.values()]
        + [[0.5] * n_features]
    ) * SQRT_W

    logger.info(
        f"Features: {len(unique_combos)} unique opponent action combinations "
        f"of length {args.n_rounds - 1}, giving {n_features} features total "
        f"(including histories of shorter length)."
    )

    # ==========================================================================
    # PHASE 3: PCA on all data
    # ==========================================================================
    log_section("COMBINED PCA (fitted on all attitudes)")

    X_all = np.vstack([pca_data[g]['X'] for g in args.games]) * SQRT_W
    labels_all = np.concatenate([pca_data[g]['labels'] for g in args.games])
    game_labels = np.concatenate(
        [[g] * len(pca_data[g]['X']) for g in args.games])

    pca_combined, X_pca_combined = fit_pca_on_all(X_all)
    baseline_pca_combined = pca_combined.transform(baseline_X)

    plot_pca_by_game(pca_data, X_pca_combined, labels_all, game_labels,
                     baseline_pca_combined, baseline_labels, args.games,
                     pca_combined, output_dir)

    # ==========================================================================
    # PHASE 4: Per-round cooperation
    # ==========================================================================
    log_section("PER-ROUND COOPERATION")
    df_rounds = build_per_round_cooperation_df(pca_data, args.games, args.n_rounds)
    log_df(df_rounds, '{:.3f}')
    df_rounds.to_csv(output_dir / "per_round_cooperation.csv")
    plot_per_round_cooperation(df_rounds, args.games, args.n_rounds, output_dir)

    # ==========================================================================
    # PHASE 5: Main metrics table
    # ==========================================================================
    log_section("MAIN METRICS (aggregated by base family)")
    df_main = build_main_dataframe(X_all, labels_all, game_labels, pca_data,
                                   args.games)
    if not df_main.empty:
        log_df(df_main, '{:.2f}')
        df_main.to_csv(output_dir / "main_metrics.csv")
        write_main_latex(df_main, output_dir / "main_metrics.tex")

    log_section("VARIANCE EXPLAINED BY GAME MEMBERSHIP")
    models_all = sorted(set(g.model for game in args.games
                            for g in pca_data[game]['genes']))
    for model in models_all:
        model_mask = np.array([label.startswith(f"{model}[")
                               for label in labels_all])
        if model_mask.sum() == 0:
            continue
        eta_sq = compute_game_variance_explained(X_all[model_mask],
                                                 game_labels[model_mask])
        logger.info(f"  {pretty_model(model)}: η² = {eta_sq:.3f}")

    log_section("CENTROID-NEAREST STRATEGIES")
    find_centroid_strategies(X_all, labels_all, game_labels, pca_data, args.games)

    # ==========================================================================
    # PHASE 6: Appendix synonym comparison
    # ==========================================================================
    log_section("APPENDIX: SYNONYM PLACEMENT")
    df_appendix = build_appendix_dataframe(
        X_all, labels_all, game_labels, pca_data, args.games,
    )
    if not df_appendix.empty:
        log_df(df_appendix, '{:.2f}')
        df_appendix.to_csv(output_dir / "appendix_synonyms.csv")
        write_appendix_latex(df_appendix, output_dir / "appendix_synonyms.tex")
    else:
        logger.info("No non-base synonyms found in data.")
