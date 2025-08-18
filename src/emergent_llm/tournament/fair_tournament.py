"""Fair tournament system where all players play equal number of games."""
import logging
import random
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from datetime import datetime

from emergent_llm.games.base_game import BaseGame, GameResult, GameDescription
from emergent_llm.players.base_player import BasePlayer


@dataclass
class FairTournamentConfig:
    """Configuration for fair tournament."""
    game_class: type[BaseGame]
    game_description: GameDescription
    repetitions: int = 1  # Number of times to repeat the tournament


@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    repetition: int
    game_result: GameResult
    timestamp: datetime


@dataclass
class PlayerStats:
    """Statistics for a single player across all games."""
    player_name: str
    player_repr: str
    payoffs: List[float] = field(default_factory=list)
    cooperations: List[int] = field(default_factory=list)

    @property
    def games_played(self) -> int:
        return len(self.payoffs)

    @property
    def mean_payoff(self) -> float:
        return float(np.mean(self.payoffs)) if self.payoffs else 0.0

    @property
    def std_payoff(self) -> float:
        return float(np.std(self.payoffs)) if len(self.payoffs) > 1 else 0.0

    @property
    def mean_cooperations(self) -> float:
        return float(np.mean(self.cooperations)) if self.cooperations else 0.0

    @property
    def total_payoff(self) -> float:
        return sum(self.payoffs)

    @property
    def total_cooperations(self) -> int:
        return sum(self.cooperations)


class FairTournament:
    """Fair tournament where all players play equal number of games."""

    def __init__(self, players: list[BasePlayer], config: FairTournamentConfig):
        # Validate population size
        n_players = config.game_description.n_players
        if len(players) % n_players != 0:
            raise ValueError(
                f"Population size ({len(players)}) must be divisible by "
                f"n_players ({n_players})"
            )

        self.players: list[BasePlayer] = players
        self.config: FairTournamentConfig = config

        # Calculate matches per repetition
        self.matches_per_repetition = len(players) // n_players

        # Results storage
        self.match_results: list[MatchResult] = []
        self.player_stats: dict[str, PlayerStats] = {
            player.name: PlayerStats(
                player_name=player.name,
                player_repr=repr(player)
            )
            for player in self.players
        }

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initialized fair tournament: {len(players)} players, "
            f"{n_players} per game, {self.matches_per_repetition} matches per repetition, "
            f"{config.repetitions} repetitions"
        )

    def run_tournament(self) -> pd.DataFrame:
        """Run complete tournament with all repetitions."""
        self.logger.info(
            f"Starting tournament: {self.config.repetitions} repetitions × "
            f"{self.matches_per_repetition} matches"
        )

        for repetition in range(self.config.repetitions):
            self._run_repetition(repetition)

        # Log summary statistics
        self._log_summary()

        return self._create_results_dataframe()

    def _run_repetition(self, repetition: int):
        """Run a single repetition of the tournament."""
        self.logger.info(f"Starting repetition {repetition + 1}/{self.config.repetitions}")

        shuffled_players = self.players.copy()
        random.shuffle(shuffled_players)

        # Run matches for this repetition
        n_players = self.config.game_description.n_players
        for match_num in range(self.matches_per_repetition):
            start_idx = match_num * n_players
            end_idx = start_idx + n_players
            match_players = shuffled_players[start_idx:end_idx]

            match_id = f"rep{repetition:02d}_match{match_num:04d}"
            self._run_match(match_players, match_id, repetition)

    def _run_match(self, players: list[BasePlayer], match_id: str, repetition: int):
        """Run a single match and record results."""
        # Create and run game
        game = self.config.game_class(players, self.config.game_description)

        # Log match start (debug level to reduce noise)
        player_names = [p.name for p in players]
        self.logger.debug(f"Match {match_id}: {player_names}")

        # Play game
        game_result = game.play_game()

        # Update player statistics
        for player, payoff, cooperations in zip(
            players,
            game_result.total_payoffs,
            game_result.total_cooperations
        ):
            stats = self.player_stats[player.name]
            stats.payoffs.append(payoff)
            stats.cooperations.append(cooperations)

        # Store match result
        match_result = MatchResult(
            match_id=match_id,
            repetition=repetition,
            game_result=game_result,
            timestamp=datetime.now()
        )
        self.match_results.append(match_result)

        # Optional detailed logging (debug level)
        if self.logger.isEnabledFor(logging.DEBUG):
            game_result.log_match_result(match_id, self.logger)

    def _log_summary(self):
        """Log summary statistics after tournament completion."""
        total_matches = len(self.match_results)
        self.logger.info(f"Tournament complete: {total_matches} total matches")

        # Log player statistics summary
        stats_summary = []
        for stats in self.player_stats.values():
            stats_summary.append({
                'player': stats.player_name[:20],  # Truncate long names
                'games': stats.games_played,
                'mean_payoff': f"{stats.mean_payoff:.2f}",
                'std_payoff': f"{stats.std_payoff:.2f}",
                'mean_coop': f"{stats.mean_cooperations:.2f}"
            })

        if stats_summary and self.logger.isEnabledFor(logging.INFO):
            df = pd.DataFrame(stats_summary)
            self.logger.info(f"Player statistics:\n{df.to_string(index=False)}")

    def _create_results_dataframe(self) -> pd.DataFrame:
        """Create summary DataFrame from player statistics."""
        rows = []
        for stats in self.player_stats.values():
            rows.append({
                'player_name': stats.player_name,
                'player_repr': stats.player_repr,
                'games_played': stats.games_played,
                'mean_payoff': stats.mean_payoff,
                'std_payoff': stats.std_payoff,
                'mean_cooperations': stats.mean_cooperations,
                'total_payoff': stats.total_payoff,
                'total_cooperations': stats.total_cooperations
            })

        return pd.DataFrame(rows)

    def get_detailed_results(self) -> pd.DataFrame:
        """Get detailed match-by-match results."""
        rows = []
        for match_result in self.match_results:
            game_result = match_result.game_result
            for i, player_name in enumerate(game_result.player_ids):
                rows.append({
                    'match_id': match_result.match_id,
                    'repetition': match_result.repetition,
                    'timestamp': match_result.timestamp,
                    'player_name': player_name,
                    'payoff': game_result.total_payoffs[i],
                    'cooperations': game_result.total_cooperations[i]
                })

        return pd.DataFrame(rows)
