"""Mixture tournament for a single group size."""
import random
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from emergent_llm.common.attitudes import Attitude
from emergent_llm.players import BasePlayer
from emergent_llm.tournament.base_tournament import BaseTournament, MatchResult, BaseTournamentConfig


@dataclass
class MixtureStats:
    """Statistics for a specific mixture configuration."""
    n_cooperative: int
    n_aggressive: int
    cooperative_scores: list[float]
    aggressive_scores: list[float]
    matches_played: int

    @property
    def group_size(self) -> int:
        return self.n_cooperative + self.n_aggressive

    @property
    def aggressive_ratio(self) -> float:
        return self.n_aggressive / self.group_size

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


class MixtureTournament(BaseTournament):
    """Tournament testing different mixtures of cooperative vs aggressive players for a single group size."""

    def __init__(self,
                 cooperative_players: list[BasePlayer],
                 aggressive_players: list[BasePlayer],
                 config: BaseTournamentConfig):
        """
        Initialize mixture tournament.

        Args:
            cooperative_players: List of cooperative players
            aggressive_players: List of aggressive players
            game_class: Game class to use
            game_description: Game description
            config: Tournament configuration
        """
        super().__init__(config)

        self.cooperative_players = cooperative_players
        self.aggressive_players = aggressive_players

        group_size = config.game_description.n_players

        # Validate we have enough strategies
        if len(cooperative_players) < group_size:
            raise ValueError(f"Need at least {group_size} cooperative players, got {len(cooperative_players)}")
        if len(aggressive_players) < group_size:
            raise ValueError(f"Need at least {group_size} aggressive players, got {len(aggressive_players)}")

        # Stats storage - organized by (n_cooperative, n_aggressive)
        self.mixture_stats: dict[tuple, MixtureStats] = {}

    def run_tournament(self) -> pd.DataFrame:
        """Run tournament across all mixture ratios for this group size."""
        group_size = self.config.game_description.n_players
        self.logger.info(f"Running mixture tournament for group size {group_size}")

        # Test all possible mixtures
        for n_aggressive in range(group_size + 1):
            n_cooperative = group_size - n_aggressive
            mixture_key = (n_cooperative, n_aggressive)

            # Initialize stats for this mixture
            self.mixture_stats[mixture_key] = MixtureStats(
                n_cooperative=n_cooperative,
                n_aggressive=n_aggressive,
                cooperative_scores=[],
                aggressive_scores=[],
                matches_played=0
            )

            # Run matches for this mixture
            self._run_mixture(mixture_key)

        return self.create_results_dataframe()

    def _run_mixture(self, mixture_key: tuple[int, int]):
        """Run multiple matches for a specific mixture"""

        self.logger.info(f"Testing mixture: {mixture_key}")

        for match_num in range(self.config.repetitions):
            # Create players for this match
            match_players = self._create_match_players(mixture_key)
            match_id = f"mixture_{mixture_key}a_match{match_num:04d}"

            # Run the match using base class method
            match_result = self._run_match(match_players, match_id)

            # Record mixture-specific stats
            self._record_match_stats(mixture_key, match_players, match_result)

    def _create_match_players(self, mixture_key: tuple[int, int]) -> list[BasePlayer]:
        """Create players for a single match by sampling from available strategies."""
        players = []

        # Sample cooperative players
        if mixture_key[0] > 0:
            players.extend(random.sample(self.cooperative_players, mixture_key[0]))

        # Sample aggressive players
        if mixture_key[1] > 0:
            players.extend(random.sample(self.aggressive_players, mixture_key[1]))

        # Shuffle to randomize positions
        random.shuffle(players)
        return players

    def _record_match_stats(self, mixture_key: tuple, players: list[BasePlayer], match_result: MatchResult):
        """Record statistics for a completed match."""
        stats = self.mixture_stats[mixture_key]

        # Record payoffs by player type
        for player, payoff in zip(players, match_result.payoffs):
            if hasattr(player, 'attitude'):
                if player.attitude == Attitude.COOPERATIVE:
                    stats.cooperative_scores.append(payoff)
                elif player.attitude == Attitude.AGGRESSIVE:
                    stats.aggressive_scores.append(payoff)
                else:
                    self.logger.warning(f"Player {player.name} has unknown attitude: {player.attitude}")
            else:
                self.logger.warning(f"Player {player.name} has no attitude attribute")

        stats.matches_played += 1

    def create_results_dataframe(self) -> pd.DataFrame:
        """Create DataFrame from collected mixture statistics."""
        rows = []

        for stats in self.mixture_stats.values():
            rows.append({
                'group_size': stats.group_size,
                'aggressive_ratio': stats.aggressive_ratio,
                'n_cooperative': stats.n_cooperative,
                'n_aggressive': stats.n_aggressive,
                'avg_cooperative_score': stats.avg_cooperative_score,
                'avg_aggressive_score': stats.avg_aggressive_score,
                'avg_social_welfare': stats.avg_social_welfare,
                'matches_played': stats.matches_played,
                'total_cooperative_scores': len(stats.cooperative_scores),
                'total_aggressive_scores': len(stats.aggressive_scores)
            })

        return pd.DataFrame(rows)

    def create_schelling_diagram(self, output_path: str):
        """Create Schelling diagram for this tournament."""
        # Ensure output directory exists
        output_file = Path(output_path).with_suffix('.png')
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Sort stats by number of cooperators
        sorted_stats = sorted(self.mixture_stats.values(), key=lambda x: x.n_cooperative)

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
        n_cooperators = [stats.n_cooperative for stats in sorted_stats]
        coop_scores = [stats.avg_cooperative_score for stats in sorted_stats]
        agg_scores = [stats.avg_aggressive_score for stats in sorted_stats]

        # Shift cooperative scores to show payoffs as if there was one fewer cooperator
        # This matches the original Schelling diagram logic
        coop_scores = np.roll(coop_scores, -1)

        # Plot cooperative and aggressive scores
        ax.plot(n_cooperators, coop_scores,
                label='Cooperative', lw=0.75, marker='o', markersize=4)
        ax.plot(n_cooperators, agg_scores,
                label='Aggressive', lw=0.75, marker='s', markersize=4)

        group_size = self.config.game_description.n_players
        ax.set_xlabel('Number of cooperators')
        ax.set_ylabel('Average reward')
        ax.set_xlim(0, group_size)

        # Set y-limits based on data range with some padding
        # valid_scores = [s for s in coop_scores + agg_scores if not np.isnan(s)]
        # if valid_scores:
        #     y_min = min(valid_scores) * 0.95
        #     y_max = max(valid_scores) * 1.05
        #     ax.set_ylim(y_min, y_max)

        ax.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=2, frameon=False, columnspacing=0.5)

        # Save plot
        fig.savefig(output_file, format='png', bbox_inches='tight')
        plt.close(fig)

        self.logger.info(f"Schelling diagram saved: {output_file}")
