from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import logging
import pandas as pd
import numpy as np

from emergent_llm.games import BaseGame, GameResult
from emergent_llm.common import GameDescription
from emergent_llm.players import BasePlayer
from emergent_llm.tournament.results import MatchResult


@dataclass
class BaseTournamentConfig:
    game_class: type[BaseGame]
    game_description: GameDescription
    repetitions: int = 1


class BaseTournament(ABC):
    """Base class for all tournament types."""

    def __init__(self, config: BaseTournamentConfig):
        self.config: BaseTournamentConfig = config
        self.logger = logging.getLogger(self.__class__.__name__)

        # Results storage
        self.match_results: list[MatchResult] = []

    def _run_match(self, players: list[BasePlayer], match_id: str) -> MatchResult:
        """Run a single match and record results."""
        # Create and run game
        game = self.config.game_class(players, self.config.game_description)
        game_result = game.play_game()

        # Create match result
        match_result = MatchResult(
            match_id=match_id,
            players=[p.name for p in players],
            payoffs=list(game_result.total_payoffs),
            cooperations=list(game_result.total_cooperations),
            timestamp=datetime.now()
        )

        # Store match result
        self.match_results.append(match_result)

        return match_result

    @abstractmethod
    def run_tournament(self) -> pd.DataFrame:
        """Run the tournament and return results."""
        pass

    @abstractmethod
    def create_results_dataframe(self) -> pd.DataFrame:
        """Output dataframe of results."""
        pass
