import random
import pandas as pd
import numpy as np
from dataclasses import dataclass, field

from src.emergent_llm.base_tournament import BaseTournament, BaseTournamentConfig
from src.emergent_llm.players import BasePlayer
from emergent_llm.games import GameResult


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


class FairTournament(BaseTournament):
    """Fair tournament where all players play equal number of games."""

    def __init__(self, players: list[BasePlayer], config: BaseTournamentConfig):
        super().__init__(config)

        # Validate population size
        if len(players) % config.game_description.n_players != 0:
            raise ValueError(
                f"Population size ({len(players)}) must be divisible by "
                f"n_players ({config.game_description.n_players})"
            )

        self.players = players

        # Initialize player statistics storage
        self.player_stats: dict[str, PlayerStats] = {}

    def run_tournament(self) -> pd.DataFrame:
        """Run complete tournament with all repetitions."""
        self.logger.info(f"Starting fair tournament: {self.repetitions} repetitions")

        for repetition in range(self.repetitions):
            self._run_repetition(repetition)

        return self.create_results_dataframe()

    def _run_repetition(self, repetition: int):
        """Run a single repetition of the tournament."""
        shuffled_players = self.players.copy()
        random.shuffle(shuffled_players)

        n_players = self.game_description.n_players
        matches_per_repetition = len(self.players) // n_players

        for match_num in range(matches_per_repetition):
            start_idx = match_num * n_players
            end_idx = start_idx + n_players
            match_players = shuffled_players[start_idx:end_idx]

            match_id = f"rep{repetition:02d}_match{match_num:04d}"
            game_result = self._run_match(match_players, match_id)

            # Update player statistics
            self._update_player_stats(shuffled_players, game_result)

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
        # Sort by mean payoff descending
        df = pd.DataFrame(rows)
        return df.sort_values('mean_payoff', ascending=False).reset_index(drop=True)
