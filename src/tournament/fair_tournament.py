"""Fair tournament system where all players play equal number of games."""
import logging
import random
from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

from ..games.base_game import BaseGame, GameResult
from ..players import BasePlayer


@dataclass
class FairTournamentConfig:
    """Configuration for fair tournament."""
    n_players: int = 6
    n_rounds: int = 20

    def __post_init__(self):
        """Validate configuration."""
        if self.n_players <= 0:
            raise ValueError("n_players must be positive")


@dataclass
class FairMatchResult:
    """Results from a single match."""
    match_id: str
    game_result: GameResult
    timestamp: datetime
    players: List[BasePlayer]  # Store player references


class FairTournament:
    """Fair tournament where all players play equal number of games."""

    def __init__(self, players: List[BasePlayer], config: FairTournamentConfig,
                 game_class: type[BaseGame], game_kwargs: Dict[str, Any] = None):
        """Initialize tournament."""
        # Validate population size
        if len(players) % config.n_players != 0:
            raise ValueError(
                f"Population size ({len(players)}) must be divisible by "
                f"n_players ({config.n_players})"
            )

        self.players = players
        self.config = config
        self.game_class = game_class
        self.game_kwargs = game_kwargs or {}

        # Results storage
        self.results: List[FairMatchResult] = []

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized tournament with {len(players)} players")

    def run_tournament(self) -> pd.DataFrame:
        """Run tournament with fair player distribution."""
        total_players = len(self.players)
        n_matches = total_players // self.config.n_players

        self.logger.info(f"Starting fair tournament: {total_players} players, {n_matches} matches")

        # Create random permutation of all players
        shuffled_players = self.players.copy()
        random.shuffle(shuffled_players)

        all_results = []

        # Divide players into groups
        for match_num in range(n_matches):
            start_idx = match_num * self.config.n_players
            end_idx = start_idx + self.config.n_players

            match_players = shuffled_players[start_idx:end_idx]
            match_id = f"match_{match_num:04d}"

            try:
                result = self._run_match(match_players, match_id)
                all_results.append(result)

            except Exception as e:
                self.logger.error(f"Error in match {match_id}: {e}")
                continue

        self.results = all_results

        # Convert to DataFrame for analysis
        return self._results_to_dataframe()

    def _run_match(self, players: List[BasePlayer], match_id: str) -> FairMatchResult:
        """Run a single match with given players."""
        # Create game instance
        game = self.game_class(players, **self.game_kwargs)

        # Log match start
        player_names = [p.name for p in players]
        self.logger.info(f"Starting match {match_id} with players: {player_names}")

        # Play game
        game_result = game.play_game(self.config.n_rounds)

        # Create match result
        match_result = FairMatchResult(
            match_id=match_id,
            game_result=game_result,
            timestamp=datetime.now(),
            players=players
        )

        # Log results
        self._log_match_result(match_result)

        return match_result

    def _log_match_result(self, result: FairMatchResult):
        """Log detailed match results."""
        self.logger.info(f"Match {result.match_id} completed")

        # Log individual payoffs
        for i, (player, payoff) in enumerate(zip(result.players, result.game_result.payoffs)):
            self.logger.info(f"  {player.name}: {payoff:.3f}")

        avg_payoff = sum(result.game_result.payoffs) / len(result.game_result.payoffs)
        self.logger.info(f"  Average payoff: {avg_payoff:.3f}")

    def _results_to_dataframe(self) -> pd.DataFrame:
        """Convert tournament results to DataFrame for analysis."""
        rows = []

        for result in self.results:
            base_row = {
                'match_id': result.match_id,
                'timestamp': result.timestamp,
                'game_parameters': str(result.game_result.game_parameters)
            }

            # Add individual player results
            for i, (player, payoff) in enumerate(zip(result.players, result.game_result.payoffs)):
                row = base_row.copy()
                row.update({
                    'player_name': player.name,
                    'player_type': player.__class__.__name__,
                    'payoff': payoff,
                    'position': i
                })
                rows.append(row)

        return pd.DataFrame(rows)
