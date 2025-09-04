import random
import pandas as pd

from emergent_llm.tournament.base_tournament import BaseTournament, BaseTournamentConfig
from emergent_llm.tournament.results import FairTournamentResults, PlayerStats, MatchResult
from emergent_llm.players import LLMPlayer


class FairTournament(BaseTournament):
    """Fair tournament where all players play equal number of games."""

    def __init__(self, players: list[LLMPlayer], config: BaseTournamentConfig):
        super().__init__(config)

        # Validate population size
        if len(players) % config.game_description.n_players != 0:
            raise ValueError(
                f"Population size ({len(players)}) must be divisible by "
                f"n_players ({config.game_description.n_players})"
            )

        self.players = players

    def run_tournament(self) -> FairTournamentResults:
        """Run complete tournament and return results."""
        self.logger.info(f"Starting fair tournament: {self.config.repetitions} repetitions")

        for repetition in range(self.config.repetitions):
            self._run_repetition(repetition)

        return FairTournamentResults(
            config=self.config,
            player_ids=[p.id() for p in self.players],
            match_results=self.match_results
        )

    def _run_repetition(self, repetition: int):
        """Run a single repetition of the tournament."""
        shuffled_players = self.players.copy()
        random.shuffle(shuffled_players)

        n_players = self.config.game_description.n_players
        matches_per_repetition = len(self.players) // n_players

        for match_num in range(matches_per_repetition):
            start_idx = match_num * n_players
            end_idx = start_idx + n_players
            match_players = shuffled_players[start_idx:end_idx]

            match_id = f"rep{repetition:02d}_match{match_num:04d}"
            self._run_match(match_players, match_id)
