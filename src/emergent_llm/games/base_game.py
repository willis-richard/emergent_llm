"""Base game class for social dilemma experiments."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from emergent_llm.common import Action, GameDescription, GameHistory
from emergent_llm.players.base_player import BasePlayer


@dataclass
class GameResult:
    """Results from a single game."""
    player_names: list[str]
    total_payoffs: list[float]
    total_cooperations: list[int]
    cooperations_by_round: list[int]
    history: GameHistory
    description: GameDescription


class BaseGame(ABC):
    """Abstract base class for social dilemma games."""

    def __init__(self, players: Sequence[BasePlayer],
                 description: GameDescription):
        if len(players) != description.n_players:
            raise ValueError(
                f"Number of players ({len(players)}) must match "
                f"description.n_players ({description.n_players})"
            )

        self.players: Sequence[BasePlayer] = players
        self.description: GameDescription = description
        self.history: GameHistory = GameHistory(
            n_rounds=self.description.n_rounds,
            n_players=self.description.n_players,
        )

    @abstractmethod
    def _calculate_payoffs(
            self, actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round given actions."""

    def get_current_stock(self):
        return None

    def _play_round(self, players: Sequence[BasePlayer]) -> None:
        """Play a single round, recording into self.history."""
        stock = self.get_current_stock()

        action_enums = [
            player(history=self.history.for_player(i), current_stock=stock)
            for i, player in enumerate(players)
        ]

        actions = Action.to_bool_array(action_enums)
        payoffs = self._calculate_payoffs(actions)
        self.history.record(actions, payoffs)

    def play_game(self) -> GameResult:
        """Play a complete game for the number of rounds in description."""
        self.reset()

        for _ in range(self.description.n_rounds):
            self._play_round(self.players)

        return GameResult(
            player_names=[p.id.name for p in self.players],
            total_payoffs=self.history.total_payoffs(),
            total_cooperations=self.history.total_cooperations(),
            cooperations_by_round=self.history.cooperations_by_round(),
            history=self.history,
            description=self.description,
        )

    def reset(self) -> None:
        """Prepare for a new game. Safe to call repeatedly to reuse the game object."""
        self.history = GameHistory(
            n_rounds=self.description.n_rounds,
            n_players=self.description.n_players,
        )
        for player in self.players:
            player.reset()
