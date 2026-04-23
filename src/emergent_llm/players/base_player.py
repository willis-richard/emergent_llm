"""Player classes for social dilemma experiments."""
from abc import ABC, abstractmethod

from emergent_llm.common import Action, GameDescription, PlayerHistory, PlayerId


class BaseStrategy(ABC):
    """Abstract base class for strategies. State is game-specific and optional."""

    @abstractmethod
    def __init__(self, game_description: GameDescription):
        """For initialising member variables."""

    @abstractmethod
    def __call__(self, history: PlayerHistory, state=None) -> Action:
        """
        Compute the action for the current round.

        For games without extra state (public_goods, collective_risk), strategies
        should be written as `def __call__(self, history) -> Action` and the
        `state` argument will never be inspected.

        For common_pool, state is a CommonPoolState and strategies should be
        written as `def __call__(self, history, state) -> Action`.
        """


class BasePlayer(ABC):
    """Abstract base class for players in social dilemma games."""

    def __init__(self, name: str):
        self.id = PlayerId(name, None, None)

    @abstractmethod
    def reset(self):
        """Prepare for a new game"""

    @abstractmethod
    def __call__(self, history: PlayerHistory, state=None) -> Action:
        """
        Player's strategy function.

        Args:
            history: Player-specific view of game history
            state: Game-specific state, or None for games without extra state.
        """

    def __repr__(self):
        return f"{self.id.name}[{self.__class__.__name__}]"
