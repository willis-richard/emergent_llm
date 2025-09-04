from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import logging
import pandas as pd
import numpy as np

from emergent_llm.games import (BaseGame, GameResult,
                                PublicGoodsDescription, PublicGoodsGame,
                                CollectiveRiskDescription, CollectiveRiskGame,
                                CommonPoolDescription, CommonPoolGame)
from emergent_llm.common import GameDescription
from emergent_llm.players import LLMPlayer


@dataclass
class MatchResult:
    """Results from a single match."""
    match_id: str
    player_ids: list[tuple[str, str, str]]
    payoffs: list[float]
    cooperations: list[int]


@dataclass
class BaseTournamentConfig:
    game_description: GameDescription
    repetitions: int = 1

    def get_game_class(self) -> type[BaseGame]:
        """Get appropriate game class from description type."""
        if isinstance(self.game_description, PublicGoodsDescription):
            return PublicGoodsGame
        elif isinstance(self.game_description, CollectiveRiskDescription):
            return CollectiveRiskGame
        elif isinstance(self.game_description, CommonPoolDescription):
            return CommonPoolGame
        else:
            raise ValueError(f"No game class found for description type: {type(self.game_description)}")



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
            player_ids=[p.id() for p in players],
            payoffs=list(game_result.total_payoffs),
            cooperations=list(game_result.total_cooperations),
        )

        # Store match result
        self.match_results.append(match_result)

        return match_result

    @abstractmethod
    def run_tournament(self):
        """Run the tournament and return results."""
        pass
