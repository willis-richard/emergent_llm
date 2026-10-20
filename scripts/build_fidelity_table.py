"""Build the policy-fidelity LaTeX table from replicate_strategies.py output.

Reads results/replication/{game}/{model}/{model}/{run}/results.csv for every
(game, model) and writes one table: rows are model x condition, columns are
action match and trajectory match per game. Missing runs print as '--'.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

GAMES = {"public_goods": "Public Goods",
         "collective_risk": "Collective Risk",
         "common_pool": "Common Pool"}
MODELS = {"claude-haiku-4-5": "Claude Haiku 4.5",
          "gemini-3.1-flash-lite-preview": "Gemini 3.1 Flash Lite",
          "gpt-5.4-mini": "GPT-5.4 Mini"}
SOURCES = {"code": "code", "description": "description"}
EPISODE_KEYS = ["strategy_class", "trajectory"]


def summarise(path: Path) -> dict[str, tuple[float, float, int]]:
    """source -> (action match, trajectory match, n episodes)."""
    frame = pd.read_csv(path, dtype={"trajectory": str})
    frame["match"] = frame["match"].astype(bool)
    out = {}
    for source, group in frame.groupby("source"):
        trajectories = group.groupby(EPISODE_KEYS)["match"].all()
        out[source] = (group["match"].mean(), trajectories.mean(),
                       len(trajectories))
    return out


def pct(value: float, decimals: int) -> str:
    text = f"{100 * value:.{decimals}f}"
    if decimals and text.endswith("." + "0" * decimals):
        text = text.split(".")[0]
    return text + r"\%"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results_dir", default="results")
    parser.add_argument("--run", default="n4x7_g30_jsonl_medium_seed0",
                        help="Run subdirectory written by replicate_strategies")
    parser.add_argument("--output", default=None,
                        help="Default: {results_dir}/replication/fidelity.tex")
    args = parser.parse_args()

    root = Path(args.results_dir) / "replication"
    stats = {}
    for game in GAMES:
        for model in MODELS:
            path = root / game / model / model / args.run / "results.csv"
            if path.exists():
                stats[game, model] = summarise(path)
            else:
                print(f"missing: {path}", file=sys.stderr)

    for (game, model), by_source in stats.items():
        for source, (_, _, n) in by_source.items():
            if n != 100:
                print(f"note: {game} {model} {source}: {n} episodes",
                      file=sys.stderr)

    lines = [
        r"\begin{table}[h]",
        r"\caption{Agreement between each model acting round-by-round and the "
        r"algorithm generated from the same strategy. Act.: per-round action "
        r"match. Traj.: all seven rounds match.}",
        r"\centering",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{ll" + "cc" * len(GAMES) + "}",
        r"\toprule",
        " & & " + " & ".join(rf"\multicolumn{{2}}{{c}}{{{label}}}"
                             for label in GAMES.values()) + r" \\",
        " ".join(rf"\cmidrule(lr){{{3 + 2 * i}-{4 + 2 * i}}}"
                 for i in range(len(GAMES))),
        r"Model & Shown & " + " & ".join(["Act.", "Traj."] * len(GAMES))
        + r" \\",
        r"\midrule",
    ]
    for model, model_label in MODELS.items():
        for i, (source, source_label) in enumerate(SOURCES.items()):
            cells = []
            for game in GAMES:
                value = stats.get((game, model), {}).get(source)
                cells += (["--", "--"] if value is None
                          else [pct(value[0], 1), pct(value[1], 0)])
            first = (rf"\multirow{{2}}{{*}}{{{model_label}}}" if i == 0 else "")
            lines.append(f"{first} & {source_label} & " + " & ".join(cells)
                         + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\label{tab:fidelity}",
              r"\end{table}"]

    output = Path(args.output) if args.output else root / "fidelity.tex"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
