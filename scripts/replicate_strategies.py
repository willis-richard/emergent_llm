"""Does an LLM given a strategy description reproduce its algorithmic implementation?

For each episode: sample a strategy uniformly from all attitudes for one
(game, model), sample a trajectory of opponent cooperator-counts, play the
algorithm against it, then ask the LLM what it would do in each round — feeding
it the ALGORITHM's past actions so the paths cannot diverge. Each query is
independent; no prior reasoning is carried.

Both conditions (`description` and `code`) run against the same episode plan, so
their rows are paired on (strategy_class, trajectory, round) and divergences can
be read off directly. Round labels differ by condition — 1-based for
descriptions, 0-based for code — because the descriptions were generated against
the old 1-based convention. This is a known, unavoidable confound.

Strategies must be proved deterministic by a prior diversity.py sweep at exactly
these parameters; there is no live determinism check and no fallback.

Results are appended per episode, so an aborted run resumes by re-running with
the same --seed and output directory.
"""
# pylint: disable=missing-function-docstring,broad-except
import argparse
import ast
import logging
import os
import pickle
import random
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import anthropic
import numpy as np
import ollama
import openai
import pandas as pd
from google import genai

from emergent_llm.common import Gene
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import FixedCooperatorCount, StrategyRegistry
from emergent_llm.generation.create_strategies import (
    LLMConfig,
    get_llm_response,
    make_safe,
    parse_strategy_description_file,
    EFFORT_LEVELS,
)
from emergent_llm.generation.replication_prompts import (
    HISTORY_FORMATS,
    SOURCES,
    create_replication_system_prompt,
    create_replication_user_prompt,
)
from emergent_llm.players import LLMPlayer, SimplePlayer

# Generated strategies occasionally recurse deeply.
sys.setrecursionlimit(10000)

ACTION_RE = re.compile(r"<action>\s*([CD])\s*</action>", re.IGNORECASE)
DETERMINATE_RE = re.compile(r"<determinate>\s*(yes|no)\s*</determinate>",
                            re.IGNORECASE)
CLASS_NAME_RE = re.compile(r"^Strategy_([A-Z_]+)_(\d+)$")

EPISODE_KEYS = ["strategy_class", "trajectory"]
TAGS = {"description": "desc", "code": "code"}


class ParseFailure(Exception):
    """Model output could not be parsed after all retries."""


@dataclass
class StrategyPair:
    gene: Gene
    index: int
    description: str
    strategy_class: type
    source: str = ""

    @property
    def name(self) -> str:
        return self.strategy_class.__name__

    def text_for(self, source: str) -> str:
        return self.description if source == "description" else self.source


def trajectory_key(combo) -> str:
    """Separator matters: counts reach 10+ once n_players > 10."""
    return "-".join(str(c) for c in combo)


# =============================================================================
# ARGUMENTS
# =============================================================================


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--game", default="public_goods",
                        choices=["public_goods", "collective_risk"],
                        help="common_pool is unsupported: it exposes stock to "
                             "strategies, which this harness does not render")
    parser.add_argument("--strategy_model", required=True,
                        help="Model whose strategies/descriptions are loaded")
    parser.add_argument("--inference_model", default=None,
                        help="Model queried round-by-round (default: "
                             "--strategy_model)")
    parser.add_argument("--llm_provider", required=True,
                        choices=["openai", "anthropic", "ollama", "google",
                                 "openrouter"])
    parser.add_argument("--reasoning_effort", default="medium",
                        choices=list(EFFORT_LEVELS))

    parser.add_argument("--sources", nargs="+", default=list(SOURCES),
                        choices=SOURCES,
                        help="Conditions run per episode. Both by default; "
                             "each sees the same strategy and trajectory, so "
                             "the rows are paired.")
    parser.add_argument("--history_format", default="jsonl",
                        choices=HISTORY_FORMATS)
    parser.add_argument("--description_source", default="parsed",
                        choices=["parsed", "raw"],
                        help="'parsed' reproduces the backslash-escape "
                             "corruption the code generator also saw "
                             "(preserves parity); 'raw' recovers the model's "
                             "original text")
    parser.add_argument("--strip_docstring", action="store_true",
                        help="Drop class docstrings in the code condition; "
                             "they can restate the attitude")
    parser.add_argument("--include_derived", action="store_true",
                        help="Add total_cooperators and cumulative aggregates")

    parser.add_argument("--n_episodes", type=int, default=30)
    parser.add_argument("--n_samples", type=int, default=1,
                        help="Queries per round; >1 gives a majority vote and "
                             "a self-consistency figure")
    parser.add_argument("--n_players", type=int, default=4)
    parser.add_argument("--n_rounds", type=int, default=7)
    parser.add_argument("--diversity_games", type=int, default=30,
                        help="Selects which diversity.py cache to require: "
                             "results/diversity/cache/{game}_{gene}"
                             "_p{n_players}_r{n_rounds}_g{diversity_games}.pkl")

    parser.add_argument("--strategies_dir", type=str, default="strategies")
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max_retries", type=int, default=3)

    args = parser.parse_args()
    if args.inference_model is None:
        args.inference_model = args.strategy_model
    if args.n_samples < 1 or args.max_retries < 1:
        parser.error("--n_samples and --max_retries must be >= 1")
    # Fixed order so column layout and logs are stable.
    args.sources = [s for s in SOURCES if s in args.sources]
    return args


def create_client(provider: str):
    if provider == "openai":
        return openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    if provider == "anthropic":
        return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    if provider == "ollama":
        return ollama.Client(host=os.environ["OLLAMA_HOST"])
    if provider == "openrouter":
        return openai.OpenAI(base_url="https://openrouter.ai/api/v1",
                             api_key=os.environ["OPENROUTER_API_KEY"])
    if provider == "google":
        return genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    raise ValueError(f"Unknown provider {provider}")


# =============================================================================
# LOGGING
# =============================================================================


class Report:
    """Human-facing narrative: stdout and report.log. No API payloads."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = open(path, "a", encoding="utf-8")

    def __call__(self, text: str = ""):
        print(text)
        self.handle.write(text + "\n")
        self.handle.flush()

    def close(self):
        self.handle.close()


class QueryLogger:
    """Every API call, with real newlines."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = open(path, "a", encoding="utf-8")

    def write(self, header: dict, system_prompt: str, user_prompt: str,
              native_reasoning: str, raw: str, note: str = ""):
        rule = "=" * 79
        self.handle.write(f"\n{rule}\n")
        for key, value in header.items():
            self.handle.write(f"{key}: {value}\n")
        if note:
            self.handle.write(f"note: {note}\n")
        for title, body in (("SYSTEM PROMPT", system_prompt),
                            ("USER PROMPT", user_prompt),
                            ("NATIVE REASONING", native_reasoning),
                            ("VISIBLE RESPONSE", raw)):
            self.handle.write(f"\n{'-' * 79}\n{title}\n{'-' * 79}\n")
            self.handle.write((body or "(none)") + "\n")
        self.handle.write(f"{rule}\n")
        self.handle.flush()

    def close(self):
        self.handle.close()


# =============================================================================
# LOADING: pair each description with its implementation
# =============================================================================


def _strategy_sources(strategy_file: Path,
                      strip_docstring: bool) -> dict[str, str]:
    """Map stored class name -> source text, each renamed to `Strategy`.

    Read from disk rather than via `inspect.getsource`: `StrategyRegistry`
    execs strategy modules without registering them in `sys.modules`, so
    `inspect.getfile` raises "is a built-in class".

    The rename matters — stored names are `Strategy_COLLECTIVE_37` and would
    leak the attitude, which the description condition never sees.

    `ast.unparse` is lossless here: `write_strategy_class` produced these files
    with `ast.unparse`, so the stored text is already in that normal form.
    """
    tree = ast.parse(strategy_file.read_text(encoding="utf-8"))
    sources = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        stored_name = node.name
        node.name = "Strategy"

        if strip_docstring:
            first = node.body[0] if node.body else None
            if (isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                node.body.pop(0)
                if not node.body:
                    node.body.append(ast.Pass())

        source = ast.unparse(node)

        # Renaming the definition does not rewrite references in the body.
        if stored_name in source:
            logging.warning("%s hardcodes its own class name; scrubbing",
                            stored_name)
            source = source.replace(stored_name, "Strategy")

        sources[stored_name] = source

    return sources


def load_pairs(strategies_dir: Path, game_name: str, model: str,
               need_source: bool = False,
               strip_docstring: bool = False) -> list[StrategyPair]:
    """Join `description_{ATTITUDE}_{n}` to `Strategy_{ATTITUDE}_{n}`."""
    safe_model = make_safe(model)
    game_dir = Path(strategies_dir) / game_name
    description_file = game_dir / f"{safe_model}_descriptions.py"
    strategy_file = game_dir / f"{safe_model}.py"

    descriptions = parse_strategy_description_file(description_file)
    if not descriptions:
        raise ValueError(f"No descriptions found in {description_file}")

    sources = (_strategy_sources(strategy_file, strip_docstring)
               if need_source else {})

    registry = StrategyRegistry(strategies_dir=Path(strategies_dir),
                                game_name=game_name, models=[model])

    pairs, unmatched = [], []
    for gene in sorted(registry.available_genes, key=str):
        for spec in registry.get_all_specs(gene):
            class_name = spec.strategy_class.__name__
            match = CLASS_NAME_RE.match(class_name)
            if match is None:
                unmatched.append(class_name)
                continue
            key = (match.group(1), int(match.group(2)))
            if key not in descriptions:
                unmatched.append(class_name)
                continue
            if need_source and class_name not in sources:
                unmatched.append(class_name)
                continue
            pairs.append(StrategyPair(
                gene=spec.gene, index=key[1],
                description=descriptions[key].strip(),
                strategy_class=spec.strategy_class,
                source=sources.get(class_name, "")))

    if unmatched:
        logging.warning("No description/source for %d implementations: %s",
                        len(unmatched), unmatched[:5])
    if not pairs:
        raise ValueError(f"No description/implementation pairs for {model}")
    return pairs


# =============================================================================
# DETERMINISM (from diversity.py's sweep; nothing is computed here)
# =============================================================================


def _deterministic_from_features(features: dict) -> bool:
    """A strategy is deterministic iff every stored mean is exactly 0 or 1.

    diversity.py keys each feature on `combo[:r]` and stores the mean round-r
    action over n_games runs and over every combo sharing that prefix. Round r
    can only depend on opponent counts from rounds 0..r-1, i.e. on the key
    itself, so under determinism every summand is identical and the mean is
    exactly 0.0 or 1.0. Sums of exact 0.0/1.0 divide exactly, so no tolerance
    is needed.
    """
    return all(value in (0.0, 1.0) for value in features.values())


def load_diversity_verdicts(results_dir: Path, game_name: str, genes,
                            n_players: int, n_rounds: int, n_games: int,
                            report) -> dict[str, bool]:
    """Reuse diversity.py's exhaustive sweep as a determinism oracle.

    Exact parameters only: the filename must be
    `{game}_{gene}_p{n_players}_r{n_rounds}_g{n_games}.pkl`. A sweep at other
    p/r says nothing about this geometry — endgame logic keyed on n_rounds is
    invisible at a shorter horizon — and a different g is a different strength
    of evidence. Files with an `_s{n}` suffix cover only the first n strategies
    per gene and are never built, so they are never read.

    Caveat: diversity.py builds players with the default max_errors=2, so a
    strategy that raises has its exception swallowed and replaced by a
    deterministic attitude-based fallback. Such a strategy looks deterministic
    here and then raises under max_errors=0 in play_algorithm; the episode is
    discarded and logged rather than trusted.
    """
    cache_dir = Path(results_dir) / "diversity" / "cache"
    verdicts, used = {}, []

    if cache_dir.is_dir():
        for gene in genes:
            path = cache_dir / (f"{game_name}_{gene}_p{n_players}_r{n_rounds}"
                                f"_g{n_games}.pkl")
            if not path.exists():
                continue
            try:
                with open(path, "rb") as handle:
                    features = pickle.load(handle)
            except Exception as error:
                logging.warning("Could not read %s: %s: %s", path.name,
                                type(error).__name__, error)
                continue
            for class_name, feature_dict in features.items():
                verdicts[class_name] = _deterministic_from_features(feature_dict)
            used.append(f"{path.name} ({len(features)} strategies)")

    if used:
        report(f"Diversity cache: {len(verdicts)} verdicts "
               f"({sum(verdicts.values())} deterministic) from {len(used)} "
               f"files")
        for name in used:
            logging.info("  %s", name)
        return verdicts

    others = (sorted(p.name for p in cache_dir.glob("*.pkl")
                     if p.name.startswith(f"{game_name}_"))
              if cache_dir.is_dir() else [])
    for name in others:
        logging.info("ignored (wrong parameters): %s", name)
    raise FileNotFoundError(
        f"No diversity cache at p{n_players}_r{n_rounds}_g{n_games} for "
        f"{game_name}. {len(others)} file(s) exist for this game at other "
        f"parameters and were ignored; see run.log. Run diversity.py with "
        f"--n_players {n_players} --n_rounds {n_rounds} --n_games {n_games} "
        f"and no --n_strategies.")


def select_deterministic(pairs, verdicts, report):
    """Keep only the strategies the diversity sweep proved deterministic.

    There is no live fallback: a strategy absent from the cache cannot be
    screened, so it is excluded rather than assumed safe.
    """
    kept, stochastic, unknown = [], [], []
    for pair in pairs:
        verdict = verdicts.get(pair.name)
        if verdict is None:
            unknown.append(pair.name)
        elif verdict:
            kept.append(pair)
        else:
            stochastic.append(pair.name)

    report(f"Deterministic: {len(kept)}/{len(pairs)} strategies "
           f"({len(stochastic)} stochastic, {len(unknown)} absent from cache)")
    if unknown:
        logging.warning("Absent from diversity cache (%d): %s",
                        len(unknown), unknown[:5])
    if not kept:
        raise ValueError("No deterministic strategies to sample from")
    return kept, len(stochastic), len(unknown)


# =============================================================================
# PLAYING THE ALGORITHM
# =============================================================================


def play_algorithm(pair: StrategyPair, game_name: str, description,
                   combo: tuple[int, ...]):
    """Run the implementation against one trajectory.

    Returns (my_actions, my_payoffs, opponent_cooperators) as full-length
    arrays; prompt histories are prefix slices of these. Opponents are
    non-reactive, so the prefixes are exactly what the strategy saw live.

    Called once per episode and shared by every source condition, so the
    conditions are guaranteed to see byte-identical histories.
    """
    game_class, _ = get_game_type(game_name)
    n_opponents = description.n_players - 1
    counts = list(combo) + [0]  # final round's opponent actions are unused
    opponents = [SimplePlayer(f"opp_{i}", FixedCooperatorCount(i, counts))
                 for i in range(n_opponents)]

    player = LLMPlayer("focal", pair.gene, description, pair.strategy_class,
                       max_errors=0)
    history = game_class([player] + opponents, description).play_game().history

    my_actions = history.actions[:, 0]
    my_payoffs = history.payoffs[:, 0]
    opponent_cooperators = (history.actions.sum(axis=1)
                            - history.actions[:, 0].astype(np.int_))

    if tuple(int(c) for c in opponent_cooperators[:len(combo)]) != combo:
        raise RuntimeError("trajectory not reproduced by the game engine")
    return my_actions, my_payoffs, opponent_cooperators


# =============================================================================
# QUERYING
# =============================================================================


def parse_response(text: str) -> tuple[str, str]:
    action_matches = ACTION_RE.findall(text or "")
    if not action_matches:
        raise ParseFailure("no <action> tag")
    determinate_matches = DETERMINATE_RE.findall(text or "")
    determinate = (determinate_matches[-1].lower()
                   if determinate_matches else "missing")
    return action_matches[-1].upper(), determinate


def ask_round(config, args, query_logger, header, system_prompt, user_prompt):
    """Returns (action, determinate, agreement, n_retries, latency, usage)."""
    votes, determinates, retries, latency, usage = [], [], 0, 0.0, None

    for sample in range(args.n_samples):
        for attempt in range(args.max_retries):
            started = time.time()
            response = get_llm_response(config, system_prompt, user_prompt,
                                        thinking=True)
            latency += time.time() - started
            usage = response.usage or usage

            try:
                action, determinate = parse_response(response.text)
            except ParseFailure as failure:
                retries += 1
                query_logger.write({**header, "sample": sample,
                                    "attempt": attempt}, system_prompt,
                                   user_prompt, response.reasoning,
                                   response.text,
                                   note=f"PARSE FAILURE: {failure}")
                if attempt == args.max_retries - 1:
                    raise
                continue

            query_logger.write(
                {**header, "sample": sample, "attempt": attempt,
                 "llm_action": action, "determinate": determinate},
                system_prompt, user_prompt, response.reasoning, response.text)
            votes.append(action)
            determinates.append(determinate)
            break

    modal_action, modal_count = Counter(votes).most_common(1)[0]
    return (modal_action,
            Counter(determinates).most_common(1)[0][0],
            modal_count / len(votes),
            retries, latency, usage)


# =============================================================================
# EPISODE
# =============================================================================


def run_episode(episode: int, pair: StrategyPair, combo, source: str, args,
                config, description, played, query_logger) -> pd.DataFrame:
    my_actions, my_payoffs, opponent_cooperators = played
    strategy_text = pair.text_for(source)
    system_prompt = create_replication_system_prompt(source)
    trajectory = trajectory_key(combo)

    rows = []
    for round_index in range(args.n_rounds):
        user_prompt = create_replication_user_prompt(
            game_name=args.game,
            game_description=description,
            strategy_text=strategy_text,
            source=source,
            my_actions=my_actions,
            my_payoffs=my_payoffs,
            opponent_cooperators=opponent_cooperators,
            n_played=round_index,
            history_format=args.history_format,
            include_derived=args.include_derived,
        )
        algo_action = "C" if my_actions[round_index] else "D"
        header = {
            "episode": episode, "game": args.game,
            "strategy_model": args.strategy_model,
            "inference_model": args.inference_model,
            "source": source, "gene": str(pair.gene),
            "strategy_class": pair.name, "trajectory": trajectory,
            "round": round_index, "algo_action": algo_action,
        }
        action, determinate, agreement, retries, latency, usage = ask_round(
            config, args, query_logger, header, system_prompt, user_prompt)

        rows.append({
            "episode": episode,
            "game": args.game,
            "strategy_model": args.strategy_model,
            "inference_model": args.inference_model,
            "source": source,
            "history_format": args.history_format,
            "include_derived": args.include_derived,
            "gene": str(pair.gene),
            "attitude": pair.gene.attitude.name,
            "strategy_class": pair.name,
            "trajectory": trajectory,
            "round": round_index,
            "opp_coops_prev": (int(opponent_cooperators[round_index - 1])
                               if round_index else None),
            "algo": algo_action,
            "llm": action,
            "match": action == algo_action,
            "determinate": determinate,
            "agreement": agreement,
            "n_retries": retries,
            "latency_s": round(latency, 2),
            "input_tokens": (usage or {}).get("input_tokens"),
            "output_tokens": (usage or {}).get("output_tokens"),
        })

    return pd.DataFrame(rows)


def print_episode(episode: int, pair: StrategyPair, combo,
                  frames: dict[str, pd.DataFrame], args, report: Report):
    order = [s for s in SOURCES if s in frames]

    report("\n" + "=" * 79)
    report(f"EPISODE {episode}  |  {args.game}  |  "
           f"{args.strategy_model} -> {args.inference_model}")
    report(f"gene:       {pair.gene}")
    report(f"strategy:   {pair.name}")
    report(f"trajectory: {trajectory_key(combo)}   "
           f"(opponent cooperators, rounds 1..n-1)")

    for source in order:
        report("-" * 79)
        report(f"TEXT SHOWN TO THE MODEL — {source}")
        report(pair.text_for(source))

    report("-" * 79)
    table = frames[order[0]][["round", "opp_coops_prev", "algo"]].copy()
    for source in order:
        indexed = frames[source].set_index("round")
        tag = TAGS[source]
        table[f"llm_{tag}"] = table["round"].map(indexed["llm"])
        table[f"ok_{tag}"] = table["round"].map(indexed["match"])
        table[f"det_{tag}"] = table["round"].map(indexed["determinate"])
    with pd.option_context("display.width", 200):
        report(table.to_string(index=False))

    report("")
    for source in order:
        frame = frames[source]
        matched = int(frame["match"].astype(bool).sum())
        report(f"{source:>12} accuracy: {matched}/{len(frame)} = "
               f"{matched / len(frame):.1%}")
    if len(order) == 2:
        left, right = (frames[s].set_index("round")["llm"] for s in order)
        report(f"{'divergence':>12}: {int((left != right).sum())}/{len(left)} "
               f"rounds where the conditions disagree")
    report("=" * 79)


# =============================================================================
# CHECKPOINTING
# =============================================================================


def load_partial(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, dtype={"trajectory": str, "gene": str})


def append_rows(frame: pd.DataFrame, path: Path):
    frame.to_csv(path, mode="a", header=not path.exists(), index=False)


# =============================================================================
# PLAN
# =============================================================================


def build_plan(pairs, args, rng, report):
    """(pair, combo) per episode. Fixed by --seed, so a resumed run continues
    the identical sequence without any RNG state on disk."""
    plan, seen, attempts = [], set(), 0
    max_attempts = 10 * args.n_episodes + 50

    while len(plan) < args.n_episodes and attempts < max_attempts:
        attempts += 1
        pair = pairs[rng.randrange(len(pairs))]
        combo = tuple(rng.randrange(args.n_players)
                      for _ in range(args.n_rounds - 1))
        if (pair.name, combo) in seen:
            continue
        seen.add((pair.name, combo))
        plan.append((pair, combo))

    if len(plan) < args.n_episodes:
        report(f"WARNING: planned {len(plan)}/{args.n_episodes} episodes "
               f"after {attempts} attempts")
    return plan


# =============================================================================
# SUMMARY
# =============================================================================


def print_summary(results: pd.DataFrame, n_stochastic: int, n_unknown: int,
                  discarded: int, results_path: Path, report: Report):
    results = results.copy()
    results["match"] = results["match"].astype(bool)
    fmt = lambda v: f"{v:.3f}"  # noqa: E731

    report("\n" + "=" * 79)
    report(f"SUMMARY  ({results.groupby(EPISODE_KEYS).ngroups} episodes, "
           f"{len(results)} decisions)")
    report(f"excluded: {n_stochastic} stochastic, {n_unknown} uncached   "
           f"discarded (error): {discarded}")

    report("-" * 79)
    report("PER CONDITION")
    per_source = []
    for source, frame in results.groupby("source"):
        trajectories = frame.groupby(EPISODE_KEYS)["match"].all()
        per_source.append({
            "source": source,
            "episodes": len(trajectories),
            "decisions": len(frame),
            "action_match": frame["match"].mean(),
            "trajectory_match": trajectories.mean(),
            "algo_C": (frame["algo"] == "C").mean(),
            "llm_C": (frame["llm"] == "C").mean(),
        })
    report(pd.DataFrame(per_source).to_string(index=False, float_format=fmt))

    report("\nAction match by round:")
    report(results.pivot_table(index="round", columns="source",
                               values="match", aggfunc="mean")
           .to_string(float_format=fmt))

    report("\nAction match by self-reported determinacy:")
    report(results.pivot_table(index="determinate", columns="source",
                               values="match", aggfunc=["mean", "size"])
           .to_string(float_format=fmt))

    report("\nConfusion (rows algo, cols llm):")
    report(pd.crosstab([results["source"], results["algo"]],
                       results["llm"]).to_string())

    if results["source"].nunique() > 1:
        wide = (results.pivot_table(
            index=EPISODE_KEYS + ["round", "algo"], columns="source",
            values="llm", aggfunc="first").dropna().reset_index())
        report("-" * 79)
        report(f"PAIRED  ({len(wide)} decisions present in both conditions)")
        report("conditions agree with each other: "
               f"{(wide['description'] == wide['code']).mean():.1%}")
        report("\nCorrectness cross-tab:")
        report(pd.crosstab(wide["description"] == wide["algo"],
                           wide["code"] == wide["algo"],
                           rownames=["description correct"],
                           colnames=["code correct"]).to_string())

    ranking = results.assign(error=~results["match"]).pivot_table(
        index="strategy_class", columns="source", values="error",
        aggfunc="sum", fill_value=0)
    ranking.columns = [f"errors_{c}" for c in ranking.columns]
    ranking["errors_total"] = ranking.sum(axis=1)
    ranking = ranking.join(
        results.groupby("strategy_class").size().rename("decisions"))
    ranking["error_rate"] = ranking["errors_total"] / ranking["decisions"]
    ranking = ranking.sort_values(["errors_total", "error_rate"],
                                  ascending=False)
    report("-" * 79)
    report("STRATEGIES BY DESCENDING ERRORS")
    report(ranking.to_string(float_format=fmt))

    report(f"\nWrote {results_path}")
    report("=" * 79)


# =============================================================================
# MAIN
# =============================================================================


def main():
    args = parse_arguments()
    rng = random.Random(args.seed)

    model_dir = (Path(args.results_dir) / "replication" / args.game /
                 make_safe(args.strategy_model))
    output_dir = (model_dir / make_safe(args.inference_model) /
                  f"n{args.n_players}x{args.n_rounds}_g{args.diversity_games}"
                  f"_{args.history_format}"
                  f"_{args.reasoning_effort}_seed{args.seed}"
                  f"{'_derived' if args.include_derived else ''}"
                  f"{'_nodoc' if args.strip_docstring else ''}")
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(output_dir / "run.log"),
                  logging.StreamHandler()])
    for noisy in ("httpx", "openai._base_client", "anthropic"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    report = Report(output_dir / "report.log")
    query_logger = QueryLogger(output_dir / "queries.log")

    config = LLMConfig(create_client(args.llm_provider), args.inference_model,
                       reasoning_effort=args.reasoning_effort)
    description = STANDARD_GENERATORS[args.game + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    pairs = load_pairs(Path(args.strategies_dir), args.game,
                       args.strategy_model,
                       need_source=("code" in args.sources),
                       strip_docstring=args.strip_docstring)
    logging.info("Loaded %d description/implementation pairs across %d genes",
                 len(pairs), len({p.gene for p in pairs}))

    verdicts = load_diversity_verdicts(
        Path(args.results_dir), args.game,
        sorted({p.gene for p in pairs}, key=str),
        args.n_players, args.n_rounds, args.diversity_games, report)
    pairs, n_stochastic, n_unknown = select_deterministic(pairs, verdicts,
                                                          report)

    results_path = output_dir / "results.csv"
    done = load_partial(results_path)
    completed = (set(zip(done["strategy_class"], done["trajectory"],
                         done["source"])) if not done.empty else set())
    if completed:
        report(f"Resuming: {len(completed)} episode-conditions already in "
               f"{results_path}")

    plan = build_plan(pairs, args, rng, report)

    discarded = 0
    for episode, (pair, combo) in enumerate(plan, 1):
        trajectory = trajectory_key(combo)
        pending = [s for s in args.sources
                   if (pair.name, trajectory, s) not in completed]
        if not pending:
            continue

        frames = {
            source: done[(done["strategy_class"] == pair.name)
                         & (done["trajectory"] == trajectory)
                         & (done["source"] == source)]
            for source in args.sources if source not in pending
        }

        try:
            played = play_algorithm(pair, args.game, description, combo)
            for source in pending:
                frames[source] = run_episode(
                    episode, pair, combo, source, args, config, description,
                    played, query_logger)
        except Exception as failure:
            # One broken strategy or one unparseable response must not kill the
            # run. Written all-or-nothing so paired rows are never half-present;
            # with no prompt cache, a discard re-pays for the completed half.
            discarded += 1
            logging.warning("Discarded episode %d (%s / %s): %s: %s",
                            episode, pair.name, trajectory,
                            type(failure).__name__, failure)
            continue

        for source in pending:
            append_rows(frames[source], results_path)
        print_episode(episode, pair, combo, frames, args, report)

    query_logger.close()

    results = load_partial(results_path)
    if results.empty:
        report("No episodes completed.")
    else:
        print_summary(results, n_stochastic, n_unknown, discarded,
                      results_path, report)
    report.close()


if __name__ == "__main__":
    main()
