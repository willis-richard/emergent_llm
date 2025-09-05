"""Tournament results dataclasses."""
import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from emergent_llm.common import Attitude, GameDescription, PlayerId
from matplotlib.ticker import MaxNLocator
from emergent_llm.tournament.base_tournament import BaseTournamentConfig, MatchResult
from emergent_llm.games import (CollectiveRiskDescription,
                                CommonPoolDescription,
                                PublicGoodsDescription)


@dataclass
class PlayerStats:
    """Statistics for a single player across all games."""
    player_id: tuple[str, str, str]
    payoffs: list[float] = field(default_factory=list)
    cooperations: list[int] = field(default_factory=list)

    @property
    def games_played(self) -> int:
        return len(self.payoffs)

    @property
    def mean_payoff(self) -> float:
        return float(np.mean(self.payoffs)) if self.payoffs else 0.0

    @property
    def total_payoff(self) -> float:
        return sum(self.payoffs)

    @property
    def mean_cooperations(self) -> float:
        return float(np.mean(self.cooperations)) if self.cooperations else 0.0

    @property
    def total_cooperations(self) -> int:
        return sum(self.cooperations)

    def add_game_result(self, payoff: float, cooperations: int) -> None:
        """Add results from a single game."""
        self.payoffs.append(payoff)
        self.cooperations.append(cooperations)


@dataclass
class MixtureResult:
    """Results for a specific mixture configuration."""
    group_size: int
    n_cooperative: int
    n_aggressive: int
    cooperative_scores: list[float]
    aggressive_scores: list[float]
    matches_played: int

    def __post_init__(self):
        if not (self.n_cooperative + self.n_aggressive == self.group_size):
            raise ValueError(f"Number of cooperative ({self.n_cooperative}) plus aggressive ({self.n_aggressive}) players must equal group size ({self.group_size})")

    @property
    def aggressive_ratio(self) -> float:
        return self.n_aggressive / self.group_size

    @property
    def cooperative_ratio(self) -> float:
        return self.n_cooperative / self.group_size

    @property
    def avg_cooperative_score(self) -> float:
        return float(np.mean(self.cooperative_scores)) if self.cooperative_scores else np.nan

    @property
    def avg_aggressive_score(self) -> float:
        return float(np.mean(self.aggressive_scores)) if self.aggressive_scores else np.nan

    @property
    def avg_social_welfare(self) -> float:
        all_scores = self.cooperative_scores + self.aggressive_scores
        return float(np.mean(all_scores)) if all_scores else np.nan


@dataclass(frozen=True)
class FairTournamentResults:
    """Results from a fair tournament."""
    config: BaseTournamentConfig
    player_ids: list[tuple[str, str, str]]
    match_results: list[MatchResult]
    _player_stats: dict[str, PlayerStats] = field(default=None, init=False, repr=False)
    _results_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Validate results consistency."""
        if not self.match_results:
            raise ValueError("Cannot create results with no match results")

        # Aggregate all match results into player statistics
        stats: dict[tuple[str, str, str], PlayerStats] = {}
        for mr in self.match_results:
            for pid, total_payoffs, total_cooperations in zip(mr.player_ids,
                                                              mr.total_payoffs,
                                                              mr.total_cooperations):
                if pid not in stats:
                    stats[pid] = PlayerStats(player_id=pid)
                stats[pid].add_game_result(total_payoffs, total_cooperations)

        games_played = [s.games_played for s in stats.values()]
        if len(set(games_played)) > 1:
            raise ValueError(f"Inconsistent games played across players: {games_played}")

        object.__setattr__(self, '_player_stats', stats)

        rows = []
        for stats in self.player_stats.values():
            rows.append({
                'player_name': stats.player_id.name,
                'player_attitude': stats.player_id.attitude.value,
                'player_strategy': stats.player_id.strategy,
                'games_played': stats.games_played,
                'mean_payoff': stats.mean_payoff,
                'total_payoff': stats.total_payoff,
                'total_cooperations': stats.total_cooperations,
                'mean_cooperations': stats.mean_cooperations,
            })
        results_df = pd.DataFrame(rows).sort_values('mean_payoff', ascending=False)
        object.__setattr__(self, '_results_df', results_df)

    @property
    def player_stats(self) -> dict[str, PlayerStats]:
        return self._player_stats

    @property
    def results_df(self) -> pd.DataFrame:
        return self._results_df

    def __str__(self) -> str:
        type_summary = self.results_df.groupby('player_attitude')['total_payoff'].agg(['mean', 'std', 'count'])
        output = str(type_summary)

        output += "\n\nGames played per player:"
        games_per_player = self.results_df.groupby('player_name').size()
        output += f"\nMin: {games_per_player.min()}, Max: {games_per_player.max()}"
        output += f"\nAll players played same number of games: {games_per_player.nunique() == 1}"

        output += f"\n\nTotal matches: {len(self.match_results)}"

        return output

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        data = {
            'config': {
                'game_description_type': self.config.game_description.__class__.__name__,
                'game_description': asdict(self.config.game_description),
                'repetitions': self.config.repetitions
            },
            'player_ids': self.player_ids,
            'match_results': [asdict(mr) for mr in self.match_results],
            'result_type': 'FairTournamentResults'
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


@dataclass(frozen=True)
class MixtureTournamentResults:
    """Results from a mixture tournament."""
    config: BaseTournamentConfig
    cooperative_player_ids: list[tuple[str, str, str]]
    aggressive_player_ids: list[tuple[str, str, str]]
    match_results: list[MatchResult]
    _mixture_results: list[MixtureResult] = field(default=None, init=False, repr=False)
    _results_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Validate results consistency."""
        if not self.match_results:
            raise ValueError("Cannot create results with no match results")

        # Group matches by mixture composition and compute stats
        mixture_stats: dict[tuple[int, int], MixtureResult] = {}

        for match_result in self.match_results:
            # Count attitudes in this match
            n_cooperative = sum(1 for pid in match_result.player_ids
                            if pid.attitude == Attitude.COOPERATIVE)
            n_aggressive = sum(1 for pid in match_result.player_ids
                            if pid.attitude == Attitude.AGGRESSIVE)

            mixture_key = (n_cooperative, n_aggressive)
            group_size = n_cooperative + n_aggressive

            # Initialize mixture result if needed
            if mixture_key not in mixture_stats:
                mixture_stats[mixture_key] = MixtureResult(
                    group_size=group_size,
                    n_cooperative=n_cooperative,
                    n_aggressive=n_aggressive,
                    cooperative_scores=[],
                    aggressive_scores=[],
                    matches_played=0
                )

            # Accumulate scores by attitude
            stats = mixture_stats[mixture_key]
            for player_id, total_payoff in zip(match_result.player_ids, match_result.total_payoffs):
                if player_id.attitude == Attitude.COOPERATIVE:
                    stats.cooperative_scores.append(total_payoff)
                elif player_id.attitude == Attitude.AGGRESSIVE:
                    stats.aggressive_scores.append(total_payoff)

            stats.matches_played += 1

        object.__setattr__(self, '_mixture_results', list(mixture_stats.values()))

        matches_played = [m.matches_played for m in self.mixture_results]
        if len(set(matches_played)) > 1:
            raise ValueError(f"Inconsistent games played across mixtures: {matches_played}")

        rows = []

        for result in self.mixture_results:
            rows.append({
                'group_size': result.group_size,
                'aggressive_ratio': result.aggressive_ratio,
                'cooperative_ratio': result.cooperative_ratio,
                'n_cooperative': result.n_cooperative,
                'n_aggressive': result.n_aggressive,
                'avg_cooperative_score': result.avg_cooperative_score,
                'avg_aggressive_score': result.avg_aggressive_score,
                'avg_social_welfare': result.avg_social_welfare,
                'matches_played': result.matches_played,
            })
        results_df = pd.DataFrame(rows)
        object.__setattr__(self, '_results_df', results_df)

    @property
    def mixture_results(self) -> list[MixtureResult]:
        return self._mixture_results

    @property
    def results_df(self) -> pd.DataFrame:
        return self._results_df

    def __str__(self) -> str:
        return str(self.results_df)

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        data = {
            'config': {
                'game_description_type': self.config.game_description.__class__.__name__,
                'game_description': asdict(self.config.game_description),
                'repetitions': self.config.repetitions
            },
            'cooperative_player_ids': self.cooperative_player_ids,
            'aggressive_player_ids': self.aggressive_player_ids,
            'match_results': [asdict(mr) for mr in self.match_results],
            'mixture_results': [asdict(v) for v in self.mixture_results],
            'result_type': 'MixtureTournamentResults'
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def create_schelling_diagram(self, output_path: str):
        """Create Schelling diagram for this tournament results."""

        # Ensure output directory exists
        output_file = Path(output_path).with_suffix('.png')
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Sort stats by number of cooperators
        sorted_results = sorted(self.mixture_results, key=lambda x: x.n_cooperative)

        # Setup plot styling
        FIGSIZE, SIZE = (10, 4), 12
        plt.rcParams.update({
            'font.size': SIZE,
            'axes.titlesize': 'medium',
            'axes.labelsize': 'medium',
            'xtick.labelsize': 'small',
            'ytick.labelsize': 'small',
            'legend.fontsize': 'medium',
            'axes.linewidth': 0.1
        })

        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        # Extract data for plotting
        n_cooperators = [result.n_cooperative for result in sorted_results]
        coop_scores = [result.avg_cooperative_score for result in sorted_results]
        agg_scores = [result.avg_aggressive_score for result in sorted_results]

        # Shift cooperative scores to show payoffs as if there was one fewer cooperator
        coop_scores = np.roll(coop_scores, -1)

        # Plot cooperative and aggressive scores
        ax.plot(n_cooperators, coop_scores,
                label='Cooperative', lw=0.75, marker='o', markersize=4, clip_on=False)
        ax.plot(n_cooperators, agg_scores,
                label='Aggressive', lw=0.75, marker='s', markersize=4, clip_on=False)

        game_description = self.config.game_description
        group_size = game_description.n_players
        ax.set_xlabel('Number of cooperators')
        ax.set_ylabel('Average reward')
        ax.set_xlim(0, group_size - 1)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))

        ax.set_ylim(math.floor(game_description.min_payoff()),
                    math.ceil(game_description.max_payoff()))

        plt.axhline(y=game_description.min_social_welfare(), color='grey', alpha=0.3, linestyle='-')
        plt.axhline(y=game_description.max_social_welfare(), color='grey', alpha=0.3, linestyle='-')

        ax.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=2, frameon=False, columnspacing=0.5)

        # Save plot
        fig.savefig(output_file, format='png', bbox_inches='tight')
        plt.close(fig)


@dataclass
class BatchTournamentResults:
    """Results from a batch tournament across multiple group sizes."""
    all_results: list[pd.DataFrame]  # One per group size
    group_sizes: list[int]
    repetitions: int
    game_description_generator: str  # Just store the description, not the callable

    def to_combined_dataframe(self) -> pd.DataFrame:
        """Combine all results into single DataFrame."""
        combined = []
        for i, df in enumerate(self.all_results):
            df_copy = df.copy()
            df_copy['group_size'] = self.group_sizes[i]
            combined.append(df_copy)
        return pd.concat(combined, ignore_index=True)

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        data = {
            'all_results': [df.to_dict('records') for df in self.all_results],
            'group_sizes': self.group_sizes,
            'repetitions': self.repetitions,
            'game_description_generator': self.game_description_generator,
            'result_type': 'BatchTournamentResults'
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def load_results(filepath: str):
    """Load tournament results from JSON file."""

    game_class_map = {
        'PublicGoodsDescription': PublicGoodsDescription,
        'CollectiveRiskDescription': CollectiveRiskDescription,
        'CommonPoolDescription': CommonPoolDescription,
    }

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Reconstruct game description
    game_cls = game_class_map[data['config']['game_description_type']]
    game_description = game_cls(**data['config']['game_description'])

    # Reconstruct config
    config = BaseTournamentConfig(
        game_description=game_description,
        repetitions=data['config']['repetitions']
    )

    # Reconstruct match results (convert player_ids back to tuples)
    match_results = []
    for mr_data in data['match_results']:
        mr_data['player_ids'] = [tuple(pid) for pid in mr_data['player_ids']]
        match_results.append(MatchResult(**mr_data))

    result_type = data['result_type']

    if result_type == 'FairTournamentResults':
        # Convert player_ids back to tuples
        player_ids = [tuple(pid) for pid in data['player_ids']]

        return FairTournamentResults(
            config=config,
            player_ids=player_ids,
            match_results=match_results
        )

    elif result_type == 'MixtureTournamentResults':
        # Convert player_ids back to tuples
        cooperative_player_ids = [tuple(pid) for pid in data['cooperative_player_ids']]
        aggressive_player_ids = [tuple(pid) for pid in data['aggressive_player_ids']]

        # Reconstruct mixture results
        mixture_results = [MixtureResult(**mr) for mr in data['mixture_results']]

        return MixtureTournamentResults(
            config=config,
            cooperative_player_ids=cooperative_player_ids,
            aggressive_player_ids=aggressive_player_ids,
            match_results=match_results,
            mixture_results=mixture_results
        )

    else:
        raise ValueError(f"Unknown result type: {result_type}")
