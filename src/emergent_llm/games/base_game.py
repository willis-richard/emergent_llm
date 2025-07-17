"""Base game class for social dilemma experiments."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from emergent_llm.common.actions import Action
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

    def __init__(self, players: list[BasePlayer], description: GameDescription):
        """Initialize game with players and description."""
        if len(players) != description.n_players:
            raise ValueError(
                f"Number of players ({len(players)}) must match "
                f"description.n_players ({description.n_players})"
            )

        self.players = players
        self.description = description
        self.n_players = len(players)

        # Initialize game state
        self.history = GameHistory(
            actions=np.array([]).reshape(0, self.n_players),
            payoffs=np.array([]).reshape(0, self.n_players)
        )
        self.current_round = 0

    @abstractmethod
    def calculate_payoffs(self, actions: list[Action]) -> list[float]:
        """Calculate payoffs for a single round given actions."""

    def play_round(self, players: list[BasePlayer]):
        """Play a single round of the game."""
        # Get actions from each player
        actions = [player(self.history.for_player(i))
                   for i, player in enumerate(self.players)]

        # Calculate payoffs for this round
        round_payoffs = self.calculate_payoffs(actions)

        # Update history with new round
        actions_array = np.array(actions).reshape(1, -1)
        payoffs_array = np.array(round_payoffs).reshape(1, -1)

        if self.history.actions.size == 0:
            # First round
            self.history.actions = actions_array
            self.history.payoffs = payoffs_array
        else:
            # Append to existing history
            self.history.actions = np.vstack([self.history.actions, actions_array])
            self.history.payoffs = np.vstack([self.history.payoffs, payoffs_array])

        self.current_round += 1

    def play_game(self) -> GameResult:
        """Play a complete game for the number of rounds specified in description."""
        players = [p(self.description) for p in self.players]
        for _ in range(self.description.n_rounds):
            self.play_round(players)

        return GameResult(
            players=[player.name for player in players],
            history=self.history,
            description=self.description
        )

    def reset(self):
        """Reset game to initial state."""
        self.history = GameHistory(
            actions=np.array([]).reshape(0, self.n_players),
            payoffs=np.array([]).reshape(0, self.n_players)
        )
        self.current_round = 0
