"""Tournament results dataclasses."""
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from emergent_llm.common import Attitude, Gene, PlayerId
from emergent_llm.games import (CollectiveRiskDescription,
                                CommonPoolDescription, PublicGoodsDescription)
from emergent_llm.tournament.configs import (BaseTournamentConfig,
                                             BatchTournamentConfig,
                                             CulturalEvolutionConfig)
from emergent_llm.tournament.mixture_tournament import MixtureKey
from matplotlib.ticker import MaxNLocator, MultipleLocator


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
            player_ids=[PlayerId.from_dict(pid_data) for pid_data in data['player_ids']],
            total_payoffs=data['total_payoffs'],
            total_cooperations=data['total_cooperations']
        )


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
    player_ids: list[PlayerId]
    match_results: list[MatchResult]
    _player_stats: dict[str, PlayerStats] = field(default=None, init=False, repr=False)
    _results_df: pd.DataFrame = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Validate results consistency."""
        if not self.match_results:
            raise ValueError("Cannot create results with no match results")

        # Aggregate all match results into player statistics
        stats: dict[PlayerId, PlayerStats] = {}
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
        player_ids = [PlayerId.from_dict(pid_data) for pid_data in data['player_ids']]
        match_results = [MatchResult.from_dict(mr_data) for mr_data in data['match_results']]

        return cls(
            config=config,
            player_ids=player_ids,
            match_results=match_results
        )

    @classmethod
    def load(cls, filepath: str) -> 'FairTournamentResults':
        """Load FairTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'FairTournamentResults':
            raise ValueError(f"Expected FairTournamentResults, got {data['result_type']}")

        return cls.from_dict(data)


@dataclass(frozen=True)
class MixtureTournamentResults:
    """Results from a mixture tournament."""
    config: BaseTournamentConfig
    cooperative_player_ids: list[PlayerId]
    aggressive_player_ids: list[PlayerId]
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

            mixture_key = MixtureKey(n_cooperative, n_aggressive)
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

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': self.config.serialise(),
            'cooperative_player_ids': [asdict(pid) for pid in self.cooperative_player_ids],
            'aggressive_player_ids': [asdict(pid) for pid in self.aggressive_player_ids],
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
        cooperative_player_ids = [PlayerId.from_dict(pid_data) for pid_data in data['cooperative_player_ids']]
        aggressive_player_ids = [PlayerId.from_dict(pid_data) for pid_data in data['aggressive_player_ids']]
        match_results = [MatchResult.from_dict(mr_data) for mr_data in data['match_results']]

        return cls(
            config=config,
            cooperative_player_ids=cooperative_player_ids,
            aggressive_player_ids=aggressive_player_ids,
            match_results=match_results
        )

    @classmethod
    def load(cls, filepath: str) -> 'MixtureTournamentResults':
        """Load MixtureTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'MixtureTournamentResults':
            raise ValueError(f"Expected MixtureTournamentResults, got {data['result_type']}")

        return cls.from_dict(data)


    def create_schelling_diagram(self, output_dir: Path):
        """Create Schelling diagram for this tournament results."""

        # Sort stats by number of cooperators
        sorted_results = sorted(self.mixture_results, key=lambda x: x.n_cooperative)

        # Setup plot styling
        # FIGSIZE, SIZE, FORMAT = (2.5, 0.9), 8, 'svg'  # for 2 column paper
        # FIGSIZE, SIZE, FORMAT = (5, 1.2), 8, 'svg'  # for 1 column slide
        FIGSIZE, SIZE, FORMAT = (2.2, 0.8), 7, 'svg'  # for 2 column slide
        plt.rcParams.update({
            'font.size': SIZE,
            'axes.titlesize': 'medium',
            'axes.labelsize': 'medium',
            'xtick.labelsize': 'small',
            'ytick.labelsize': 'small',
            'legend.fontsize': 'medium',
            'lines.markersize': SIZE / 4,
            'legend.handlelength': SIZE / 6,
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
                label='Cooperative', lw=0.75, marker='o', clip_on=False)
        ax.plot(n_cooperators, agg_scores,
                label='Aggressive', lw=0.75, marker='s', clip_on=False)

        game_description = self.config.game_description
        group_size = game_description.n_players
        ax.set_xlabel('Number of cooperators')
        ax.set_ylabel('Mean reward')
        ax.set_xlim(0, group_size - 1)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))

        ax.set_ylim(math.floor(game_description.min_payoff()),
                    (math.ceil(game_description.max_payoff() / 10 + 1) * 10 ))
        ax.yaxis.set_major_locator(MultipleLocator(self.config.game_description.n_rounds // 1))

        plt.axhline(y=game_description.min_social_welfare(), color='grey', alpha=0.3, linestyle='-')
        plt.axhline(y=game_description.max_social_welfare(), color='grey', alpha=0.3, linestyle='-')
        plt.axhline(y=game_description.max_payoff(), color='grey', alpha=0.3, linestyle='-')

        ax.legend(bbox_to_anchor=(0, 1.4), loc='upper left', ncol=2, frameon=False, columnspacing=0.5)


        # Ensure output directory exists
        output_file = output_dir / f"schelling_n_{group_size}.{FORMAT}"
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
            raise ValueError("Cannot create results with no fair tournament results")

        if len(self.fair_results) != len(self.config.group_sizes):
            raise ValueError(
                f"Number of results ({len(self.fair_results)}) must match "
                f"number of group sizes ({len(self.config.group_sizes)})"
            )

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
            attitude_summary = self.combined_df.groupby(['group_size', 'player_attitude'])['mean_payoff'].agg(['mean', 'std', 'count'])
            summary_lines.extend([
                "\nPerformance by group size and attitude:",
                str(attitude_summary)
            ])

        return "\n".join(summary_lines)

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': asdict(self.config),
            'fair_results': {str(group_size): result.serialise()
                            for group_size, result in self.fair_results.items()},
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
        fair_results = {int(group_size): FairTournamentResults.from_dict(result_data)
                        for group_size, result_data in data['fair_results'].items()}

        return cls(
            config=config,
            fair_results=fair_results
        )

    @classmethod
    def load(cls, filepath: str) -> 'BatchFairTournamentResults':
        """Load BatchFairTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'BatchFairTournamentResults':
            raise ValueError(f"Expected BatchFairTournamentResults, got {data['result_type']}")

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
            raise ValueError("Cannot create results with no mixture tournament results")

        if len(self.mixture_results) != len(self.config.group_sizes):
            raise ValueError(
                f"Number of results ({len(self.mixture_results)}) must match "
                f"number of group sizes ({len(self.config.group_sizes)})"
            )

        # Combine all results into single DataFrame
        combined_rows = []
        for group_size, fair_result in self.mixture_results.items():
            df = fair_result.results_df.copy()
            df['group_size'] = group_size
            combined_rows.append(df)

        combined_df = pd.concat(combined_rows, ignore_index=True)
        object.__setattr__(self, '_combined_df', combined_df)

        # Create summary pivot table
        summary_df = combined_df.pivot_table(
            values='avg_social_welfare',
            index='cooperative_ratio',
            columns='group_size',
            fill_value=np.nan
        )
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
        # Create pivot table with aggressive ratios as rows and group sizes as columns
        pivot_df = self.combined_df.pivot_table(
            values='avg_social_welfare',
            index='cooperative_ratio',
            columns='group_size',
            fill_value=np.nan
        )

        # Format as percentages for the index
        pivot_df.index = [f"{ratio:.0%}" for ratio in pivot_df.index]

        outputs = "=== SOCIAL WELFARE SUMMARY TABLE ==="
        outputs += "\nRows: Aggressive player ratio, Columns: Group size"
        outputs += pivot_df.to_string(float_format='%.3f')
        return outputs

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'config': asdict(self.config),
            'mixture_results': {str(group_size): result.serialise()
                            for group_size, result in self.mixture_results.items()},
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
        mixture_results = {int(group_size): MixtureTournamentResults.from_dict(result_data)
                        for group_size, result_data in data['mixture_results'].items()}

        return cls(
            config=config,
            mixture_results=mixture_results
        )

    @classmethod
    def load(cls, filepath: str) -> 'BatchMixtureTournamentResults':
        """Load BatchMixtureTournamentResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'BatchMixtureTournamentResults':
            raise ValueError(f"Expected BatchMixtureTournamentResults, got {data['result_type']}")

        return cls.from_dict(data)

    def create_schelling_diagrams(self):
        """Create Schelling diagrams for all group sizes."""
        output_dir = Path(self.config.results_dir) / "batch_mixture"
        for group_size, mixture_result in self.mixture_results.items():
            mixture_result.create_schelling_diagram(output_dir)

    def create_social_welfare_diagram(self):
        """Create social welfare vs cooperative ratio diagram with lines for each group size."""

        # Setup plot styling
        # FIGSIZE, SIZE, FORMAT = (2.5, 0.9), 8, 'svg'  # for 2 column paper
        # FIGSIZE, SIZE, FORMAT = (5, 1.2), 8, 'svg'  # for 1 column slide
        FIGSIZE, SIZE, FORMAT = (2.2, 0.8), 7, 'svg'  # for 2 column slide
        plt.rcParams.update({
            'font.size': SIZE,
            'axes.titlesize': 'medium',
            'axes.labelsize': 'medium',
            'xtick.labelsize': 'small',
            'ytick.labelsize': 'small',
            'legend.fontsize': 'medium',
            'lines.markersize': SIZE / 4,
            'legend.handlelength': SIZE / 6,
            'axes.linewidth': 0.1
        })

        fig, ax = plt.subplots(figsize=FIGSIZE, facecolor='white')

        # Plot a line for each group size
        for group_size in sorted(self.config.group_sizes):
            group_data = self.combined_df[self.combined_df['group_size'] == group_size]
            group_data = group_data.sort_values('cooperative_ratio')

            ax.plot(group_data['cooperative_ratio'] * 100,  # Convert to percentage
                    group_data['avg_social_welfare'],
                    label=f'n={group_size}',
                    lw=1.5,
                    marker='o')

        # Get game description from first mixture result
        game_description = self.mixture_results[self.config.group_sizes[-1]].config.game_description

        ax.set_xlabel('Proportion of Cooperative Prompts (%)')
        ax.set_ylabel('Mean Reward')
        ax.set_xlim(0, 100)
        ax.set_ylim(math.floor(game_description.min_payoff()),
                    (math.ceil(game_description.max_payoff() / 10 + 1) * 10 ))
        ax.yaxis.set_major_locator(MultipleLocator(game_description.n_rounds // 1))

        plt.axhline(y=game_description.min_social_welfare(), color='grey', alpha=0.3, linestyle='-')
        plt.axhline(y=game_description.max_social_welfare(), color='grey', alpha=0.3, linestyle='-')
        plt.axhline(y=game_description.max_payoff(), color='grey', alpha=0.3, linestyle='-')

        ax.legend(bbox_to_anchor=(0, 1.4), loc='upper left', ncol=len(self.config.group_sizes), frameon=False, columnspacing=0.5)


        # Ensure output directory exists
        output_file = Path(self.config.results_dir) / "batch_mixture" / f"social_welfare.{FORMAT}"
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

    def __str__(self) -> str:
        lines = [
            f"Cultural Evolution Results",
            f"Final generation: {self.final_generation}",
            f"Final gene frequencies:"
        ]
        for gene, freq in sorted(self.final_gene_frequencies.items(),
                                 key=lambda x: x[1], reverse=True):
            lines.append(f"  {gene}: {freq:.2%}")
        return "\n".join(lines)

    def serialise(self) -> dict:
        """Serialise to dictionary for JSON storage."""
        return {
            'config': asdict(self.config),
            'final_generation': self.final_generation,
            'final_gene_frequencies': {
                str(gene): freq for gene, freq in self.final_gene_frequencies.items()
            },
            'gene_frequency_history': [
                {str(gene): freq for gene, freq in gen_freqs.items()}
                for gen_freqs in self.gene_frequency_history
            ],
            'generation_results': [result.serialise() for result in self.generation_results],
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
        # Need to reconstruct genes list
        genes = [Gene(g['provider_model'], Attitude(g['attitude']))
                 for g in config_data['genes']]

        game_class_map = {
            'PublicGoodsDescription': PublicGoodsDescription,
            'CollectiveRiskDescription': CollectiveRiskDescription,
            'CommonPoolDescription': CommonPoolDescription,
        }
        game_cls = game_class_map[config_data['game_description']['__class__']]
        game_description = game_cls(**{k: v for k, v in config_data['game_description'].items()
                                       if k != '__class__'})

        config = CulturalEvolutionConfig(
            game_description=game_description,
            population_size=config_data['population_size'],
            genes=genes,
            top_k=config_data['top_k'],
            mutation_rate=config_data['mutation_rate'],
            threshold_pct=config_data['threshold_pct'],
            max_generations=config_data['max_generations'],
            repetitions_per_generation=config_data['repetitions_per_generation']
        )

        # Parse gene frequency dictionaries
        def parse_gene_dict(d):
            result = {}
            for gene_str, freq in d.items():
                # Parse "provider_model[attitude]" format
                match = re.match(r'(.+)\[(\w+)\]', gene_str)
                if match:
                    provider_model, attitude_str = match.groups()
                    gene = Gene(provider_model, Attitude(attitude_str))
                    result[gene] = freq
            return result

        final_gene_frequencies = parse_gene_dict(data['final_gene_frequencies'])
        gene_frequency_history = [parse_gene_dict(d) for d in data['gene_frequency_history']]

        # Reconstruct generation results
        generation_results = [FairTournamentResults.from_dict(result_data)
                             for result_data in data['generation_results']]

        return cls(
            config=config,
            final_generation=data['final_generation'],
            final_gene_frequencies=final_gene_frequencies,
            gene_frequency_history=gene_frequency_history,
            generation_results=generation_results
        )

    @classmethod
    def load(cls, filepath: str) -> 'CulturalEvolutionResults':
        """Load CulturalEvolutionResults from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        if data['result_type'] != 'CulturalEvolutionResults':
            raise ValueError(f"Expected CulturalEvolutionResults, got {data['result_type']}")

        return cls.from_dict(data)

    def plot_gene_frequencies(self, output_path: str):
        """Plot gene frequency evolution over generations."""
        import matplotlib.pyplot as plt

        # Collect all unique genes
        all_genes = set()
        for gen_freqs in self.gene_frequency_history:
            all_genes.update(gen_freqs.keys())

        # Create frequency matrix: generations x genes
        generations = list(range(len(self.gene_frequency_history)))

        plt.figure(figsize=(10, 6))

        for gene in all_genes:
            frequencies = [gen_freqs.get(gene, 0.0) for gen_freqs in self.gene_frequency_history]
            plt.plot(generations, frequencies, marker='o', label=str(gene))

        plt.xlabel('Generation')
        plt.ylabel('Gene Frequency')
        plt.title('Gene Frequency Evolution')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path)
        plt.close()
