"""Player classes for social dilemma experiments."""
from abc import ABC, abstractmethod

from emergent_llm.common import (Action, GameDescription, GameState,
                                 PlayerHistory, PlayerId)


class BaseStrategy(ABC):
    """Abstract base class for strategies, which are callable classes."""

    @abstractmethod
    def __init__(self, game_description: GameDescription):
        """For initialising member variables. Names need to be unique"""

    @abstractmethod
    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        """For computing the action"""


class BasePlayer(ABC):
    """Abstract base class for players in social dilemma games."""

    def __init__(self, name: str):
        self.id = PlayerId(name, None, None)

    @abstractmethod
    def reset(self):
        """
        Prepare for a new game
        """

    @abstractmethod
    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        """
        Player's strategy function.

        Args:
            state: dataclass of game specific state, e.g. capacity for CommonPool
            history: Player-specific view of game history

        Returns:
            Action: C (cooperate) or D (defect)
        """

    def __repr__(self):
        """String representation of the player."""
        return f"{self.id.name}[{self.__class__.__name__}]"
