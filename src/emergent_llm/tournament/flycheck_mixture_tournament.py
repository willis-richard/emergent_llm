"""Mixture tournament for a single group size."""
import logging
import random
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from emergent_llm.games.base_game import BaseGame, GameResult
from emergent_llm.common import GameDescription
from emergent_llm.players import BasePlayer
from emergent_llm.common.attitudes import Attitude
from emergent_llm.tournament.fair_tournament import MatchResult


@dataclass
class MixtureTournamentConfig:
    """Configuration for single-group-size mixture tournament."""
    game_class: type[BaseGame]
    game_description: GameDescription
    matches_per_mixture: int


@dataclass
class MixtureStats:
    """Statistics for a specific mixture configuration."""
    n_cooperative: int
    n_aggressive: int
    cooperative_scores: List[float]
    aggressive_scores: List[float]
    matches_played: int

    @property
    def group_size(self) -> int:
        return self.n_cooperative + self.n_aggressive

    @property
    def aggressive_ratio(self) -> float:
        return self.n_aggressive / self.group_size

    @property
    def avg_cooperative_score(self) -> float:
        return np.mean(self.cooperative_scores) if self.cooperative_scores else np.nan

    @property
    def avg_aggressive_score(self) -> float:
        return np.mean(self.aggressive_scores) if self.aggressive_scores else np.nan

    @property
    def avg_social_welfare(self) -> float:
        all_scores = self.cooperative_scores + self.aggressive_scores
        return np.mean(all_scores) if all_scores else np.nan


class MixtureTournament:
    """Tournament testing different mixtures of cooperative vs aggressive players for a single group size."""

    def __init__(self,
                 cooperative_players: List[BasePlayer],
                 aggressive_players: List[BasePlayer],
                 config: MixtureTournamentConfig):

        self.cooperative_players = cooperative_players
        self.aggressive_players = aggressive_players
        self.config = config

        # Setup logging
        self.logger = logging.getLogger(__name__)

        group_size = config.game_description.n_players

        # Validate we have enough strategies
        if len(cooperative_players) < group_size:
            raise ValueError(f"Need at least {group_size} cooperative players, got {len(cooperative_players)}")
        if len(aggressive_players) < group_size:
            raise ValueError(f"Need at least {group_size} aggressive players, got {len(aggressive_players)}")

        # Stats storage - organized by (n_cooperative, n_aggressive)
        self.mixture_stats: Dict[tuple, MixtureStats] = {}

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
            self._run_mixture(n_cooperative, n_aggressive)

        return self._create_results_dataframe()

    def _run_mixture(self, n_cooperative: int, n_aggressive: int):
        """Run multiple matches for a specific mixture."""
        mixture_key = (n_cooperative, n_aggressive)

        self.logger.info(f"Testing mixture: {mixture_key}")

        for match_num in range(self.config.matches_per_mixture):
            # Create players for this match
            match_players = self._create_match_players(n_cooperative, n_aggressive)
            match_id = f"match_{mixture_key}_{match_num:04d}"

            result = self._run_match(match_players, mixture_key, match_id)

    def _run_match(self, players: list[BasePlayer], mixture_key, match_id: str) -> MatchResult:
        # Run the match
        game = self.config.game_class(players, self.config.game_description)
        result = game.play_game()

        # Record stats immediately with known player types
        self._record_match_stats(mixture_key, players, result)

        return MatchResult(
            match_id=match_id,
            game_result=game_result,
            timestamp=datetime.now()
        )

    def _create_match_players(self, n_cooperative: int, n_aggressive: int) -> List[BasePlayer]:
        """Create players for a single match by sampling from available strategies."""
        players = []

        # Sample cooperative players
        if n_cooperative > 0:
            players.extend(random.sample(self.cooperative_players, n_cooperative))

        # Sample aggressive players
        if n_aggressive > 0:
            players.extend(random.sample(self.aggressive_players, n_aggressive))

        # Shuffle to randomize positions
        random.shuffle(players)
        return players

    def _record_match_stats(self, mixture_key: tuple, players: List[BasePlayer], result: GameResult):
        """Record statistics for a completed match."""
        stats = self.mixture_stats[mixture_key]
        total_payoffs = result.history.total_payoffs()

        # Record payoffs by player type
        for player, payoff in zip(players, total_payoffs):
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

    def _create_results_dataframe(self) -> pd.DataFrame:
        """Create DataFrame from collected statistics."""
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
