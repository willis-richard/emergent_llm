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


def _fmt_pm(val, se=None):
    """Compact uncertainty notation in percent: '68(1)\\%' = 0.68 +/- 0.01."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "--"
    pct = round(val * 100)
    if se is None or (isinstance(se, float) and np.isnan(se)):
        return f"{pct}\\%"
    return f"{pct}({round(se * 100)})\\%"


def find_experiment_dir(results_dir: Path, game: str, group_size: int) -> Path:
    parent = results_dir / "cultural_evolution" / game
    matches = sorted(parent.glob(f"n{group_size}_*"))
    if not matches:
        raise FileNotFoundError(f"No experiment for {game} n={group_size} in {parent}")
    if len(matches) > 1:
        raise ValueError(f"Multiple experiments for {game} n={group_size}: {matches}")
    return matches[0]


def compute_metrics(summary: BatchCulturalEvolutionSummary):
    per_run_collapsed = [
        collapse_to_base(run) for run in summary.final_window_mean_frequencies
    ]
    n_runs = len(per_run_collapsed)
    sqrt_n = np.sqrt(n_runs) if n_runs > 0 else float('nan')
    all_genes = set().union(*per_run_collapsed)

    gene_stats = {}
    for gene in all_genes:
        freqs = [run.get(gene, 0.0) for run in per_run_collapsed]
        mean = float(np.mean(freqs))
        se = float(np.std(freqs, ddof=1) / sqrt_n) if n_runs > 1 else float('nan')
        gene_stats[gene] = (mean, se)

    gd = summary.config.evolution_config.game_description
    n_rounds = gd.n_rounds
    max_w = gd.max_player_welfare() / n_rounds
    min_w = gd.min_player_welfare() / n_rounds
    if max_w > min_w:
        effs = [(w - min_w) / (max_w - min_w)
                for w in summary.normalised_social_welfares]
        eff_mean = float(np.mean(effs))
        eff_se = float(np.std(effs, ddof=1) / sqrt_n) if len(effs) > 1 else float('nan')
        eff_stats = (eff_mean, eff_se)
    else:
        eff_stats = (float('nan'), float('nan'))

    cf_mean = float(np.mean(summary.collective_frequencies))
    cf_se = (float(np.std(summary.collective_frequencies, ddof=1) / sqrt_n)
             if len(summary.collective_frequencies) > 1 else float('nan'))
    cf_stats = (cf_mean, cf_se)
    return gene_stats, eff_stats, cf_stats, n_runs


def select_bolded(gene_stats: dict, n_runs: int) -> set:
    if not gene_stats:
        return set()
    leader_gene, (leader_mean, leader_se) = max(gene_stats.items(),
                                                key=lambda x: x[1][0])
    bolded = set()
    for gene, (mean, se) in gene_stats.items():
        combined_se = np.sqrt(leader_se**2 + se**2)
        if abs(leader_mean - mean) < 2 * combined_se:
            bolded.add(gene)
    return bolded


def build_table(games: list[str], group_sizes: list[int], data: dict, ordered_models: list[str]) -> str:
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

    bolded_per_col = {
        (game, gs): select_bolded(data[(game, gs)][0], data[(game, gs)][3])
        for gs in group_sizes for game in games
    }

    attitudes = [Attitude.COLLECTIVE, Attitude.SELFISH]
    for model_idx, model in enumerate(ordered_models):
        for att_idx, attitude in enumerate(attitudes):
            model_cell = (rf"\multirow{{2}}{{*}}{{{pretty_model(model)}}}"
                          if att_idx == 0 else "")
            row = f"{model_cell} & {attitude.value.capitalize()}"
            for gs in group_sizes:
                for game in games:
                    gene_stats, _, _, _ = data[(game, gs)]
                    gene = next(
                        (g for g in gene_stats
                         if g.model == model and g.attitude == attitude),
                        None)
                    if gene is not None:
                        m, se = gene_stats[gene]
                        body = _fmt_pm(m, se)
                        if gene in bolded_per_col[(game, gs)]:
                            cell = rf"\textbf{{{body}}}"
                        else:
                            cell = body
                    else:
                        cell = "--"
                    row += f" & {cell}"
            lines.append(row + r" \\")
        if model_idx < len(ordered_models) - 1:
            lines.append(r"\midrule")
    lines.append(r"\midrule")

    row = r"\multicolumn{2}{l|}{Welfare efficiency}"
    for gs in group_sizes:
        for game in games:
            _, (eff_m, eff_se), _, _ = data[(game, gs)]
            row += f" & {_fmt_pm(eff_m, eff_se)}"
    lines.append(row + r" \\")

    row = r"\multicolumn{2}{l|}{Collective frequency}"
    for gs in group_sizes:
        for game in games:
            _, _, (cf_m, cf_se), _ = data[(game, gs)]
            row += f" & {_fmt_pm(cf_m, cf_se)}"
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
    all_models = set()
    for gs in args.group_sizes:
        for game in args.games:
            exp_dir = find_experiment_dir(args.results_dir, game, gs)
            summary = BatchCulturalEvolutionSummary.load(exp_dir)
            gene_stats, eff_stats, cf_stats, n_runs = compute_metrics(summary)
            data[(game, gs)] = (gene_stats, eff_stats, cf_stats, n_runs)
            all_models.update(g.model for g in gene_stats)

    ordered_models = sorted(all_models)
    table = build_table(args.games, args.group_sizes, data, ordered_models)
    print(table)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(table)


if __name__ == "__main__":
    main()
