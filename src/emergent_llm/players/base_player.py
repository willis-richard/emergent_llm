"""Player classes for social dilemma experiments."""
from abc import ABC, abstractmethod

from emergent_llm.common.actions import Action
from emergent_llm.common.history import PlayerHistory
from emergent_llm.common.game_description import GameDescription


class BaseStrategy(ABC):
    """Abstract base class for strategies, which are callable classes."""

    @abstractmethod
    def __init__(self, game_description: GameDescription):
        """For initialising member variables"""

    @abstractmethod
    def __call__(self, history: None | PlayerHistory) -> Action:
        """For computing the action"""


class BasePlayer(ABC):
    """Abstract base class for players in social dilemma games."""

    def __init__(self, name: str):
        """Initialize player with a name."""
        self.name = name

    @abstractmethod
    def reset(self):
        """
        Prepare for a new game
        """

    @abstractmethod
    def __call__(self, history: None | PlayerHistory) -> Action:
        """
        Player's strategy function.

        Args:
            history: Player-specific view of game history

        Returns:
            Action: C (cooperate) or D (defect)
        """

    def __repr__(self):
        """String representation of the player."""
        return f"{self.__class__.__name__}({self.name})"
