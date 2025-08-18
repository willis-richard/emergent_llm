from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import logging
import pandas as pd
import numpy as np

from emergent_llm.games import BaseGame, GameResult
from emergent_llm.common import GameDescription
from emergent_llm.players import BasePlayer


@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    players: list[str]  # Player names
    payoffs: list[float]
    cooperations: list[int]
    timestamp: datetime


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
        return float(np.mean(self.payoffs))

    @property
    def total_payoff(self) -> float:
        return sum(self.payoffs)

    @property
    def mean_cooperations(self) -> float:
        return float(np.mean(self.cooperations))

    @property
    def total_cooperations(self) -> float:
        return sum(self.cooperations)


class BaseTournament(ABC):
    """Base class for all tournament types."""

    def __init__(self, game_class: type[BaseGame], game_description: GameDescription):
        self.game_class = game_class
        self.game_description = game_description
        self.logger = logging.getLogger(self.__class__.__name__)

        # Results storage
        self.match_results: list[MatchResult] = []
        self.player_stats: dict[str, PlayerStats] = {}

    def _run_match(self, players: list[BasePlayer], match_id: str) -> MatchResult:
        """Run a single match and record results."""
        # Create and run game
        game = self.game_class(players, self.game_description)
        game_result = game.play_game()

        # Create match result
        match_result = MatchResult(
            match_id=match_id,
            players=[p.name for p in players],
            payoffs=list(game_result.total_payoffs),
            cooperations=list(game_result.total_cooperations),
            timestamp=datetime.now()
        )

        # Update player statistics
        self._update_player_stats(players, game_result)

        # Store match result
        self.match_results.append(match_result)

        return match_result

    def _update_player_stats(self, players: list[BasePlayer], game_result: GameResult):
        """Update player statistics with results from a match."""
        for player, payoff, cooperations in zip(
            players, game_result.total_payoffs, game_result.total_cooperations
        ):
            if player.name not in self.player_stats:
                self.player_stats[player.name] = PlayerStats(
                    player_name=player.name,
                    player_repr=repr(player)
                )

            stats = self.player_stats[player.name]
            stats.payoffs.append(payoff)
            stats.cooperations.append(cooperations)

    def create_results_dataframe(self) -> pd.DataFrame:
        """Create summary DataFrame from player statistics."""
        rows = []
        for stats in self.player_stats.values():
            rows.append({
                'player_name': stats.player_name,
                'player_repr': stats.player_repr,
                'games_played': stats.games_played,
                'mean_payoff': stats.mean_payoff,
                'total_payoff': stats.total_payoff,
                'total_cooperations': sum(stats.cooperations),
                'mean_cooperations': np.mean(stats.cooperations) if stats.cooperations else 0.0,
            })
        return pd.DataFrame(rows)

    @abstractmethod
    def run_tournament(self) -> pd.DataFrame:
        """Run the tournament and return results."""
        pass
