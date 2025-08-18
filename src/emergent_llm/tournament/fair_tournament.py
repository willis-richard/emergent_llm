import random
import pandas as pd

from src.emergent_llm.base_tournament import BaseTournament
from emergent_llm.players import BasePlayer
from emergent_llm.games import BaseGame
from emergent_llm.common import GameDescription


class FairTournament(BaseTournament):
    """Fair tournament where all players play equal number of games."""

    def __init__(self, players: list[BasePlayer], game_class: type[BaseGame],
                 game_description: GameDescription, repetitions: int = 1):
        super().__init__(game_class, game_description)

        # Validate population size
        if len(players) % game_description.n_players != 0:
            raise ValueError(
                f"Population size ({len(players)}) must be divisible by "
                f"n_players ({game_description.n_players})"
            )

        self.players = players
        self.repetitions = repetitions
        self.matches_per_repetition = len(players) // game_description.n_players

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
        for match_num in range(self.matches_per_repetition):
            start_idx = match_num * n_players
            end_idx = start_idx + n_players
            match_players = shuffled_players[start_idx:end_idx]

            match_id = f"rep{repetition:02d}_match{match_num:04d}"
            self._run_match(match_players, match_id)
