"""PCA and prompt-word sensitivity analysis for strategy variants.

This script mirrors the existing diversity analysis but groups strategies by
their prompt wording within a base behavioural family. It supports both:

- the original core-code layout, where a single ``<model>.py`` file can contain
  ``Strategy_COLLECTIVE_*``, ``Strategy_PROSOCIAL_*``, etc.; and
- the earlier wrapper layout, where files were split as
  ``<base-model>__<prompt-word>.py``.
"""

import argparse
import logging
import pickle
import random
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
    PlayerHistory,
    setup,
)
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import (
    Altenator,
    BasePlayer,
    ConditionalCooperator,
    Cooperator,
    Defector,
    GradualDefector,
    Grim,
    HistoricalCooperator,
    LLMPlayer,
    PeriodicDefector,
    Random,
    RandomCooperator,
    RandomDefector,
    SimplePlayer,
    SpecialRounds,
)

FIGSIZE, FORMAT = setup("fullscreen")
OpponentActions = tuple[tuple[Action, ...], ...]

COLLECTIVE_WORDS = tuple(attitude.value for attitude in (
    Attitude.COLLECTIVE,
    Attitude.PROSOCIAL,
    Attitude.COMMUNAL,
))
EXPLOITATIVE_WORDS = tuple(attitude.value for attitude in (
    Attitude.EXPLOITATIVE,
    Attitude.AGGRESSIVE,
    Attitude.OPPORTUNISTIC,
))

args: argparse.Namespace
logger: logging.Logger
description = None
game_class = None
game_name = ""
registry: StrategyRegistry
unique_combos: tuple
combo_keys: list[tuple[str, ...]] | None = None


@dataclass(frozen=True)
class BaselineSpec:
    name: str
    factory: callable


@dataclass(frozen=True)
class PromptGroupInfo:
    game: str
    base_model: str
    prompt_word: str
    family: str


@dataclass
class PromptGroupMetrics:
    game: str
    base_model: str
    prompt_word: str
    family: str
    n_strategies: int
    mean_pairwise_distance: float
    mean_pairwise_distance_normalised: float
    participation_ratio: float


@dataclass
class PromptPairMetrics:
    game: str
    base_model: str
    family: str
    word_a: str
    word_b: str
    n_a: int
    n_b: int
    centroid_distance: float
    cohens_d: float


GROUP_METRIC_COLUMNS = [
    "game",
    "base_model",
    "prompt_word",
    "family",
    "n_strategies",
    "mean_pairwise_distance",
    "mean_pairwise_distance_normalised",
    "participation_ratio",
]

PAIR_METRIC_COLUMNS = [
    "game",
    "base_model",
    "family",
    "word_a",
    "word_b",
    "n_a",
    "n_b",
    "centroid_distance",
    "cohens_d",
]

PROMPT_WORD_ORDER = [
    "collective",
    "prosocial",
    "communal",
    "exploitative",
    "aggressive",
    "opportunistic",
]

SUMMARY_TABLE_COLUMNS = [
    "game",
    "base_model",
    "family",
    "prompt_word",
    "n_strategies",
    "mean_pairwise_distance",
    "mean_pairwise_distance_normalised",
    "participation_ratio",
    "canonical_prompt_word",
    "shift_centroid_distance",
    "shift_cohens_d",
]


def build_table1_style_wide(summary_df: pd.DataFrame) -> pd.DataFrame:
    if summary_df.empty:
        return pd.DataFrame()

    rows: list[dict] = []
    games = list(dict.fromkeys(summary_df["game"]))

    key_columns = ["base_model", "family", "prompt_word"]
    for key_values, subdf in summary_df.groupby(key_columns, sort=False):
        row = dict(zip(key_columns, key_values, strict=True))
        for game in games:
            game_df = subdf[subdf["game"] == game]
            if game_df.empty:
                row[f"{game}_MPD"] = np.nan
                row[f"{game}_d"] = np.nan
                row[f"{game}_PR"] = np.nan
                continue

            metric_row = game_df.iloc[0]
            row[f"{game}_MPD"] = metric_row[
                "mean_pairwise_distance_normalised"]
            row[f"{game}_d"] = metric_row["shift_cohens_d"]
            row[f"{game}_PR"] = metric_row["participation_ratio"]
        rows.append(row)

    wide_df = pd.DataFrame(rows)
    if wide_df.empty:
        return wide_df

    return wide_df.sort_values(
        by=["base_model", "family", "prompt_word"],
        key=lambda column: column.map(prompt_word_sort_key)
        if column.name == "prompt_word" else column,
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run PCA and centroid sensitivity analysis for prompt-word variants."
    )
    parser.add_argument("--games",
                        type=str,
                        nargs="+",
                        default=["public_goods"],
                        choices=["public_goods", "collective_risk",
                                 "common_pool"],
                        help="Game type(s) to analyse")
    parser.add_argument("--strategies_dir",
                        type=str,
                        default="strategies",
                        help="Base directory containing strategy files")
    parser.add_argument("--models",
                        nargs="*",
                        default=None,
                        help="Optional base model filter, e.g. gpt-5-mini")
    parser.add_argument(
        "--n_strategies",
        type=int,
        default=32,
        help="Randomly sample this many strategies per gene before feature computation.",
    )
    parser.add_argument("--sample_seed",
                        type=int,
                        default=0,
                        help="Seed used for random strategy subsampling")
    parser.add_argument("--feature_mode",
                        type=str,
                        default="fixed_actions",
                        choices=["fixed_actions", "baseline_opponents"])
    parser.add_argument("--n_players", type=int, default=4)
    parser.add_argument("--n_rounds", type=int, default=5)
    parser.add_argument("--n_games", type=int, default=20)
    parser.add_argument("--recompute", action="store_true")
    parser.add_argument("--results_dir",
                        type=str,
                        default="results",
                        help="Directory used for plots, tables and caches")
    return parser.parse_args()


def setup_logging(log_file: Path, loglevel=logging.INFO):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file),
                  logging.StreamHandler()],
    )


def get_output_dir(local_args: argparse.Namespace) -> Path:
    return Path(local_args.results_dir) / "diversity_prompt_sensitivity" / local_args.feature_mode


def get_cache_path(local_game_name: str, gene: Gene,
                   local_args: argparse.Namespace) -> Path:
    cache_dir = get_output_dir(local_args) / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    safe_gene = f"{gene.model}__{gene.attitude.value}"
    filename = f"{local_game_name}_{safe_gene}_p{local_args.n_players}_r{local_args.n_rounds}_g{local_args.n_games}"
    if local_args.n_strategies is not None:
        filename += f"_s{local_args.n_strategies}_seed{local_args.sample_seed}"
    return cache_dir / f"{filename}.pkl"


def save_features(features_dict, local_game_name: str, gene: Gene,
                  local_args: argparse.Namespace):
    cache_path = get_cache_path(local_game_name, gene, local_args)
    with open(cache_path, "wb") as handle:
        pickle.dump(features_dict, handle)
    logger.info("Saved features to %s", cache_path)


def load_features(local_game_name: str, gene: Gene,
                  local_args: argparse.Namespace):
    cache_path = get_cache_path(local_game_name, gene, local_args)
    if not cache_path.exists():
        return None
    with open(cache_path, "rb") as handle:
        features_dict = pickle.load(handle)
    logger.info("Loaded features from %s", cache_path)
    return features_dict


def prompt_word_sort_key(prompt_word: str) -> int:
    try:
        return PROMPT_WORD_ORDER.index(prompt_word)
    except ValueError:
        return len(PROMPT_WORD_ORDER)


def build_prompt_sensitivity_summary(group_df: pd.DataFrame,
                                     pair_df: pd.DataFrame) -> pd.DataFrame:
    if group_df.empty:
        return pd.DataFrame(columns=SUMMARY_TABLE_COLUMNS)

    pair_lookup: dict[tuple[str, str, str, str, str], tuple[float, float]] = {}
    if not pair_df.empty:
        for _, row in pair_df.iterrows():
            key = (row["game"], row["base_model"], row["family"],
                   row["word_a"], row["word_b"])
            reverse_key = (row["game"], row["base_model"], row["family"],
                           row["word_b"], row["word_a"])
            value = (row["centroid_distance"], row["cohens_d"])
            pair_lookup[key] = value
            pair_lookup[reverse_key] = value

    family_to_canonical = {
        "collective": "collective",
        "exploitative": "exploitative",
    }

    rows: list[dict] = []
    for _, row in group_df.iterrows():
        canonical_prompt_word = family_to_canonical[row["family"]]
        shift_centroid_distance = np.nan
        shift_cohens_d = np.nan

        if row["prompt_word"] != canonical_prompt_word:
            pair_key = (row["game"], row["base_model"], row["family"],
                        canonical_prompt_word, row["prompt_word"])
            if pair_key in pair_lookup:
                shift_centroid_distance, shift_cohens_d = pair_lookup[pair_key]

        rows.append({
            "game": row["game"],
            "base_model": row["base_model"],
            "family": row["family"],
            "prompt_word": row["prompt_word"],
            "n_strategies": row["n_strategies"],
            "mean_pairwise_distance": row["mean_pairwise_distance"],
            "mean_pairwise_distance_normalised":
                row["mean_pairwise_distance_normalised"],
            "participation_ratio": row["participation_ratio"],
            "canonical_prompt_word": canonical_prompt_word,
            "shift_centroid_distance": shift_centroid_distance,
            "shift_cohens_d": shift_cohens_d,
        })

    summary_df = pd.DataFrame(rows, columns=SUMMARY_TABLE_COLUMNS)
    if summary_df.empty:
        return summary_df

    return summary_df.sort_values(
        by=["game", "base_model", "family", "prompt_word"],
        key=lambda column: column.map(prompt_word_sort_key)
        if column.name == "prompt_word" else column,
    )


class FixedOpponent:

    def __init__(self, fixed_actions):
        self.fixed_actions: list[Action] = fixed_actions

    def __call__(self, state: GameState, _: PlayerHistory | None):
        return self.fixed_actions[state.round_number]


def context_to_key(arr: list[list[Action]]) -> OpponentActions:
    return tuple(map(tuple, arr))


def build_baseline_pool(n_rounds: int) -> list[BaselineSpec]:
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


def combo_key(combo: tuple[BaselineSpec, ...]) -> tuple[str, ...]:
    return tuple(spec.name for spec in combo)


def play_games(player: LLMPlayer, n_games: int,
               combo: OpponentActions) -> list[GameHistory]:
    opponents = [
        SimplePlayer(f"opponent_{i+1}", FixedOpponent(list(actions) + [C]))
        for i, actions in enumerate(combo)
    ]
    players = [player] + opponents
    return [game_class(players, description).play_game().history
            for _ in range(n_games)]


def play_games_against_opponents(player: BasePlayer,
                                 opponents: list[SimplePlayer],
                                 n_games: int) -> list[GameHistory]:
    players = [player] + opponents
    return [game_class(players, description).play_game().history
            for _ in range(n_games)]


def compute_features(player: BasePlayer, n_games: int) -> dict[OpponentActions,
                                                               float]:
    features = {}
    for combo in unique_combos:
        histories = play_games(player, n_games, combo)
        player_history = histories[0].for_player(0)
        for round_idx in range(args.n_rounds):
            context = Action.from_bool_array(player_history.opponent_actions[:round_idx])
            actions = [Action(history.actions[round_idx, 0]) for history in histories]
            features[context_to_key(context)] = float(
                Action.to_bool_array(actions).mean())
    return features


def compute_features_baseline_opponents(player: BasePlayer,
                                        n_games: int) -> dict[tuple,
                                                               float] | None:
    features: dict[tuple, float] = {}
    for combo in unique_combos:
        opponents = [
            SimplePlayer(f"opponent_{i+1}", spec.factory())
            for i, spec in enumerate(combo)
        ]
        try:
            histories = play_games_against_opponents(player, opponents, n_games)
        except Exception as exc:
            logger.warning("Failed on combo %s for %s: %s", combo_key(combo),
                           player.id.name, exc)
            return None

        key = combo_key(combo)
        for round_idx in range(args.n_rounds):
            actions = [Action(history.actions[round_idx, 0]) for history in histories]
            features[(key, round_idx)] = float(Action.to_bool_array(actions).mean())
    return features


def sample_specs(gene: Gene):
    specs = list(registry.get_all_specs(gene))
    if args.n_strategies is None or len(specs) <= args.n_strategies:
        logger.info("Using all %d strategies for %s", len(specs), gene)
        return specs

    rng = random.Random(f"{args.sample_seed}:{game_name}:{gene}")
    indices = list(range(len(specs)))
    rng.shuffle(indices)
    sampled = [specs[i] for i in indices[:args.n_strategies]]
    logger.info("Sampled %d/%d strategies for %s",
                len(sampled), len(specs), gene)
    return sampled


def compute_gene(gene: Gene) -> dict[str, dict[tuple, float]]:
    logger.info("Computing features for %s", gene)
    if not args.recompute:
        cached = load_features(game_name, gene, args)
        if cached is not None:
            logger.info("Using cached features for %s (%d strategies)",
                        gene, len(cached))
            return cached

    strategy_features = {}
    sampled_specs = sample_specs(gene)
    for idx, strategy_spec in enumerate(sampled_specs, start=1):
        algo = strategy_spec.strategy_class
        player = LLMPlayer("testing", gene, description, algo)
        logger.info("  [%d/%d] %s", idx, len(sampled_specs), algo.__name__)

        try:
            if args.feature_mode == "baseline_opponents":
                features = compute_features_baseline_opponents(player,
                                                               args.n_games)
            else:
                features = compute_features(player, args.n_games)
        except Exception:
            logger.exception("Error while computing features for %s %s",
                             gene.model, algo.__name__)
            continue

        if features is None:
            logger.warning("Skipping %s %s due to failed combo", gene.model,
                           algo.__name__)
            continue

        strategy_features[algo.__name__] = features

    save_features(strategy_features, game_name, gene, args)
    logger.info("Finished %s: %d strategies with valid features",
                gene, len(strategy_features))
    return strategy_features


def create_baseline_players(n_players: int,
                            n_rounds: int) -> list[SimplePlayer]:
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
                          [n_rounds - 1]),
        ) for i in [2]
    ]
    return baseline_players


def compute_baselines(n_players: int,
                      n_rounds: int) -> dict[str, dict[tuple, float]]:
    baseline_players = create_baseline_players(n_players, n_rounds)
    baseline_features = {}
    n_games = args.n_games if args.feature_mode == "baseline_opponents" else 1

    for player in baseline_players:
        try:
            if args.feature_mode == "baseline_opponents":
                features = compute_features_baseline_opponents(player, n_games)
            else:
                features = compute_features(player, n_games)
        except Exception:
            logger.exception("Error while computing baseline features for %s",
                             player.id.name)
            continue
        if features is None:
            continue
        baseline_features[player.id.name] = features
    return baseline_features


def build_feature_vector(feature_dict: dict[tuple, float]) -> list[float]:
    if args.feature_mode == "baseline_opponents":
        if combo_keys is None:
            raise RuntimeError("combo_keys is not set for baseline opponents")
        vector = []
        for current_combo_key in combo_keys:
            for round_idx in range(args.n_rounds):
                vector.append(feature_dict.get((current_combo_key, round_idx),
                                               0.0))
        return vector
    return list(feature_dict.values())


def compute_random_baseline_distance(n_features: int,
                                     n_samples: int = 500) -> float:
    random_X = np.random.uniform(0, 1, (n_samples, n_features))
    return float(np.mean(pdist(random_X, metric="euclidean")))


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
    return float((eigenvalues.sum() ** 2) / (eigenvalues ** 2).sum())


def compute_between_set_metrics(X_a: np.ndarray,
                                X_b: np.ndarray) -> tuple[float, float]:
    if len(X_a) == 0 or len(X_b) == 0:
        return np.nan, np.nan

    centroid_a = X_a.mean(axis=0)
    centroid_b = X_b.mean(axis=0)
    centroid_distance = float(np.linalg.norm(centroid_a - centroid_b))

    var_a = np.var(X_a, axis=0).mean() if len(X_a) > 1 else 0.0
    var_b = np.var(X_b, axis=0).mean() if len(X_b) > 1 else 0.0
    n_a, n_b = len(X_a), len(X_b)
    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2) if (n_a + n_b) > 2 else 1.0
    pooled_std = np.sqrt(pooled_var * X_a.shape[1])
    cohens_d = centroid_distance / pooled_std if pooled_std > 0 else np.nan
    return centroid_distance, float(cohens_d)


def plot_covariance_ellipse(ax, mean, cov, n_std=1.0, **kwargs):
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(np.maximum(eigenvalues, 0))
    ellipse = Ellipse(mean, width, height, angle=angle, **kwargs)
    ax.add_patch(ellipse)


def plot_grouped_pca(ax, X_pca, group_labels, groups, baseline_pca,
                     baseline_labels, title, pca):
    colors = plt.colormaps.get_cmap("tab10")(np.linspace(0, 1, len(groups)))
    handles = []

    for idx, group in enumerate(groups):
        mask = group_labels == group
        points = X_pca[mask, :2]
        scatter = ax.scatter(points[:, 0],
                             points[:, 1],
                             alpha=0.35,
                             s=12,
                             color=colors[idx])
        if len(points) > 0:
            mean_pt = points.mean(axis=0)
            ax.scatter(mean_pt[0],
                       mean_pt[1],
                       marker="o",
                       s=120,
                       color=colors[idx],
                       edgecolors="black",
                       linewidths=1.5,
                       zorder=5)
            if len(points) > 2:
                cov = np.cov(points.T)
                plot_covariance_ellipse(ax,
                                        mean_pt,
                                        cov,
                                        n_std=1.0,
                                        facecolor=colors[idx],
                                        alpha=0.15,
                                        edgecolor=colors[idx],
                                        linewidth=1.5)
        handles.append((scatter, group))

    for idx, name in enumerate(baseline_labels):
        ax.scatter(baseline_pca[idx, 0],
                   baseline_pca[idx, 1],
                   marker="X",
                   s=120,
                   edgecolors="black",
                   linewidths=1,
                   zorder=6)
        ax.annotate(name, (baseline_pca[idx, 0], baseline_pca[idx, 1]),
                    fontsize=6)

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_title(title)
    ax.legend([item[0] for item in handles], [item[1] for item in handles],
              fontsize=7)


def parse_prompt_group(gene: Gene) -> PromptGroupInfo:
    if "__" in gene.model:
        base_model, prompt_word = gene.model.rsplit("__", 1)
    else:
        base_model = gene.model
        prompt_word = gene.attitude.value
    family = gene.attitude.to_base_attitude().value
    return PromptGroupInfo(game=game_name,
                           base_model=base_model,
                           prompt_word=prompt_word,
                           family=family)


def model_allowed(gene: Gene) -> bool:
    if not args.models:
        return True
    info = parse_prompt_group(gene)
    return info.base_model in set(args.models)


def prefer_core_layout_genes(genes: list[Gene]) -> list[Gene]:
    core_pairs = {
        (parse_prompt_group(gene).base_model, parse_prompt_group(gene).prompt_word)
        for gene in genes if "__" not in gene.model
    }

    filtered = []
    skipped = 0
    for gene in genes:
        info = parse_prompt_group(gene)
        if "__" in gene.model and (info.base_model, info.prompt_word) in core_pairs:
            skipped += 1
            continue
        filtered.append(gene)

    if skipped:
        logger.info("Skipped %d wrapper-layout genes because core-layout "
                    "strategies exist for the same model/prompt word", skipped)
    return filtered


def ensure_feature_context():
    global unique_combos, combo_keys
    if args.feature_mode == "baseline_opponents":
        baseline_specs = build_baseline_pool(args.n_rounds)
        unique_combos = tuple(
            combinations_with_replacement(baseline_specs, args.n_players - 1))
        combo_keys = [combo_key(combo) for combo in unique_combos]
    else:
        all_actions = tuple(product([D, C], repeat=args.n_rounds - 1))
        unique_combos = tuple(
            combinations_with_replacement(all_actions, args.n_players - 1))
        combo_keys = None


def main():
    global args, logger, game_name, game_class, description, registry

    args = parse_args()
    output_dir = get_output_dir(args)
    log_file = output_dir / "logs" / "diversity_prompt_sensitivity.log"
    setup_logging(log_file)
    logger = logging.getLogger(__name__)

    ensure_feature_context()
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Running prompt sensitivity analysis for games: %s", args.games)
    logger.info("Strategy subsample per gene: %s", args.n_strategies)
    logger.info("Sample seed: %s", args.sample_seed)

    pca_data: dict[str, dict[str, np.ndarray | list | dict]] = {}

    for game_name in args.games:
        logger.info("Starting game: %s", game_name)
        game_class, _ = get_game_type(game_name)
        description = STANDARD_GENERATORS[game_name + "_default"](
            n_players=args.n_players, n_rounds=args.n_rounds)
        registry = StrategyRegistry(strategies_dir=args.strategies_dir,
                                    game_name=game_name)
        genes = sorted([gene for gene in registry.available_genes if model_allowed(gene)],
                       key=str)
        genes = prefer_core_layout_genes(genes)
        logger.info("Found %d genes for %s", len(genes), game_name)

        if not genes:
            logger.warning("No genes found for %s", game_name)
            continue

        results_dict = {gene: compute_gene(gene) for gene in genes}
        logger.info("Completed feature extraction for %s", game_name)

        X_game = []
        labels_gene = []
        labels_base_model = []
        labels_prompt_word = []
        labels_family = []
        metadata_game = []

        for gene, strategy_features in results_dict.items():
            info = parse_prompt_group(gene)
            for strategy_name, feature_dict in strategy_features.items():
                X_game.append(build_feature_vector(feature_dict))
                labels_gene.append(str(gene))
                labels_base_model.append(info.base_model)
                labels_prompt_word.append(info.prompt_word)
                labels_family.append(info.family)
                metadata_game.append({
                    "gene": gene,
                    "strategy_name": strategy_name,
                    "base_model": info.base_model,
                    "prompt_word": info.prompt_word,
                    "family": info.family,
                })

        if not X_game:
            logger.warning("No strategy features computed for %s", game_name)
            continue

        pca_data[game_name] = {
            "X": np.array(X_game),
            "labels_gene": np.array(labels_gene),
            "labels_base_model": np.array(labels_base_model),
            "labels_prompt_word": np.array(labels_prompt_word),
            "labels_family": np.array(labels_family),
            "metadata": metadata_game,
            "genes": genes,
        }
        logger.info("Built feature matrix for %s: %d strategies x %d features",
                    game_name, len(X_game), len(X_game[0]))

    if not pca_data:
        raise ValueError("No PCA data available. Check strategies_dir and model filters.")

    first_game = next(iter(pca_data))
    game_class, _ = get_game_type(first_game)
    description = STANDARD_GENERATORS[first_game + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    baseline_features = compute_baselines(args.n_players, args.n_rounds)
    logger.info("Computed %d baseline feature sets", len(baseline_features))
    baseline_labels = list(baseline_features.keys()) + ["Random 0.5"]
    baseline_X = [build_feature_vector(data) for data in baseline_features.values()]
    if not baseline_X:
        raise ValueError("Failed to compute baseline features.")
    n_features = len(baseline_X[0])
    baseline_X = np.array(baseline_X + [[0.5] * n_features])

    X_all = np.vstack([pca_data[current_game]["X"] for current_game in pca_data])
    labels_all_gene = np.concatenate(
        [pca_data[current_game]["labels_gene"] for current_game in pca_data])
    labels_all_base_model = np.concatenate(
        [pca_data[current_game]["labels_base_model"] for current_game in pca_data])
    labels_all_prompt_word = np.concatenate(
        [pca_data[current_game]["labels_prompt_word"] for current_game in pca_data])
    labels_all_family = np.concatenate(
        [pca_data[current_game]["labels_family"] for current_game in pca_data])
    game_labels = np.concatenate([[current_game] * len(pca_data[current_game]["X"])
                                  for current_game in pca_data])

    n_components = min(10, X_all.shape[1], X_all.shape[0])
    pca_combined = PCA(n_components=n_components)
    logger.info("Running PCA on %d strategies with %d components",
                X_all.shape[0], n_components)
    X_pca_combined = pca_combined.fit_transform(X_all)
    baseline_pca_combined = pca_combined.transform(baseline_X)
    logger.info("Finished PCA")

    cumulative = np.cumsum(pca_combined.explained_variance_ratio_)
    plt.figure()
    plt.plot(range(1, len(cumulative) + 1), cumulative, "o-")
    plt.axhline(y=0.9, color="r", linestyle="--", label="90% threshold")
    plt.xlabel("Component")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("Prompt Sensitivity PCA Scree Plot")
    plt.legend()
    plt.savefig(output_dir / f"scree_combined.{FORMAT}",
                format=FORMAT,
                bbox_inches="tight")
    plt.close()

    for current_game in pca_data:
        mask = game_labels == current_game
        X_game_pca = X_pca_combined[mask]

        prompt_words_game = labels_all_prompt_word[mask]
        prompt_word_groups = sorted(set(prompt_words_game))
        fig, ax = plt.subplots(figsize=FIGSIZE)
        plot_grouped_pca(ax, X_game_pca, prompt_words_game, prompt_word_groups,
                         baseline_pca_combined, baseline_labels,
                         f"{current_game} (prompt words)", pca_combined)
        plt.tight_layout()
        plt.savefig(output_dir / f"pca_{current_game}_prompt_words.{FORMAT}",
                    format=FORMAT,
                    bbox_inches="tight")
        plt.close()

        base_models_game = sorted(set(labels_all_base_model[mask]))
        for base_model in base_models_game:
            model_mask = mask & (labels_all_base_model == base_model)
            X_model_pca = X_pca_combined[model_mask]
            prompt_words_model = labels_all_prompt_word[model_mask]
            model_groups = sorted(set(prompt_words_model))
            if len(model_groups) < 2:
                continue

            fig, ax = plt.subplots(figsize=FIGSIZE)
            plot_grouped_pca(
                ax,
                X_model_pca,
                prompt_words_model,
                model_groups,
                baseline_pca_combined,
                baseline_labels,
                f"{current_game} ({base_model}, prompt words)",
                pca_combined,
            )
            plt.tight_layout()
            safe_model = base_model.replace("/", "-")
            plt.savefig(output_dir /
                        f"pca_{current_game}_prompt_words_{safe_model}.{FORMAT}",
                        format=FORMAT,
                        bbox_inches="tight")
            plt.close()

    random_baseline_dist = compute_random_baseline_distance(X_all.shape[1])
    group_rows: list[dict] = []
    pair_rows: list[dict] = []

    for current_game in pca_data:
        mask = game_labels == current_game
        base_models_game = sorted(set(labels_all_base_model[mask]))

        for base_model in base_models_game:
            model_mask = mask & (labels_all_base_model == base_model)
            words_present = sorted(set(labels_all_prompt_word[model_mask]))

            for prompt_word in words_present:
                word_mask = model_mask & (labels_all_prompt_word == prompt_word)
                X_group = X_all[word_mask]
                if len(X_group) == 0:
                    continue
                family = labels_all_family[word_mask][0]
                mpd, mpd_norm = compute_within_set_metrics(X_group,
                                                           random_baseline_dist)
                pr = compute_participation_ratio(X_group)
                group_metrics = PromptGroupMetrics(
                    game=current_game,
                    base_model=base_model,
                    prompt_word=prompt_word,
                    family=family,
                    n_strategies=len(X_group),
                    mean_pairwise_distance=mpd,
                    mean_pairwise_distance_normalised=mpd_norm,
                    participation_ratio=pr,
                )
                group_rows.append(group_metrics.__dict__)

            family_to_words = {
                "collective": [word for word in COLLECTIVE_WORDS if word in words_present],
                "exploitative": [word for word in EXPLOITATIVE_WORDS if word in words_present],
            }

            for family, family_words in family_to_words.items():
                for word_a, word_b in combinations(family_words, 2):
                    mask_a = model_mask & (labels_all_prompt_word == word_a)
                    mask_b = model_mask & (labels_all_prompt_word == word_b)
                    X_a = X_all[mask_a]
                    X_b = X_all[mask_b]
                    if len(X_a) == 0 or len(X_b) == 0:
                        continue
                    centroid_distance, cohens_d = compute_between_set_metrics(
                        X_a, X_b)
                    pair_metrics = PromptPairMetrics(
                        game=current_game,
                        base_model=base_model,
                        family=family,
                        word_a=word_a,
                        word_b=word_b,
                        n_a=len(X_a),
                        n_b=len(X_b),
                        centroid_distance=centroid_distance,
                        cohens_d=cohens_d,
                    )
                    pair_rows.append(pair_metrics.__dict__)

    group_df = pd.DataFrame(group_rows, columns=GROUP_METRIC_COLUMNS)
    pair_df = pd.DataFrame(pair_rows, columns=PAIR_METRIC_COLUMNS)

    if not group_df.empty:
        group_df = group_df.sort_values(
            ["game", "base_model", "family", "prompt_word"])
    if not pair_df.empty:
        pair_df = pair_df.sort_values(
            ["game", "base_model", "family", "word_a", "word_b"])

    group_path = output_dir / "prompt_group_metrics.csv"
    pair_path = output_dir / "prompt_pair_metrics.csv"
    summary_path = output_dir / "prompt_sensitivity_summary.csv"
    table1_path = output_dir / "prompt_sensitivity_table1.csv"
    table1_wide_path = output_dir / "prompt_sensitivity_table1_wide.csv"
    group_df.to_csv(group_path, index=False)
    pair_df.to_csv(pair_path, index=False)
    summary_df = build_prompt_sensitivity_summary(group_df, pair_df)
    summary_df.to_csv(summary_path, index=False)
    summary_df.to_csv(table1_path, index=False)
    table1_wide_df = build_table1_style_wide(summary_df)
    table1_wide_df.to_csv(table1_wide_path, index=False)

    logger.info("Saved prompt group metrics to %s", group_path)
    logger.info("Saved prompt pair metrics to %s", pair_path)
    logger.info("Saved prompt sensitivity summary to %s", summary_path)
    logger.info("Saved Table-1-style prompt sensitivity summary to %s",
                table1_path)
    logger.info("Saved Table-1-style wide summary to %s", table1_wide_path)

    if not summary_df.empty:
        logger.info("Prompt sensitivity summary:")
        for _, row in summary_df.iterrows():
            logger.info(
                "%s/%s/%s/%s: MPD=%.3f (norm=%.2f), PR=%.2f, "
                "shift_from_%s centroid_dist=%s, Cohen's d=%s",
                row["game"],
                row["base_model"],
                row["family"],
                row["prompt_word"],
                row["mean_pairwise_distance"],
                row["mean_pairwise_distance_normalised"],
                row["participation_ratio"],
                row["canonical_prompt_word"],
                "NA" if pd.isna(row["shift_centroid_distance"]) else
                f"{row['shift_centroid_distance']:.3f}",
                "NA" if pd.isna(row["shift_cohens_d"]) else
                f"{row['shift_cohens_d']:.2f}",
            )

    if not pair_df.empty:
        logger.info("Prompt pair metrics:")
        for _, row in pair_df.iterrows():
            logger.info(
                "%s/%s/%s %s vs %s: centroid_dist=%.3f, Cohen's d=%.2f (n=%s,%s)",
                row["game"],
                row["base_model"],
                row["family"],
                row["word_a"],
                row["word_b"],
                row["centroid_distance"],
                row["cohens_d"],
                row["n_a"],
                row["n_b"],
            )


if __name__ == "__main__":
    main()
