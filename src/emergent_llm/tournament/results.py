"""Tournament results dataclasses."""
import json
from collections import Counter
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator, MultipleLocator

from emergent_llm.common import Attitude, Gene, PlayerId, setup
from emergent_llm.games import get_description_type
from emergent_llm.tournament.configs import (
    BaseTournamentConfig,
    BatchTournamentConfig,
    CulturalEvolutionConfig,
    MixtureKey,
    SurvivorRecord,
)

FIGSIZE, FORMAT = setup('3_col_paper')

@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    player_ids: list[PlayerId]
    total_payoffs: list[float]
    total_cooperations: list[int]

    @classmethod
    def from_dict(cls, data: dict) -> 'MatchResult':
        """Load MatchResult from dictionary data."""
        return cls(
            match_id=data['match_id'],
            player_ids=[
                PlayerId.from_dict(pid_data) for pid_data in data['player_ids']
            ],
            total_payoffs=data['total_payoffs'],
            total_cooperations=data['total_cooperations'])


@dataclass
class PlayerStats:
    """Statistics for a single player across all games."""
    player_id: PlayerId
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
    n_collective: int
    n_exploitative: int
    collective_scores: list[float]
    exploitative_scores: list[float]
    matches_played: int

    def __post_init__(self):
        if not (self.n_collective + self.n_exploitative == self.group_size):
            raise ValueError(
                f"Number of collective ({self.n_collective}) plus exploitative ({self.n_exploitative}) players must equal group size ({self.group_size})"
            )

    @property
    def exploitative_ratio(self) -> float:
        return self.n_exploitative / self.group_size

    @property
    def collective_ratio(self) -> float:
        return self.n_collective / self.group_size

    @property
    def mean_collective_score(self) -> float:
        return float(np.mean(
            self.collective_scores)) if self.collective_scores else np.nan

    @property
    def mean_exploitative_score(self) -> float:
        return float(np.mean(
            self.exploitative_scores)) if self.exploitative_scores else np.nan

    @property
    def mean_social_welfare(self) -> float:
        all_scores = self.collective_scores + self.exploitative_scores
        return float(np.mean(all_scores)) if all_scores else np.nan


@dataclass(frozen=True)
class FairTournamentResults:
    """Results from a fair tournament."""
    config: BaseTournamentConfig
    player_ids: list[PlayerId]
    match_results: list[MatchResult]
    _player_stats: dict[str, PlayerStats] = field(default=None,
                                                  init=False,
                                                  repr=False)
    _results_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Validate results consistency."""
        if not self.match_results:
            raise ValueError("Cannot create results with no match results")

        # Aggregate all match results into player statistics
        stats: dict[PlayerId, PlayerStats] = {}
        for mr in self.match_results:
            for pid, total_payoffs, total_cooperations in zip(
                    mr.player_ids, mr.total_payoffs, mr.total_cooperations):
                if pid not in stats:
                    stats[pid] = PlayerStats(player_id=pid)
                stats[pid].add_game_result(total_payoffs, total_cooperations)

        games_played = [s.games_played for s in stats.values()]
        if len(set(games_played)) > 1:
            raise ValueError(
                f"Inconsistent games played across players: {games_played}")

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
        results_df = pd.DataFrame(rows).sort_values('mean_payoff',
                                                    ascending=False)
        results_df.sort_index(inplace=True)
        object.__setattr__(self, '_results_df', results_df)

    @property
    def player_stats(self) -> dict[str, PlayerStats]:
        return self._player_stats

    @property
    def results_df(self) -> pd.DataFrame:
        return self._results_df

    def __str__(self) -> str:
        type_summary = self.results_df.groupby(
            'player_attitude')['total_payoff'].agg(['mean', 'std', 'count'])
        output = str(type_summary)

        output += "\n\nGames played per player:"
        games_per_player = self.results_df.groupby('player_name').size()
        output += f"\nMin: {games_per_player.min()}, Max: {games_per_player.max()}"
        output += f"\nAll players played same number of games: {games_per_player.nunique() == 1}"

        output += f"\n\nTotal matches: {len(self.match_results)}"

        return output

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': self.config.serialise(),
            'player_ids': [asdict(pid) for pid in self.player_ids],
            'match_results': [asdict(mr) for mr in self.match_results],
            'result_type': 'FairTournamentResults'
        }

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.serialise(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'FairTournamentResults':
        """Load FairTournamentResults from dictionary data."""
        config = BaseTournamentConfig.from_dict(data['config'])
        player_ids = [
            PlayerId.from_dict(pid_data) for pid_data in data['player_ids']
        ]
        match_results = [
            MatchResult.from_dict(mr_data) for mr_data in data['match_results']
        ]

        return cls(config=config,
                   player_ids=player_ids,
                   match_results=match_results)

    @classmethod
    def load(cls, filepath: str) -> 'FairTournamentResults':
        """Load FairTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'FairTournamentResults':
            raise ValueError(
                f"Expected FairTournamentResults, got {data['result_type']}")

        return cls.from_dict(data)


@dataclass(frozen=True)
class MixtureTournamentResults:
    """Results from a mixture tournament."""
    config: BaseTournamentConfig
    collective_player_ids: list[PlayerId]
    exploitative_player_ids: list[PlayerId]
    match_results: list[MatchResult]
    _mixture_results: list[MixtureResult] = field(default=None,
                                                  init=False,
                                                  repr=False)
    _results_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Validate results consistency."""
        if not self.match_results:
            raise ValueError("Cannot create results with no match results")

        # Group matches by mixture composition and compute stats
        mixture_stats: dict[tuple[int, int], MixtureResult] = {}

        for match_result in self.match_results:
            # Count attitudes in this match
            n_collective = sum(1 for pid in match_result.player_ids
                               if pid.attitude == Attitude.COLLECTIVE)
            n_exploitative = sum(1 for pid in match_result.player_ids
                                 if pid.attitude == Attitude.EXPLOITATIVE)

            mixture_key = MixtureKey(n_collective, n_exploitative)
            group_size = n_collective + n_exploitative

            # Initialize mixture result if needed
            if mixture_key not in mixture_stats:
                mixture_stats[mixture_key] = MixtureResult(
                    group_size=group_size,
                    n_collective=n_collective,
                    n_exploitative=n_exploitative,
                    collective_scores=[],
                    exploitative_scores=[],
                    matches_played=0)

            # Accumulate scores by attitude
            stats = mixture_stats[mixture_key]
            for player_id, total_payoff in zip(match_result.player_ids,
                                               match_result.total_payoffs):
                if player_id.attitude == Attitude.COLLECTIVE:
                    stats.collective_scores.append(total_payoff)
                elif player_id.attitude == Attitude.EXPLOITATIVE:
                    stats.exploitative_scores.append(total_payoff)

            stats.matches_played += 1

        object.__setattr__(self, '_mixture_results',
                           list(mixture_stats.values()))

        matches_played = [m.matches_played for m in self.mixture_results]
        if len(set(matches_played)) > 1:
            raise ValueError(
                f"Inconsistent games played across mixtures: {matches_played}")

        rows = []

        for result in self.mixture_results:
            rows.append({
                'group_size': result.group_size,
                'exploitative_ratio': result.exploitative_ratio,
                'collective_ratio': result.collective_ratio,
                'n_collective': result.n_collective,
                'n_exploitative': result.n_exploitative,
                'mean_collective_score': result.mean_collective_score,
                'mean_exploitative_score': result.mean_exploitative_score,
                'mean_social_welfare': result.mean_social_welfare,
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

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': self.config.serialise(),
            'collective_player_ids': [
                asdict(pid) for pid in self.collective_player_ids
            ],
            'exploitative_player_ids': [
                asdict(pid) for pid in self.exploitative_player_ids
            ],
            'match_results': [asdict(mr) for mr in self.match_results],
            'result_type': 'MixtureTournamentResults'
        }

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.serialise(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'MixtureTournamentResults':
        """Load MixtureTournamentResults from dictionary data."""

        config = BaseTournamentConfig.from_dict(data['config'])
        collective_player_ids = [
            PlayerId.from_dict(pid_data)
            for pid_data in data['collective_player_ids']
        ]
        exploitative_player_ids = [
            PlayerId.from_dict(pid_data)
            for pid_data in data['exploitative_player_ids']
        ]
        match_results = [
            MatchResult.from_dict(mr_data) for mr_data in data['match_results']
        ]

        return cls(config=config,
                   collective_player_ids=collective_player_ids,
                   exploitative_player_ids=exploitative_player_ids,
                   match_results=match_results)

    @classmethod
    def load(cls, filepath: str) -> 'MixtureTournamentResults':
        """Load MixtureTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'MixtureTournamentResults':
            raise ValueError(
                f"Expected MixtureTournamentResults, got {data['result_type']}")

        return cls.from_dict(data)

    def create_schelling_diagram(self, output_dir: Path):
        """Create Schelling diagram for this tournament results."""

        # Sort stats by number of collective
        sorted_results = sorted(self.mixture_results,
                                key=lambda x: x.n_collective)

        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        # Extract data for plotting
        n_collective = [result.n_collective for result in sorted_results]
        collective_scores = np.array([
            result.mean_collective_score for result in sorted_results
        ]) / self.config.game_description.n_rounds
        exploitative_scores = np.array([
            result.mean_exploitative_score for result in sorted_results
        ]) / self.config.game_description.n_rounds

        # Shift collective scores to show payoffs as if there was one fewer collective
        collective_scores = np.roll(collective_scores, -1)

        # Plot collective and exploitative scores
        ax.plot(n_collective,
                collective_scores,
                label='Collective',
                lw=0.75,
                marker='o',
                clip_on=False)
        ax.plot(n_collective,
                exploitative_scores,
                label='Exploitative',
                lw=0.75,
                marker='s',
                clip_on=False)

        game_description = self.config.game_description
        group_size = game_description.n_players
        ax.set_xlabel('Number of collective co-players')
        ax.set_ylabel('Normalised reward')
        ax.set_xlim(0, group_size - 1)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))

        ax.set_ylim(math.floor(game_description.normalised_min_payoff()),
                    math.ceil(game_description.normalised_max_payoff()))
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.axhline(y=game_description.normalised_min_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')
        plt.axhline(y=game_description.normalised_max_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')
        plt.axhline(y=game_description.normalised_max_payoff(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')

        ax.legend(bbox_to_anchor=(0, 1.4),
                  loc='upper left',
                  ncol=2,
                  frameon=False,
                  columnspacing=0.5)

        # Ensure output directory exists
        output_file = Path(output_dir) / f"schelling_n_{group_size}.{FORMAT}"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save plot
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)


@dataclass(frozen=True)
class BatchFairTournamentResults:
    """Results from a batch fair tournament across multiple group sizes."""
    config: BatchTournamentConfig
    fair_results: dict[int, FairTournamentResults]
    _combined_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compute combined results from individual tournament results."""
        if not self.fair_results:
            raise ValueError(
                "Cannot create results with no fair tournament results")

        if len(self.fair_results) != len(self.config.group_sizes):
            raise ValueError(
                f"Number of results ({len(self.fair_results)}) must match "
                f"number of group sizes ({len(self.config.group_sizes)})")

        # Combine all results into single DataFrame
        combined_rows = []
        for group_size, fair_result in self.fair_results.items():
            df = fair_result.results_df.copy()
            df['group_size'] = group_size
            combined_rows.append(df)

        combined_df = pd.concat(combined_rows, ignore_index=True)
        object.__setattr__(self, '_combined_df', combined_df)

    @property
    def combined_df(self) -> pd.DataFrame:
        """Combined results DataFrame with group size information."""
        return self._combined_df

    def __str__(self) -> str:
        """Summary of batch tournament results."""
        summary_lines = [
            f"Batch Fair Tournament Results",
            f"Group sizes: {self.config.group_sizes}",
            f"Repetitions per group: {self.config.repetitions}",
            f"Total matches: {len(self.combined_df)}",
        ]

        # Group performance by attitude and group size
        if 'player_attitude' in self.combined_df.columns:
            attitude_summary = self.combined_df.groupby([
                'group_size', 'player_attitude'
            ])['mean_payoff'].agg(['mean', 'std', 'count'])
            summary_lines.extend([
                "\nPerformance by group size and attitude:",
                str(attitude_summary)
            ])

        return "\n".join(summary_lines)

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': asdict(self.config),
            'fair_results': {
                str(group_size): result.serialise()
                for group_size, result in self.fair_results.items()
            },
            'result_type': 'BatchFairTournamentResults'
        }

    def save(self) -> None:
        """Save results to JSON file."""
        filepath = Path(self.config.results_dir) / "batch_fair/results.json"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.serialise(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchFairTournamentResults':
        """Load BatchFairTournamentResults from dictionary data."""
        config = BatchTournamentConfig(**data['config'])
        fair_results = {
            int(group_size): FairTournamentResults.from_dict(result_data)
            for group_size, result_data in data['fair_results'].items()
        }

        return cls(config=config, fair_results=fair_results)

    @classmethod
    def load(cls, filepath: str) -> 'BatchFairTournamentResults':
        """Load BatchFairTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'BatchFairTournamentResults':
            raise ValueError(
                f"Expected BatchFairTournamentResults, got {data['result_type']}"
            )

        return cls.from_dict(data)


@dataclass(frozen=True)
class BatchMixtureTournamentResults:
    """Results from a batch mixture tournament across multiple group sizes."""
    config: BatchTournamentConfig
    mixture_results: dict[int, MixtureTournamentResults]
    _combined_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _summary_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compute combined results from individual tournament results."""
        if not self.mixture_results:
            raise ValueError(
                "Cannot create results with no mixture tournament results")

        if len(self.mixture_results) != len(self.config.group_sizes):
            raise ValueError(
                f"Number of results ({len(self.mixture_results)}) must match "
                f"number of group sizes ({len(self.config.group_sizes)})")

        # Combine all results into single DataFrame
        combined_rows = []
        for group_size, fair_result in self.mixture_results.items():
            df = fair_result.results_df.copy()
            df['group_size'] = group_size
            combined_rows.append(df)

        combined_df = pd.concat(combined_rows, ignore_index=True)
        object.__setattr__(self, '_combined_df', combined_df)

        # Create summary pivot table
        summary_df = combined_df.pivot_table(values='mean_social_welfare',
                                             index='collective_ratio',
                                             columns='group_size',
                                             fill_value=np.nan)
        # Format index as percentages
        summary_df.index = [f"{ratio:.0%}" for ratio in summary_df.index]
        object.__setattr__(self, '_summary_df', summary_df)

    @property
    def combined_df(self) -> pd.DataFrame:
        """Combined results DataFrame with group size information."""
        return self._combined_df

    @property
    def summary_df(self) -> pd.DataFrame:
        """Summary table with social welfare across group sizes and ratios."""
        return self._summary_df

    def __str__(self) -> str:
        """Create summary table with social welfare across group sizes and ratios."""
        # Create pivot table with exploitative ratios as rows and group sizes as columns
        pivot_df = self.combined_df.pivot_table(values='mean_social_welfare',
                                                index='collective_ratio',
                                                columns='group_size',
                                                fill_value=np.nan)

        # Format as percentages for the index
        pivot_df.index = [f"{ratio:.0%}" for ratio in pivot_df.index]

        outputs = "=== SOCIAL WELFARE SUMMARY TABLE ==="
        outputs += "\nRows: Exploitative player ratio, Columns: Group size"
        outputs += pivot_df.to_string(float_format='%.3f')
        return outputs

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': asdict(self.config),
            'mixture_results': {
                str(group_size): result.serialise()
                for group_size, result in self.mixture_results.items()
            },
            'result_type': 'BatchMixtureTournamentResults'
        }

    def save(self) -> None:
        """Save results to JSON file."""
        filepath = Path(self.config.results_dir) / "batch_mixture/results.json"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.serialise(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchMixtureTournamentResults':
        """Load BatchMixtureTournamentResults from dictionary data."""
        config = BatchTournamentConfig(**data['config'])
        mixture_results = {
            int(group_size): MixtureTournamentResults.from_dict(result_data)
            for group_size, result_data in data['mixture_results'].items()
        }

        return cls(config=config, mixture_results=mixture_results)

    @classmethod
    def load(cls, filepath: str) -> 'BatchMixtureTournamentResults':
        """Load BatchMixtureTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'BatchMixtureTournamentResults':
            raise ValueError(
                f"Expected BatchMixtureTournamentResults, got {data['result_type']}"
            )

        return cls.from_dict(data)

    def create_schelling_diagrams(self):
        """Create Schelling diagrams for all group sizes."""
        output_dir = Path(self.config.results_dir) / "batch_mixture"
        for group_size, mixture_result in self.mixture_results.items():
            mixture_result.create_schelling_diagram(output_dir)

    def create_social_welfare_diagram(self):
        """Create social welfare vs collective ratio diagram with lines for each group size."""

        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        # Get game description from first mixture result
        game_description = self.mixture_results[
            self.config.group_sizes[-1]].config.game_description

        # Plot a line for each group size
        for group_size in sorted(self.config.group_sizes):
            group_data = self.combined_df[self.combined_df['group_size'] ==
                                          group_size]
            group_data = group_data.sort_values('collective_ratio')

            ax.plot(
                group_data['collective_ratio'] * 100,  # Convert to percentage
                group_data['mean_social_welfare'] / game_description.n_rounds,
                label=f'n={group_size}',
                lw=1.5,
                marker='o')

        ax.set_xlabel('Proportion of collective prompts (%)')
        ax.set_ylabel('Normalised reward')
        ax.set_xlim(0, 100)
        ax.set_ylim(
            math.floor(game_description.normalised_min_payoff()),
            math.ceil(game_description.normalised_max_social_welfare())
        )
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.axhline(y=game_description.normalised_min_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')
        plt.axhline(y=game_description.normalised_max_social_welfare(),
                    color='grey',
                    alpha=0.3,
                    linestyle='-')

        ax.legend(bbox_to_anchor=(-0.13, 1.4),
                  loc='upper left',
                  ncol=len(self.config.group_sizes),
                  frameon=False,
                  handletextpad=0.4,
                  columnspacing=0.6)

        # Ensure output directory exists
        output_file = Path(self.config.results_dir
                          ) / "batch_mixture" / f"social_welfare.{FORMAT}"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save plot
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def create_relative_schelling_diagram(self):
        """Create exploitative - collective payoff diagram with lines for each group size."""

        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        # Get game description from first mixture result
        game_description = self.mixture_results[
            self.config.group_sizes[-1]].config.game_description

        # Plot a line for each group size
        for group_size in sorted(self.config.group_sizes):
            group_data = self.combined_df[self.combined_df['group_size'] ==
                                          group_size]
            group_data = group_data.sort_values('collective_ratio')

            collective_scores = group_data.mean_collective_score
            rolled_collective_scores = np.roll(collective_scores, -1)[:-1]
            exploitative_scores = group_data.mean_exploitative_score.values[:-1]
            difference = exploitative_scores - rolled_collective_scores
            normalised_difference = difference / game_description.n_rounds

            n_collective = group_data.n_collective
            rolled_n_collective = np.roll(n_collective, -1)[:-1] - 1
            n_exploitative = group_data.n_exploitative.values[:-1] - 1
            opponent_proportion = rolled_n_collective / (rolled_n_collective + n_exploitative)

            ax.plot(
                opponent_proportion * 100,  # Convert to percentage
                normalised_difference,
                label=f'n={group_size}',
                lw=1.5,
                marker='o')

        ax.set_xlabel('Opponent collective prompts (%)')
        ax.set_ylabel('Normalised advantage')
        ax.set_xlim(0, 100)
        ax.set_ylim(
            math.floor((game_description.normalised_min_payoff() - game_description.normalised_max_payoff())),
            math.ceil((game_description.normalised_max_payoff() - game_description.normalised_min_payoff()))
        )
        ax.yaxis.set_major_locator(MultipleLocator(1))

        plt.axhline(y=0,
                    color='grey',
                    alpha=0.3,
                    linestyle='-')

        ax.legend(bbox_to_anchor=(-0.13, 1.4),
                  loc='upper left',
                  ncol=len(self.config.group_sizes),
                  frameon=False,
                  handletextpad=0.4,
                  columnspacing=0.6)

        # Ensure output directory exists
        output_file = Path(self.config.results_dir
                          ) / "batch_mixture" / f"schelling_difference.{FORMAT}"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save plot
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)


@dataclass
class CulturalEvolutionResults:
    """Results from cultural evolution tournament."""
    config: CulturalEvolutionConfig
    final_generation: int
    final_gene_frequencies: dict[Gene, float]
    gene_frequency_history: list[dict[Gene, float]]
    generation_results: list[FairTournamentResults]
    survivor_history: list[list['SurvivorRecord']] = field(default_factory=list)
    _gene_frequency_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _generation_stats_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _survivor_summary_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Build analysis dataframes from raw results."""
        all_genes = set()
        for gen_freqs in self.gene_frequency_history:
            all_genes.update(gen_freqs.keys())
        all_genes = sorted(all_genes, key=str)

        gene_freq_rows = []
        for gen_freqs in self.gene_frequency_history:
            row = {gene: gen_freqs.get(gene, 0.0) for gene in all_genes}
            gene_freq_rows.append(row)

        gene_frequency_df = pd.DataFrame(gene_freq_rows, columns=all_genes)
        gene_frequency_df.index.name = 'generation'
        object.__setattr__(self, '_gene_frequency_df', gene_frequency_df)

        # Build generation statistics dataframe
        stats_rows = []
        for generation, gen_result in enumerate(self.generation_results):
            collective_payoffs = []
            exploitative_payoffs = []
            all_payoffs = []
            cooperations = []

            total_rounds = self.config.game_description.n_rounds

            for stats in gen_result.player_stats.values():
                all_payoffs.append(stats.mean_payoff)
                cooperations.append(stats.mean_cooperations / total_rounds)

                if stats.player_id.attitude == Attitude.COLLECTIVE:
                    collective_payoffs.append(stats.mean_payoff)
                elif stats.player_id.attitude == Attitude.EXPLOITATIVE:
                    exploitative_payoffs.append(stats.mean_payoff)

            # Calculate attitude frequencies
            gen_freqs = self.gene_frequency_history[generation]
            collective_freq = sum(freq for gene, freq in gen_freqs.items()
                                  if gene.attitude == Attitude.COLLECTIVE)

            stats_rows.append({
                'collective_mean_payoff': np.mean(collective_payoffs) if collective_payoffs else np.nan,
                'exploitative_mean_payoff': np.mean(exploitative_payoffs) if exploitative_payoffs else np.nan,
                'overall_mean_payoff': np.mean(all_payoffs),
                'cooperation_rate': np.mean(cooperations),
                'collective_frequency': collective_freq,
                'exploitative_frequency': 1 - collective_freq,
            })

        generation_stats_df = pd.DataFrame(stats_rows)
        generation_stats_df.index.name = 'generation'
        object.__setattr__(self, '_generation_stats_df', generation_stats_df)

        # Build strategy survivor dataframe
        # Count how often each strategy survives
        strategy_counts: Counter[str] = Counter()
        strategy_genes: dict[str, Gene] = {}
        strategy_total_fitness: dict[str, float] = Counter()

        for gen_survivors in self.survivor_history:
            for record in gen_survivors:
                strategy_counts[record.name] += 1
                strategy_genes[record.name] = record.gene
                strategy_total_fitness[record.name] += record.fitness

        rows = []
        for strategy_name, count in strategy_counts.most_common():
            gene = strategy_genes[strategy_name]
            avg_fitness = strategy_total_fitness[strategy_name] / count
            rows.append({
                'strategy': strategy_name,
                'gene': str(gene),
                'model': gene.model,
                'attitude': gene.attitude.value,
                'survival_count': count,
                'survival_rate': count / len(self.survivor_history),
                'mean_fitness': avg_fitness,
            })

        object.__setattr__(self, '_survivor_summary_df', pd.DataFrame(rows))

    @property
    def gene_frequency_df(self) -> pd.DataFrame:
        """DataFrame of gene frequencies over generations."""
        return self._gene_frequency_df

    @property
    def generation_stats_df(self) -> pd.DataFrame:
        """DataFrame of generation-level statistics."""
        return self._generation_stats_df

    @property
    def survivor_summary_df(self) -> pd.DataFrame:
        """Summary of strategy survival across generations."""
        return self._survivor_summary_df

    @property
    def winning_gene(self) -> Gene:
        """Gene with highest frequency in final generation."""
        return max(self.final_gene_frequencies.items(), key=lambda x: x[1])[0]

    def __str__(self) -> str:
        lines = [
            f"Cultural Evolution Results",
            f"Final generation: {self.final_generation}",
            f"Final gene frequencies:"
        ]
        for gene, freq in sorted(self.final_gene_frequencies.items(),
                                 key=lambda x: x[1],
                                 reverse=True):
            lines.append(f"  {gene}: {freq:.2%}")

        lines.append(f"\nTop surviving strategies (across {len(self.survivor_history)} generations):")
        for _, row in self._survivor_summary_df.head(10).iterrows():
            lines.append(
                f"  {row['strategy']} ({row['gene']}): "
                f"survived {row['survival_count']}x, mean fitness {row['mean_fitness']:.2f}"
            )

        return "\n".join(lines)

    def serialise(self) -> dict:
        """Serialise to dictionary for JSON storage."""
        config_dict = asdict(self.config)
        config_dict['game_description']['__class__'] = self.config.game_description.__class__.__name__
        return {
            'config': config_dict,
            'final_generation': self.final_generation,
            'final_gene_frequencies': [
                {'gene': asdict(gene), 'frequency': freq}
                for gene, freq in self.final_gene_frequencies.items()
            ],
            'gene_frequency_history': [
                [{'gene': asdict(gene), 'frequency': freq} for gene, freq in gen_freqs.items()]
                for gen_freqs in self.gene_frequency_history
            ],
            'generation_results': [
                result.serialise() for result in self.generation_results
            ],
            'survivor_history': [
                [record.to_dict() for record in gen_survivors]
                for gen_survivors in self.survivor_history
            ],
            'result_type': 'CulturalEvolutionResults'
        }

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.serialise(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'CulturalEvolutionResults':
        """Load CulturalEvolutionResults from dictionary data."""
        # Reconstruct config
        config_data = data['config']

        game_cls = get_description_type(config_data['game_description']['__class__'])
        game_description = game_cls(
            **{
                k: v
                for k, v in config_data['game_description'].items()
                if k != '__class__'
            })

        config = CulturalEvolutionConfig(
            game_description=game_description,
            population_size=config_data['population_size'],
            top_k=config_data['top_k'],
            mutation_rate=config_data['mutation_rate'],
            threshold_pct=config_data['threshold_pct'],
            max_generations=config_data['max_generations'],
            repetitions_per_generation=config_data['repetitions_per_generation']
        )

        # Parse gene frequency dictionaries
        final_gene_frequencies = {
            Gene.from_dict(item['gene']): item['frequency']
            for item in data['final_gene_frequencies']
        }

        gene_frequency_history = [
            {Gene.from_dict(item['gene']): item['frequency'] for item in gen_freqs}
            for gen_freqs in data['gene_frequency_history']
        ]

        # Reconstruct generation results
        generation_results = [
            FairTournamentResults.from_dict(result_data)
            for result_data in data['generation_results']
        ]

        survivor_history = [
            [SurvivorRecord.from_dict(record) for record in gen_survivors]
            for gen_survivors in data['survivor_history']
        ]

        return cls(config=config,
                   final_generation=data['final_generation'],
                   final_gene_frequencies=final_gene_frequencies,
                   gene_frequency_history=gene_frequency_history,
                   generation_results=generation_results,
                   survivor_history=survivor_history)

    @classmethod
    def load(cls, filepath: str) -> 'CulturalEvolutionResults':
        """Load CulturalEvolutionResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'CulturalEvolutionResults':
            raise ValueError(
                f"Expected CulturalEvolutionResults, got {data['result_type']}")

        return cls.from_dict(data)

    def plot_gene_frequencies(self, output_dir: Path):
        """Plot gene frequency evolution over generations."""
        fig, ax = plt.subplots(figsize=(FIGSIZE[0], FIGSIZE[1] * 2), facecolor='white')

        for gene in self.gene_frequency_df.columns:
            ax.plot(self.gene_frequency_df.index,
                    self.gene_frequency_df[gene],
                    marker='o',
                    lw=0.75,
                    label=str(gene),
                    clip_on=False)

        ax.set_xlabel('Generation')
        ax.set_ylabel('Gene Frequency')
        ax.set_ylim(0, 1)
        ax.legend(bbox_to_anchor=(0, 1.8), loc='upper left', frameon=False)
        ax.grid(True, alpha=0.3)

        output_file = output_dir / f"gene_frequencies.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plot_attitude_evolution(self, output_dir: Path):
        """Plot attitude proportions over generations."""
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['collective_frequency'],
                label='Collective',
                marker='o',
                lw=0.75,
                clip_on=False)
        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['exploitative_frequency'],
                label='Exploitative',
                marker='s',
                lw=0.75,
                clip_on=False)

        ax.set_xlabel('Generation')
        ax.set_ylabel('Proportion')
        ax.set_ylim(0, 1)
        ax.legend(bbox_to_anchor=(0, 1.4),
                  loc='upper left',
                  ncol=2,
                  frameon=False,
                  columnspacing=0.5)
        ax.grid(True, alpha=0.3)

        output_file = output_dir / f"attitude_evolution.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plot_cooperation_evolution(self, output_dir: Path):
        """Plot cooperation rate over generations."""
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['cooperation_rate'],
                marker='o',
                lw=0.75,
                color='green',
                clip_on=False)

        ax.set_xlabel('Generation')
        ax.set_ylabel('Cooperation Rate')
        ax.set_ylim(0, 1)
        ax.legend(bbox_to_anchor=(0, 1.4), loc='upper left', frameon=False)
        ax.grid(True, alpha=0.3)

        output_file = output_dir / f"cooperation_evolution.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plot_mean_payoffs(self, output_dir: Path):
        """Plot mean payoffs by attitude and overall through generations."""
        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        game_description = self.config.game_description

        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['collective_mean_payoff'] / game_description.n_rounds,
                label='Collective',
                marker='o',
                lw=0.75,
                clip_on=False)
        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['exploitative_mean_payoff'] / game_description.n_rounds,
                label='Exploitative',
                marker='s',
                lw=0.75,
                clip_on=False)
        ax.plot(self.generation_stats_df.index,
                self.generation_stats_df['overall_mean_payoff'] / game_description.n_rounds,
                label='Overall',
                marker='^',
                lw=0.75,
                linestyle='--',
                clip_on=False)

        ax.axhline(y=game_description.normalised_min_social_welfare(),
                   color='grey',
                   alpha=0.3,
                   linestyle='-')
        ax.axhline(y=game_description.normalised_max_social_welfare(),
                   color='grey',
                   alpha=0.3,
                   linestyle='-')
        ax.axhline(y=game_description.normalised_max_payoff(),
                   color='grey',
                   alpha=0.3,
                   linestyle='-')

        ax.set_ylim(
            math.floor(game_description.normalised_min_payoff()),
            math.ceil(game_description.normalised_max_payoff() / 10 + 1) * 10
        )
        ax.yaxis.set_major_locator(MultipleLocator(1))

        ax.set_xlabel('Generation')
        ax.set_ylabel('Mean Payoff')
        ax.legend(bbox_to_anchor=(0, 1.4),
                  loc='upper left',
                  ncol=3,
                  frameon=False,
                  columnspacing=0.5)
        ax.grid(True, alpha=0.3)

        output_file = output_dir / f"mean_payoffs.{FORMAT}"
        fig.savefig(output_file, format=FORMAT, bbox_inches='tight')
        plt.close(fig)

    def plots(self, output_dir: str | Path):
        """Create all plots for cultural evolution results."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        self.plot_gene_frequencies(output_dir)
        self.plot_attitude_evolution(output_dir)
        self.plot_cooperation_evolution(output_dir)
        self.plot_mean_payoffs(output_dir)


@dataclass
class BatchCulturalEvolutionTournamentResults:
    runs: list[CulturalEvolutionResults]
    _run_summary_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _gene_summary_df: pd.DataFrame = field(default=None, init=False, repr=False)
    _strategy_summary_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Build analysis dataframes from all runs."""
        if not self.runs:
            raise ValueError("Cannot create results with no runs")

        # Build per-run summary
        run_rows = []
        for run_idx, run in enumerate(self.runs):
            # Get winning gene (highest frequency)
            winning_gene = run.winning_gene
            winning_frequency = run.final_gene_frequencies[winning_gene]

            run_rows.append({
                'run': run_idx,
                'generations': run.final_generation,
                'winning_gene': str(winning_gene),
                'winning_model': winning_gene.model,
                'winning_attitude': winning_gene.attitude.value,
                'winning_frequency': winning_frequency,
                'threshold_met': winning_frequency >= run.config.threshold_pct,
            })

        run_summary_df = pd.DataFrame(run_rows)
        object.__setattr__(self, '_run_summary_df', run_summary_df)

        # Build gene-level summary across all runs
        all_genes = set()
        for run in self.runs:
            all_genes.update(run.final_gene_frequencies.keys())

        # Count wins per gene
        win_counts = {}
        for run in self.runs:
            winner = run.winning_gene
            win_counts[winner] = win_counts.get(winner, 0) + 1

        gene_rows = []
        for gene in sorted(all_genes, key=str):
            frequencies = []
            for run in self.runs:
                if gene in run.final_gene_frequencies:
                    freq = run.final_gene_frequencies[gene]
                    frequencies.append(freq)

            wins = win_counts.get(gene, 0)
            gene_rows.append({
                'gene': str(gene),
                'model': gene.model,
                'attitude': gene.attitude.value,
                'wins': wins,
                'win_proportion': wins / len(self.runs),
                'mean_frequency': np.mean(frequencies) if frequencies else 0.0,
                'std_frequency': np.std(frequencies) if frequencies else 0.0,
            })

        gene_summary_df = pd.DataFrame(gene_rows).sort_values('wins', ascending=False)
        object.__setattr__(self, '_gene_summary_df', gene_summary_df)

        # Aggregate strategy survival statistics across all runs
        strategy_counts: Counter[str] = Counter()
        strategy_genes: dict[str, Gene] = {}
        strategy_fitness_sum: dict[str, float] = Counter()
        strategy_fitness_count: dict[str, int] = Counter()

        for run in self.runs:
            if not run.survivor_history:
                continue

            # All generations
            for gen_survivors in run.survivor_history:
                for record in gen_survivors:
                    strategy_counts[record.strategy_name] += 1
                    strategy_genes[record.strategy_name] = record.gene
                    strategy_fitness_sum[record.strategy_name] += record.fitness
                    strategy_fitness_count[record.strategy_name] += 1

        rows = []
        for strategy_name, count in strategy_counts.most_common():
            gene = strategy_genes[strategy_name]
            avg_fitness = strategy_fitness_sum[strategy_name] / strategy_fitness_count[strategy_name]
            rows.append({
                'strategy': strategy_name,
                'gene': str(gene),
                'model': gene.model,
                'attitude': gene.attitude.value,
                'total_survivals': count,
                'mean_fitness': avg_fitness,
            })

        object.__setattr__(self, '_strategy_summary_df', pd.DataFrame(rows))

    @property
    def run_summary_df(self) -> pd.DataFrame:
        """Per-run summary statistics."""
        return self._run_summary_df

    @property
    def gene_summary_df(self) -> pd.DataFrame:
        """Gene-level summary across all runs."""
        return self._gene_summary_df

    @property
    def strategy_summary_df(self) -> pd.DataFrame:
        """Aggregated strategy survival statistics across all runs."""
        return self._strategy_summary_df

    def __str__(self) -> str:
        threshold_met = self.run_summary_df['threshold_met'].sum()
        avg_gens = self.run_summary_df['generations'].mean()

        lines = [
            f"Multi-run cultural evolution: {len(self.runs)} runs",
            f"Threshold reached: {threshold_met}/{len(self.runs)} ({threshold_met/len(self.runs):.1%})",
            f"Average generations: {avg_gens:.1f}",
            "",
            "Gene performance:",
        ]

        # Gene performance table - show all genes
        display_df = self.gene_summary_df[['gene', 'wins', 'win_proportion', 'mean_frequency', 'std_frequency']].copy()
        display_df['win_proportion'] = display_df['win_proportion'].apply(lambda x: f"{x:.1%}")
        display_df['mean_frequency'] = display_df['mean_frequency'].apply(lambda x: f"{x:.3f}")
        display_df['std_frequency'] = display_df['std_frequency'].apply(lambda x: f"{x:.3f}")
        display_df.columns = ['Gene', 'Wins', 'Win%', 'Mean', 'Std']
        lines.append(display_df.to_string(index=False))

        # Attitude and model summaries
        lines.append("")
        lines.append("By attitude:")
        attitude_counts = self.run_summary_df['winning_attitude'].value_counts()
        for attitude, count in attitude_counts.items():
            lines.append(f"  {attitude}: {count} ({count/len(self.runs):.1%})")

        lines.append("")
        lines.append("By model:")
        model_counts = self.run_summary_df['winning_model'].value_counts()
        for model, count in model_counts.items():
            lines.append(f"  {model}: {count} ({count/len(self.runs):.1%})")

        lines.append("")
        lines.append("Top surviving strategies (across all runs):")
        top_strategies = self._strategy_summary_df.nlargest(10, 'total_survivals')
        for _, row in top_strategies.iterrows():
            lines.append(
                f"  {row['strategy']} ({row['attitude']}): "
                f"{row['total_survivals']} survivals, "
                f"fitness={row['mean_fitness']:.2f}"
            )

        return "\n".join(lines)

    def plots(self, output_dir: str | Path):
        """Create all plots including individual runs and aggregates."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Plot individual runs
        individual_dir = output_dir / "individual_runs"
        individual_dir.mkdir(exist_ok=True)
        for idx, run in enumerate(self.runs):
            run_dir = individual_dir / f"run_{idx:03d}"
            run.plots(run_dir)

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'runs': [run.serialise() for run in self.runs],
            'result_type': 'MultiRunCulturalEvolutionResults'
        }

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.serialise(), f, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'MultiRunCulturalEvolutionResults':
        """Load MultiRunCulturalEvolutionResults from dictionary data."""
        runs = [
            CulturalEvolutionResults.from_dict(run_data)
            for run_data in data['runs']
        ]
        return cls(runs=runs)

    @classmethod
    def load(cls, filepath: str) -> 'MultiRunCulturalEvolutionResults':
        """Load MultiRunCulturalEvolutionResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'MultiRunCulturalEvolutionResults':
            raise ValueError(
                f"Expected MultiRunCulturalEvolutionResults, got {data['result_type']}"
            )

        return cls.from_dict(data)
