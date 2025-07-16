"""Base game class for social dilemma experiments."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from emergent_llm.common.actions import Action, C, D
from emergent_llm.players import BasePlayer


@dataclass
class GameResult:
    """Results from a single game."""
    players: list[str]  # Player names/IDs
    history: list[list[Action]]  # Round-by-round actions for each player
    payoffs: list[float]  # Final payoffs for each player
    round_payoffs: list[list[float]]  # Payoffs for each round
    game_parameters: dict[str, any]


class BaseGame(ABC):
    """Abstract base class for social dilemma games."""

    def __init__(self, players: list[BasePlayer], **kwargs):
        """Initialize game with players and parameters."""
        self.players = players
        self.n_players = len(players)
        self.game_parameters = kwargs

        # Initialize game state
        self.history = []  # List of rounds, each round is list of actions
        self.payoffs = [0.0] * self.n_players
        self.round_payoffs = []  # Track payoffs per round
        self.current_round = 0

    @abstractmethod
    def calculate_payoffs(self, actions: list[Action]) -> list[float]:
        """Calculate payoffs for a single round given actions."""
        pass

    @abstractmethod
    def game_description(self) -> dict[str, any]:
        """Return game parameters and rules for strategy generation."""
        pass

    def play_round(self) -> list[Action]:
        """Play a single round of the game."""
        # Get actions from each player
        actions = [
            player.strategy(self.history.for_player(i))
            for i, player in enumerate(self.players)
        ]

        # Calculate payoffs for this round
        round_payoffs = self.calculate_payoffs(actions)

        # Update game state
        self.history.append(actions)
        self.round_payoffs.append(round_payoffs)
        self.current_round += 1

        # Add to cumulative payoffs
        for i, payoff in enumerate(round_payoffs):
            self.payoffs[i] += payoff

        return actions

    def play_game(self, rounds: int) -> GameResult:
        """Play a complete game for specified number of rounds."""
        for _ in range(rounds):
            self.play_round()

        return GameResult(
            players=[player.name for player in self.players],
            history=self.history.copy(),
            payoffs=self.payoffs.copy(),
            round_payoffs=self.round_payoffs.copy(),
            game_parameters=self.game_parameters
        )

    def reset(self):
        """Reset game to initial state."""
        self.history = []
        self.payoffs = [0.0] * self.n_players
        self.round_payoffs = []
        self.current_round = 0

        # Reset all players
        for player in self.players:
            player.reset()
