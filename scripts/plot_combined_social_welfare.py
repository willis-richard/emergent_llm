"""Combine social welfare diagrams from multiple BatchMixtureTournamentResults
into a 1xN figure with a shared y-axis. Loops over all games found under
<results_dir>/<game>/<model>, producing one figure per game."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter

from emergent_llm.common import setup
from emergent_llm.tournament.results import (
    BatchMixtureTournamentResults,
    pretty_model,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Combine social welfare diagrams across models, per game")
    parser.add_argument("results_dir", type=Path,
                        help="Top-level dir containing <game>/<model> subdirs")
    parser.add_argument("--games", nargs="+", default=None,
                        help="Games to include; defaults to all subdirs")
    parser.add_argument("--models", nargs="+", default=None,
                        help="Model order; defaults to alphabetical discovery")
    parser.add_argument("--output_dir")
    return parser.parse_args()


def find_results_dir(model_dir: Path) -> Path | None:
    """Return the dir containing batch_mixture results, searching recursively.
    Picks the alphabetically first match if multiple (e.g. rep100 vs rep200)."""
    fname = BatchMixtureTournamentResults.FILENAME
    for ext in (".json", ".json.gz"):
        matches = sorted(model_dir.rglob(f"{fname}{ext}"))
        if matches:
            return matches[0].parent
    return None


def discover_models(game_dir: Path) -> list[str]:
    """Return model subdirs that contain a batch_mixture results file
    anywhere underneath them."""
    return sorted(
        d.name for d in game_dir.iterdir()
        if d.is_dir() and find_results_dir(d) is not None
    )


def plot_combined(results_list: list[BatchMixtureTournamentResults],
                  game_name: str,
                  output_path: Path) -> Path:
    figsize, fmt, _ = setup('aamas')
    n = len(results_list)
    fig, axes = plt.subplots(1, n, figsize=(figsize[0] * n, figsize[1]),
                             facecolor='white', sharey=True, gridspec_kw={'wspace': 0.15})
    if n == 1:
        axes = [axes]

    handles, labels = None, None
    for ax, results in zip(axes, results_list):
        group_sizes = sorted(results.mixture_results.keys())

        for group_size in group_sizes:
            gd = results.mixture_results[group_size].config.game_description
            min_w = gd.min_player_welfare()
            max_w = gd.max_player_welfare()

            group_data = results.combined_df[
                results.combined_df['group_size'] == group_size
            ].sort_values('collective_ratio')

            efficiency = ((group_data['mean_player_welfare'] - min_w) /
                          (max_w - min_w))

            ax.plot(group_data['collective_ratio'] * 100,
                    efficiency,
                    label=f'n={group_size}',
                    lw=1.5,
                    marker='o')

        # ax.set_xlabel('Proportion of Collective prompts (%)')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 1)
        ax.set_title(pretty_model(results.config.model_name))

        if handles is None:
            handles, labels = ax.get_legend_handles_labels()

    axes[0].xaxis.set_major_locator(MultipleLocator(25))
    axes[0].set_ylabel('Welfare efficiency (%)')
    axes[0].yaxis.set_major_locator(MultipleLocator(0.25))
    axes[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))
    # fig.supxlabel('Proportion of Collective prompts (%)')
    axes[1].set_xlabel('Proportion of Collective prompts (%)')

    # if game_name == "public_goods":
    fig.legend(handles, labels,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.21),
            ncol=len(handles),
            frameon=False,
            handletextpad=0.4,
            columnspacing=0.6)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_file = (output_path / f"{game_name}").with_suffix(f".{fmt}")
    # plt.tight_layout(pad=1.05)
    fig.savefig(output_file, format=fmt, bbox_inches='tight')
    plt.close(fig)
    return output_file


def main():
    args = parse_arguments()

    if args.games is not None:
        games = args.games
    else:
        games = sorted(d.name for d in args.results_dir.iterdir() if d.is_dir())

    for game in games:
        game_dir = args.results_dir / game
        if not game_dir.is_dir():
            print(f"Skipping {game}: not a directory")
            continue

        models = args.models or discover_models(game_dir)
        if not models:
            print(f"Skipping {game}: no model results found")
            continue

        results_list = []
        for m in models:
            rdir = find_results_dir(game_dir / m)
            if rdir is None:
                print(f"  No results found for {m}, skipping")
                continue
            results_list.append(BatchMixtureTournamentResults.load(rdir))
        if not results_list:
            continue
        output_file = plot_combined(results_list, game,
                                    args.output_dir)
        print(f"Saved {game}: {output_file}")


if __name__ == "__main__":
    main()
