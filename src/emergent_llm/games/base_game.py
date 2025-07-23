"""Base game class for social dilemma experiments."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from emergent_llm.common.game_description import GameDescription
from emergent_llm.common.history import GameHistory
from emergent_llm.players.base_player import BasePlayer


@dataclass
class GameResult:
    """Results from a single game."""
    players: list[str]  # Player names/IDs
    history: GameHistory  # Complete game history
    description: GameDescription  # Game parameters and rules


class BaseGame(ABC):
    """Abstract base class for social dilemma games."""

    def __init__(self, players: list[BasePlayer],
                 description: GameDescription):
        """Initialize game with players and description."""
        if len(players) != description.n_players:
            raise ValueError(
                f"Number of players ({len(players)}) must match "
                f"description.n_players ({description.n_players})"
            )

        self.players: list[BasePlayer] = players
        self.description: GameDescription = description
        self.n_players: int = len(players)

        # Initialize game state
        self.history: GameHistory | None = None
        self.current_round: int = 0

    @abstractmethod
    def _calculate_payoffs(self, actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round given actions."""

    def _play_round(self, players: list[BasePlayer]):
        """Play a single round of the game."""
        if self.history is None:
            # Get actions from each player
            actions = np.array([player(None).value for player in players])

        else:
            # Get actions from each player
            actions = np.array([player(self.history.for_player(i)).value
                                for i, player in enumerate(players)], dtype=np.bool_)

        # Calculate payoffs for this round
        payoffs = self._calculate_payoffs(actions)

        if self.history is None:
            self.history = GameHistory(
                actions=actions,
                payoffs=payoffs
               )
        else:
            self.history.update(actions, payoffs)

        self.current_round += 1

    def play_game(self) -> GameResult:
        """Play a complete game for the number of rounds specified in description."""
        for player in self.players:
            player.reset()

        for _ in range(self.description.n_rounds):
            self._play_round(self.players)

        assert self.history is not None

        return GameResult(
            players=[player.name for player in self.players],
            history=self.history,
            description=self.description
        )

    def reset(self):
        """Reset game to initial state."""
        self.history = None
        self.current_round = 0
