"""Does an LLM given a strategy description reproduce its algorithmic implementation?

For each episode: sample a strategy uniformly from all attitudes for one
(game, model), verify the implementation is deterministic, sample a trajectory
of opponent cooperator-counts, play the algorithm against it, then ask the LLM
what it would do in each round — feeding it the ALGORITHM's past actions so the
paths cannot diverge. Each query is independent; no prior reasoning is carried.
"""
# pylint: disable=missing-function-docstring
import argparse
import ast
import hashlib
import json
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

from emergent_llm.common import Attitude, Gene
from emergent_llm.games import STANDARD_GENERATORS, get_game_type
from emergent_llm.generation import (
    FixedCooperatorCount,
    StrategyRegistry,
    make_fixed_opponents,
)
from emergent_llm.generation.create_strategies import (
    LLMConfig,
    get_llm_response,
    make_safe,
    parse_strategy_description_file,
    parse_strategy_description_file_raw,
)
from emergent_llm.generation.replication_prompts import (
    HISTORY_FORMATS,
    SOURCES,
    create_replication_system_prompt,
    create_replication_user_prompt,
)
from emergent_llm.players import LLMPlayer, SimplePlayer

sys.setrecursionlimit(10000)

ACTION_RE = re.compile(r"<action>\s*([CD])\s*</action>", re.IGNORECASE)
DETERMINATE_RE = re.compile(r"<determinate>\s*(yes|no)\s*</determinate>",
                            re.IGNORECASE)


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
                        choices=["minimal", "low", "medium", "high"])

    parser.add_argument("--source", default="description", choices=SOURCES,
                        help="Give the model the description or the code")
    parser.add_argument("--history_format", default="jsonl",
                        choices=HISTORY_FORMATS)
    parser.add_argument("--description_source", default="parsed",
                        choices=["parsed", "raw"],
                        help="'parsed' reproduces the backslash-escape "
                             "corruption the code generator also saw "
                             "(preserves parity); 'raw' recovers the model's "
                             "original text")
    parser.add_argument("--strip_docstring", action="store_true",
                        help="Drop class docstrings in --source code; they "
                             "can restate the attitude")
    parser.add_argument("--include_derived", action="store_true",
                        help="Add total_cooperators and cumulative aggregates")

    parser.add_argument("--n_episodes", type=int, default=30)
    parser.add_argument("--n_samples", type=int, default=1,
                        help="Queries per round; >1 gives a majority vote and "
                             "a self-consistency figure")
    parser.add_argument("--n_players", type=int, default=4)
    parser.add_argument("--n_rounds", type=int, default=7)
    parser.add_argument("--determinism_games", type=int, default=30)
    parser.add_argument("--skip_determinism_check", action="store_true")

    parser.add_argument("--strategies_dir", type=str, default="strategies")
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--no_cache", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max_retries", type=int, default=3)

    args = parser.parse_args()
    if args.inference_model is None:
        args.inference_model = args.strategy_model
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
               description_source: str = "parsed",
               need_source: bool = False,
               strip_docstring: bool = False) -> list[StrategyPair]:
    """Join `description_{ATTITUDE}_{n}` to `Strategy_{ATTITUDE}_{n}`."""
    safe_model = make_safe(model)
    game_dir = Path(strategies_dir) / game_name
    description_file = game_dir / f"{safe_model}_descriptions.py"
    strategy_file = game_dir / f"{safe_model}.py"

    parser = (parse_strategy_description_file_raw
              if description_source == "raw"
              else parse_strategy_description_file)
    descriptions = parser(description_file)
    if not descriptions:
        raise ValueError(f"No descriptions found in {description_file}")

    sources = (_strategy_sources(strategy_file, strip_docstring)
               if need_source else {})

    registry = StrategyRegistry(strategies_dir=Path(strategies_dir),
                                game_name=game_name, models=[model])

    pairs, unmatched = [], []
    for gene in sorted(registry.available_genes, key=str):
        for spec in registry.get_all_specs(gene):
            parts = spec.strategy_class.__name__.split("_")
            attitude_name, index = parts[1], int(parts[2])
            key = (attitude_name, index)
            if key not in descriptions:
                unmatched.append(spec.strategy_class.__name__)
                continue
            if need_source and spec.strategy_class.__name__ not in sources:
                unmatched.append(spec.strategy_class.__name__)
                continue
            pairs.append(StrategyPair(
                gene=spec.gene, index=index,
                description=descriptions[key].strip(),
                strategy_class=spec.strategy_class,
                source=sources.get(spec.strategy_class.__name__, "")))

    if unmatched:
        logging.warning("No description/source for %d implementations: %s",
                        len(unmatched), unmatched[:5])
    if not pairs:
        raise ValueError(f"No description/implementation pairs for {model}")
    return pairs

# =============================================================================
# DETERMINISM
# =============================================================================


def _actions_for_combo(strategy_class, gene, game_class, description,
                       opponents, n_games) -> set[tuple]:
    """Distinct action vectors over `n_games` runs. Fresh player and game each
    run, so state cannot leak via reset()."""
    seen = set()
    for _ in range(n_games):
        player = LLMPlayer("determinism", gene, description, strategy_class,
                           max_errors=0)
        result = game_class([player] + opponents, description).play_game()
        seen.add(tuple(bool(a) for a in result.history.actions[:, 0]))
        if len(seen) > 1:
            return seen
    return seen


def is_deterministic(strategy_class, gene, game_name: str, n_players: int,
                     n_rounds: int, n_games: int) -> bool:
    """Exhaustive over all opponent cooperator-count histories, two-stage.

    Checked directly per (combo, run) rather than via diversity.py's
    prefix-averaged features: at n_games=1 the length-(n_rounds-1) prefixes
    have a single sample each, so final-round stochasticity would be invisible.
    """
    game_class, _ = get_game_type(game_name)
    description = STANDARD_GENERATORS[game_name + "_default"](
        n_players=n_players, n_rounds=n_rounds)
    combos = list(make_fixed_opponents(n_players - 1, n_rounds))

    for stage_games in (2, n_games):
        for _, opponents in combos:
            if len(_actions_for_combo(strategy_class, gene, game_class,
                                      description, opponents,
                                      stage_games)) > 1:
                return False
        if stage_games >= n_games:
            break
    return True


class DeterminismCache:
    """class_name -> bool, keyed also on the game parameters."""

    def __init__(self, path: Path, enabled: bool):
        self.path, self.enabled = path, enabled
        self.data = {}
        if enabled and path.exists():
            with open(path, "rb") as handle:
                self.data = pickle.load(handle)

    def get(self, key):
        return self.data.get(key) if self.enabled else None

    def put(self, key, value):
        if not self.enabled:
            return
        self.data[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "wb") as handle:
            pickle.dump(self.data, handle)


# =============================================================================
# PLAYING THE ALGORITHM
# =============================================================================


def play_algorithm(pair: StrategyPair, game_name: str, description,
                   combo: tuple[int, ...]):
    """Run the implementation against one trajectory.

    Returns (my_actions, my_payoffs, opponent_cooperators) as full-length
    arrays; prompt histories are prefix slices of these. Opponents are
    non-reactive, so the prefixes are exactly what the strategy saw live.
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

    assert tuple(int(c) for c in opponent_cooperators[:len(combo)]) == combo, \
        "trajectory not reproduced by the game engine"
    return my_actions, my_payoffs, opponent_cooperators


# =============================================================================
# QUERYING
# =============================================================================


class PromptCache:
    """One JSON file per (prompt, model, source, sample). Crash-safe."""

    def __init__(self, directory: Path, enabled: bool):
        self.directory, self.enabled = directory, enabled
        if enabled:
            directory.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.directory / f"{key}.json"

    @staticmethod
    def key(*parts) -> str:
        return hashlib.sha256("\x00".join(map(str, parts)).encode()).hexdigest()

    def get(self, key):
        if not self.enabled or not self._path(key).exists():
            return None
        with open(self._path(key), encoding="utf-8") as handle:
            return json.load(handle)

    def put(self, key, value):
        if not self.enabled:
            return
        with open(self._path(key), "w", encoding="utf-8") as handle:
            json.dump(value, handle)


class QueryLogger:
    """Human-readable per-query log with real newlines."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = open(path, "a", encoding="utf-8")

    def write(self, header: dict, system_prompt: str, user_prompt: str,
              reasoning: str, native_reasoning: str, raw: str, note: str = ""):
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


def query_once(config, system_prompt, user_prompt, cache, cache_key):
    cached = cache.get(cache_key)
    if cached is not None:
        return cached, 0.0, True

    started = time.time()
    response = get_llm_response(config, system_prompt, user_prompt,
                                max_tokens=4096, thinking=True)
    payload = {"text": response.text, "reasoning": response.reasoning,
               "usage": response.usage}
    cache.put(cache_key, payload)
    return payload, time.time() - started, False


def parse_response(text: str) -> tuple[str, str]:
    action_matches = ACTION_RE.findall(text or "")
    if not action_matches:
        raise ParseFailure("no <action> tag")
    determinate_matches = DETERMINATE_RE.findall(text or "")
    determinate = (determinate_matches[-1].lower()
                   if determinate_matches else "missing")
    return action_matches[-1].upper(), determinate


def ask_round(config, args, cache, query_logger, header, system_prompt,
              user_prompt):
    """Returns (action, determinate, agreement, n_retries, latency, usage)."""
    votes, determinates, retries, latency, usage = [], [], 0, 0.0, None

    for sample in range(args.n_samples):
        for attempt in range(args.max_retries):
            cache_key = PromptCache.key(system_prompt, user_prompt,
                                        args.inference_model, args.source,
                                        sample, attempt)
            payload, elapsed, was_cached = query_once(
                config, system_prompt, user_prompt, cache, cache_key)
            latency += elapsed
            usage = payload.get("usage") or usage
            try:
                action, determinate = parse_response(payload["text"])
            except ParseFailure as failure:
                retries += 1
                query_logger.write({**header, "sample": sample,
                                    "attempt": attempt}, system_prompt,
                                   user_prompt, "", payload["reasoning"],
                                   payload["text"],
                                   note=f"PARSE FAILURE: {failure}")
                if attempt == args.max_retries - 1:
                    raise
                continue

            query_logger.write(
                {**header, "sample": sample, "attempt": attempt,
                 "llm_action": action, "determinate": determinate,
                 "cached": was_cached},
                system_prompt, user_prompt, "", payload["reasoning"],
                payload["text"])
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


def run_episode(episode: int, pair: StrategyPair, combo, args, config,
                description, cache, query_logger) -> pd.DataFrame:
    my_actions, my_payoffs, opponent_cooperators = play_algorithm(
        pair, args.game, description, combo)

    strategy_text = (pair.description if args.source == "description"
                     else pair.source)
    system_prompt = create_replication_system_prompt(args.source)

    rows = []
    for round_index in range(args.n_rounds):
        user_prompt = create_replication_user_prompt(
            game_name=args.game,
            game_description=description,
            strategy_text=strategy_text,
            source=args.source,
            my_actions=my_actions,
            my_payoffs=my_payoffs,
            opponent_cooperators=opponent_cooperators,
            n_played=round_index,
            history_format=args.history_format,
            include_derived=args.include_derived,
        )
        header = {
            "episode": episode, "game": args.game,
            "strategy_model": args.strategy_model,
            "inference_model": args.inference_model,
            "source": args.source, "gene": str(pair.gene),
            "strategy_class": pair.name, "trajectory": combo,
            "round": round_index,
            "algo_action": "C" if my_actions[round_index] else "D",
        }
        action, determinate, agreement, retries, latency, usage = ask_round(
            config, args, cache, query_logger, header, system_prompt,
            user_prompt)

        algo_action = "C" if my_actions[round_index] else "D"
        rows.append({
            "episode": episode,
            "game": args.game,
            "strategy_model": args.strategy_model,
            "inference_model": args.inference_model,
            "source": args.source,
            "history_format": args.history_format,
            "description_source": args.description_source,
            "include_derived": args.include_derived,
            "gene": str(pair.gene),
            "attitude": pair.gene.attitude.name,
            "strategy_class": pair.name,
            "trajectory": "".join(str(c) for c in combo),
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


def print_episode(episode: int, pair: StrategyPair, combo, frame: pd.DataFrame,
                  args):
    print("\n" + "=" * 79)
    print(f"EPISODE {episode}  |  {args.game}  |  source={args.source}  "
          f"|  {args.strategy_model} -> {args.inference_model}")
    print(f"gene:       {pair.gene}")
    print(f"strategy:   {pair.name}")
    print(f"trajectory: {combo}   (opponent cooperators, rounds 1..n-1)")
    print("-" * 79)
    print("STRATEGY DESCRIPTION")
    print(pair.description)
    print("-" * 79)
    columns = ["round", "opp_coops_prev", "algo", "llm", "match",
               "determinate", "agreement"]
    with pd.option_context("display.width", 200):
        print(frame[columns].to_string(index=False))
    matched = int(frame["match"].sum())
    print(f"\naccuracy: {matched}/{len(frame)} = "
          f"{matched / len(frame):.1%}")
    print("=" * 79)


# =============================================================================
# MAIN
# =============================================================================


def main():
    args = parse_arguments()
    rng = random.Random(args.seed)

    output_dir = (Path(args.results_dir) / "replication" / args.game /
                  make_safe(args.strategy_model) /
                  f"{args.source}_{args.history_format}"
                  f"_{args.description_source}"
                  f"{'_derived' if args.include_derived else ''}"
                  f"{'_nodoc' if args.strip_docstring else ''}")
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(output_dir / "run.log"),
                  logging.StreamHandler()])
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)

    config = LLMConfig(create_client(args.llm_provider), args.inference_model,
                       reasoning_effort=args.reasoning_effort)
    description = STANDARD_GENERATORS[args.game + "_default"](
        n_players=args.n_players, n_rounds=args.n_rounds)

    pairs = load_pairs(Path(args.strategies_dir), args.game,
                       args.strategy_model,
                       description_source=args.description_source,
                       need_source=(args.source == "code"),
                       strip_docstring=args.strip_docstring)
    logging.info("Loaded %d description/implementation pairs across %d genes",
                 len(pairs), len({p.gene for p in pairs}))

    cache = PromptCache(output_dir / "prompt_cache", not args.no_cache)
    determinism_cache = DeterminismCache(
        output_dir.parent / "determinism_cache.pkl", not args.no_cache)
    query_logger = QueryLogger(output_dir / "queries.log")

    frames, rejected, discarded, attempts = [], 0, 0, 0
    max_attempts = 3 * args.n_episodes + 10

    while len(frames) < args.n_episodes and attempts < max_attempts:
        attempts += 1
        pair = pairs[rng.randrange(len(pairs))]

        if not args.skip_determinism_check:
            key = (pair.name, args.n_players, args.n_rounds,
                   args.determinism_games)
            verdict = determinism_cache.get(key)
            if verdict is None:
                logging.info("Determinism check: %s", pair.name)
                verdict = is_deterministic(pair.strategy_class, pair.gene,
                                           args.game, args.n_players,
                                           args.n_rounds,
                                           args.determinism_games)
                determinism_cache.put(key, verdict)
            if not verdict:
                rejected += 1
                logging.info("Rejected %s (stochastic)", pair.name)
                continue

        combo = tuple(rng.randrange(args.n_players)
                      for _ in range(args.n_rounds - 1))
        episode = len(frames) + 1

        try:
            frame = run_episode(episode, pair, combo, args, config,
                                description, cache, query_logger)
        except ParseFailure as failure:
            discarded += 1
            logging.warning("Discarded episode (%s / %s): %s",
                            pair.name, combo, failure)
            continue

        frames.append(frame)
        print_episode(episode, pair, combo, frame, args)

    query_logger.close()

    if not frames:
        logging.error("No episodes completed after %d attempts", attempts)
        return

    results = pd.concat(frames, ignore_index=True)
    results.to_csv(output_dir / "results.csv", index=False)

    print("\n" + "=" * 79)
    print(f"SUMMARY  ({len(frames)} episodes, {len(results)} decisions)")
    print(f"attempts: {attempts}   rejected (stochastic): {rejected}   "
          f"discarded (parse): {discarded}")
    print("-" * 79)
    print("Overall accuracy: "
          f"{results['match'].mean():.1%}")
    print(f"Algorithm C-rate: {(results['algo'] == 'C').mean():.1%}   "
          f"LLM C-rate: {(results['llm'] == 'C').mean():.1%}")
    print("\nBy round:")
    print(results.groupby("round")["match"].agg(["mean", "count"]).to_string())
    print("\nBy determinacy:")
    print(results.groupby("determinate")["match"]
          .agg(["mean", "count"]).to_string())
    print("\nConfusion (rows algo, cols llm):")
    print(pd.crosstab(results["algo"], results["llm"]).to_string())
    print(f"\nWrote {output_dir / 'results.csv'}")
    print(f"Wrote {output_dir / 'queries.log'}")
    print("=" * 79)


if __name__ == "__main__":
    main()
