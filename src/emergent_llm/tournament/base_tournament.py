import logging
from abc import ABC, abstractmethod

from emergent_llm.players import LLMPlayer
from emergent_llm.tournament.configs import BaseTournamentConfig
from emergent_llm.tournament.results import MatchResult


class BaseTournament(ABC):
    """Base class for all tournament types."""

    def __init__(self, config: BaseTournamentConfig):
        self.config: BaseTournamentConfig = config
        self.logger = logging.getLogger(self.__class__.__name__)

        # Results storage
        self.match_results: list[MatchResult] = []

    def _run_match(self, players: list[LLMPlayer], match_id: str) -> MatchResult:
        """Run a single match and record results."""
        # Create and run game
        game_class = self.config.get_game_class()
        game = game_class(players, self.config.game_description)
        game_result = game.play_game()

        # Create match result
        match_result = MatchResult(
            match_id=match_id,
            player_ids=[p.id for p in players],
            total_payoffs=list(game_result.total_payoffs),
            total_cooperations=list(game_result.total_cooperations),
        )

        # Store match result
        self.match_results.append(match_result)
        self.logger.debug(f"{match_result}")

        return match_result

    @abstractmethod
    def run_tournament(self):
        """Run the tournament and return results."""
