"""Build a LaTeX table summarising batch cultural evolution results."""
import argparse
from pathlib import Path

import numpy as np

from emergent_llm.common import Attitude
from emergent_llm.tournament.results import (
    BatchCulturalEvolutionSummary,
    collapse_to_base,
    pretty_model,
)

GAME_SHORT = {
    "public_goods": "PGG",
    "collective_risk": "CRD",
    "common_pool": "CPR",
}


def find_experiment_dir(results_dir: Path, game: str, group_size: int) -> Path:
    parent = results_dir / "cultural_evolution" / game
    matches = sorted(parent.glob(f"n{group_size}_*"))
    if not matches:
        raise FileNotFoundError(f"No experiment for {game} n={group_size} in {parent}")
    if len(matches) > 1:
        raise ValueError(f"Multiple experiments for {game} n={group_size}: {matches}")
    return matches[0]


def compute_metrics(summary: BatchCulturalEvolutionSummary):
    wins: dict = {}
    per_gene_freqs: dict = {}
    for run_freqs in summary.final_window_mean_frequencies:
        collapsed = collapse_to_base(run_freqs)
        winner = max(collapsed.items(), key=lambda x: x[1])[0]
        wins[winner] = wins.get(winner, 0) + 1
        for gene, freq in collapsed.items():
            per_gene_freqs.setdefault(gene, []).append(freq)

    gene_stats = {
        gene: (float(np.mean(freqs)), float(np.std(freqs)))
        for gene, freqs in per_gene_freqs.items()
    }

    gd = summary.config.evolution_config.game_description
    n_rounds = gd.n_rounds
    max_w = gd.max_player_welfare() / n_rounds
    min_w = gd.min_player_welfare() / n_rounds
    sw = float(np.mean(summary.normalised_social_welfares))
    eff = (sw - min_w) / (max_w - min_w) if max_w > min_w else float('nan')
    return wins, gene_stats, eff


def build_table(games: list[str], group_sizes: list[int], data: dict, ordered_genes: list) -> str:
    n_games = len(games)
    n_groups = len(group_sizes)
    col_spec = "ll" + ("|" + "c" * n_games) * n_groups

    lines = [
        r"\begin{table*}[t]",
        r"\caption{Cultural evolution results}",
        r"\centering",
        r"\begin{tabular}{" + col_spec + "}",
        r"\toprule",
    ]

    h1 = "Model & Attitude"
    for i, gs in enumerate(group_sizes):
        sep = "c|" if i < n_groups - 1 else "c"
        h1 += rf" & \multicolumn{{{n_games}}}{{{sep}}}{{Group size {gs}}}"
    lines.append(h1 + r" \\")

    h2 = " &"
    for _ in group_sizes:
        for game in games:
            h2 += f" & {GAME_SHORT.get(game, game)}"
    lines.append(h2 + r" \\")
    lines.append(r"\midrule")

    for gene in ordered_genes:
        attitude = gene.attitude.value.capitalize()
        row = f"{pretty_model(gene.model)} & {attitude}"
        for gs in group_sizes:
            for game in games:
                wins, gene_stats, _ = data[(game, gs)]
                n = wins.get(gene, 0)
                if gene in gene_stats:
                    m, s = gene_stats[gene]
                    cell = rf"{n} ({m*100:.0f}$\pm${s*100:.0f})"
                else:
                    cell = "-"
                row += f" & {cell}"
        lines.append(row + r" \\")
    lines.append(r"\midrule")

    row = "Welfare efficiency &"
    for gs in group_sizes:
        for game in games:
            _, _, eff = data[(game, gs)]
            row += f" & {eff*100:.0f}\\%"
    lines.append(row + r" \\")

    lines += [r"\bottomrule", r"\end{tabular}", r"\label{table:ce}", r"\end{table*}"]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir", type=Path, required=True)
    parser.add_argument("--games", nargs="+",
                        default=["public_goods", "collective_risk", "common_pool"])
    parser.add_argument("--group_sizes", nargs="+", type=int, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    data = {}
    all_genes = set()
    for gs in args.group_sizes:
        for game in args.games:
            exp_dir = find_experiment_dir(args.results_dir, game, gs)
            summary = BatchCulturalEvolutionSummary.load(exp_dir)
            wins, gene_stats, eff = compute_metrics(summary)
            data[(game, gs)] = (wins, gene_stats, eff)
            all_genes.update(gene_stats.keys())

    selfish = sorted([g for g in all_genes if g.attitude == Attitude.SELFISH],
                     key=lambda g: g.model)
    collective = sorted([g for g in all_genes if g.attitude == Attitude.COLLECTIVE],
                        key=lambda g: g.model)
    ordered = selfish + collective

    table = build_table(args.games, args.group_sizes, data, ordered)
    print(table)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(table)


if __name__ == "__main__":
    main()
