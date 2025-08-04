"""Fair tournament system where all players play equal number of games."""
import logging
import random
from dataclasses import dataclass
import numpy as np
import pandas as pd
from datetime import datetime

from emergent_llm.games.base_game import BaseGame, GameResult, GameDescription
from emergent_llm.players.base_player import BasePlayer


@dataclass
class MatchConfig:
    game_class: type[BaseGame]
    game_description: GameDescription
    matches_per_player: int


@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    game_result: GameResult
    timestamp: datetime


class FairTournament:
    """Fair tournament where all players play equal number of games."""

    def __init__(self, players: list[BasePlayer], match_config: MatchConfig):
        # Validate population size
        if len(players) % match_config.game_description.n_players != 0:
            raise ValueError(
                f"Population size ({len(players)}) must be divisible by "
                f"n_players ({match_config.game_description.n_players})"
            )

        self.players: list[BasePlayer] = players
        self.match_config: MatchConfig = match_config

        # Results storage
        self.match_results: list[MatchResult] = []
        self.player_stats: dict[BasePlayer, dict[str, list[float]]] = {
            player: {'payoffs': [], 'cooperations': []}
            for player in self.players
        }

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialised tournament with {len(players)} players")

    def run_tournament(self) -> pd.DataFrame:
        """Run tournament with fair player distribution."""
        n_matches = len(self.players) // self.match_config.game_description.n_players

        self.logger.info(f"Starting fair tournament: {n_matches} matches")

        # Create random permutation of all players
        shuffled_players = self.players.copy()
        random.shuffle(shuffled_players)

        # Divide players into groups
        for match_num in range(n_matches):
            start_idx = match_num * self.match_config.game_description.n_players
            end_idx = start_idx + self.match_config.game_description.n_players

            match_players = shuffled_players[start_idx:end_idx]
            match_id = f"match_{match_num:04d}"

            result = self._run_match(match_players, match_id)
            self.match_results.append(result)

        return self._process_stats()

    def _run_match(self, players: list[BasePlayer], match_id: str) -> MatchResult:
        """Run a single match with given players."""
        game = self.match_config.game_class(players, self.match_config.game_description)

        # Log match start
        player_names = [p.name for p in players]
        self.logger.info(f"Starting match {match_id} with players: {player_names}")

        # Play game
        game_result = game.play_game()

        for player, payoff, cooperations in zip(
            players,
            game_result.total_payoffs,
            game_result.total_cooperations
               ):
            self.player_stats[player]['payoffs'].append(payoff)
            self.player_stats[player]['cooperations'].append(cooperations)

        # Use the game's built-in logging
        game_result.log_match_result(match_id, self.logger)

        return MatchResult(
            match_id=match_id,
            game_result=game_result,
            timestamp=datetime.now()
        )

    def _process_stats(self) -> pd.DataFrame:
        """Create summary DataFrame with mean statistics per player."""
        rows = []

        for player, stats in self.player_stats.items():
            rows.append({
                'player_name': player.name,
                'player_repr': repr(player),  # Includes strategy info
                'mean_payoff': np.mean(stats['payoffs']),
                'mean_cooperations': np.mean(stats['cooperations']),
                'games_played': len(stats['payoffs']),
                'total_payoff': sum(stats['payoffs']),
                'total_cooperations': sum(stats['cooperations'])
            })

        return pd.DataFrame(rows)
