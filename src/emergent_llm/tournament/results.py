"""Tournament results dataclasses."""
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from pathlib import Path
import json

from emergent_llm.common import GameDescription


@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    players: list[str]  # Player names
    payoffs: list[float]
    cooperations: list[int]


@dataclass
class PlayerStats:
    """Statistics for a single player across all games."""
    player_name: str
    player_repr: str
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


@dataclass
class FairTournamentResults:
    """Results from a fair tournament."""
    player_stats: dict[str, PlayerStats]
    game_description: GameDescription
    repetitions: int
    _results_df: pd.DataFrame = field(default=None, init=False, repr=False)

    @property
    def results_df(self) -> pd.DataFrame:
        """Convert player stats to DataFrame on demand."""
        if self._results_df is None:
            rows = []
            for stats in self.player_stats.values():
                rows.append({
                    'player_name': stats.player_name,
                    'player_repr': stats.player_repr,
                    'games_played': stats.games_played,
                    'mean_payoff': stats.mean_payoff,
                    'total_payoff': stats.total_payoff,
                    'total_cooperations': stats.total_cooperations,
                    'mean_cooperations': stats.mean_cooperations,
                })
            self._results_df = pd.DataFrame(rows).sort_values('mean_payoff', ascending=False)
        return self._results_df

    def top_performers(self, n: int = 10) -> pd.DataFrame:
        """Get top n performers by mean payoff."""
        return self.results_df.head(n)

    def payoff_distribution(self) -> dict:
        """Get distribution statistics of mean payoffs."""
        payoffs = [stats.mean_payoff for stats in self.player_stats.values()]
        return {
            'mean': np.mean(payoffs),
            'std': np.std(payoffs),
            'min': np.min(payoffs),
            'max': np.max(payoffs)
        }

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        # Convert PlayerStats to serializable format
        player_stats_data = {}
        for name, stats in self.player_stats.items():
            player_stats_data[name] = {
                'player_name': stats.player_name,
                'player_repr': stats.player_repr,
                'payoffs': stats.payoffs,
                'cooperations': stats.cooperations
            }

        data = {
            'player_stats': player_stats_data,
            'game_description': self.game_description.to_dict(),
            'game_description_type': self.game_description.__class__.__name__,
            'repetitions': self.repetitions,
            'result_type': 'FairTournamentResults'
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


@dataclass
class MixtureTournamentResults:
    """Results from a mixture tournament."""
    mixture_results: list[MixtureResult]
    game_description: GameDescription
    repetitions: int

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to pandas DataFrame."""
        data = []
        for result in self.mixture_results:
            data.append({
                'group_size': result.group_size,
                'aggressive_ratio': result.aggressive_ratio,
                'cooperative_ratio': result.cooperative_ratio,
                'n_cooperative': result.n_cooperative,
                'n_aggressive': result.n_aggressive,
                'avg_cooperative_score': result.avg_cooperative_score,
                'avg_aggressive_score': result.avg_aggressive_score,
                'avg_social_welfare': result.avg_social_welfare,
                'matches_played': result.matches_played,
                'total_cooperative_scores': len(result.cooperative_scores),
                'total_aggressive_scores': len(result.aggressive_scores)
            })
        return pd.DataFrame(data)

    def save(self, filepath: str) -> None:
        """Save results to JSON file."""
        data = {
            'mixture_results': [
                {
                    'group_size': r.group_size,
                    'n_cooperative': r.n_cooperative,
                    'n_aggressive': r.n_aggressive,
                    'cooperative_scores': r.cooperative_scores,
                    'aggressive_scores': r.aggressive_scores,
                    'matches_played': r.matches_played,
                }
                for r in self.mixture_results
            ],
            'game_description': self.game_description.to_dict(),
            'game_description_type': self.game_description.__class__.__name__,
            'repetitions': self.repetitions,
            'result_type': 'MixtureTournamentResults'
        }

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


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
    from emergent_llm.games import (
        PublicGoodsDescription, CollectiveRiskDescription, CommonPoolDescription
    )

    game_class_map = {
        'PublicGoodsDescription': PublicGoodsDescription,
        'CollectiveRiskDescription': CollectiveRiskDescription,
        'CommonPoolDescription': CommonPoolDescription,
    }

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Reconstruct game description
    game_cls = game_class_map[data['game_description_type']]
    game_description = game_cls(**data['game_description'])

    result_type = data['result_type']

    if result_type == 'FairTournamentResults':
        # Reconstruct PlayerStats objects
        player_stats = {}
        for name, stats_data in data['player_stats'].items():
            player_stats[name] = PlayerStats(
                player_name=stats_data['player_name'],
                player_repr=stats_data['player_repr'],
                payoffs=stats_data['payoffs'],
                cooperations=stats_data['cooperations']
            )

        return FairTournamentResults(
            player_stats=player_stats,
            game_description=game_description,
            repetitions=data['repetitions'],
        )

    elif result_type == 'MixtureTournamentResults':
        mixture_results = [MixtureResult(**mr) for mr in data['mixture_results']]
        return MixtureTournamentResults(
            mixture_results=mixture_results,
            game_description=game_description,
            repetitions=data['repetitions'],
        )

    elif result_type == 'BatchTournamentResults':
        all_results = [pd.DataFrame(df_data) for df_data in data['all_results']]
        return BatchTournamentResults(
            all_results=all_results,
            group_sizes=data['group_sizes'],
            repetitions=data['repetitions'],
            game_description_generator=data['game_description_generator'],
        )

    else:
        raise ValueError(f"Unknown result type: {result_type}")
