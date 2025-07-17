"""Player classes for social dilemma experiments."""
from abc import ABC, abstractmethod
from typing import Callable, Optional

from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.history import PlayerHistory
from emergent_llm.games.game_description import GameDescription


class BasePlayer(ABC):
    """Abstract base class for players in social dilemma games."""

    def __init__(self, name: str):
        """Initialize player with a name."""
        self.name = name

    @abstractmethod
    def clone(self):
        """Reset player to initial state."""
        # Override in subclasses if needed
        pass

    @abstractmethod
    def strategy(self, game_description: GameDescription, history: PlayerHistory) -> Action:
        """
        Player's strategy function.

        Args:
            history: Player-specific view of game history

        Returns:
            Action: C (cooperate) or D (defect)
        """
        pass

    def __repr__(self):
        """String representation of the player."""
        return f"{self.__class__.__name__}({self.name})"


class LLMPlayer(BasePlayer):
    """Player that uses an LLM-generated strategy."""

    def __init__(self, name: str, attitude: Attitude,
                 strategy_function: Callable):
        """
        Initialize LLM player with generated strategy.

        Args:
            name: Player name
            attitude: Player's attitude (cooperative/aggressive)
            strategy_function: Python function implementing the strategy
        """
        super().__init__(name=name)
        self.attitude = attitude
        self.strategy_function = strategy_function


    def strategy(self, game_description: GameDescription, history: PlayerHistory) -> Action:
        """Execute the LLM-generated strategy."""
        return self.strategy_function(game_description, history)

    def clone(self):
        """Create a copy of this player."""
        return LLMPlayer(
            name=self.name,
            attitude=self.attitude,
            strategy_function=self.strategy_function,
        )

    def __repr__(self):
        """String representation of the player."""
        return f"LLMPlayer({self.name}, {self.attitude})"


class SimplePlayer(BasePlayer):
    """Simple player for testing with no-argument strategy function."""

    def __init__(self, name: str, strategy_function: Callable[[], Action], **kwargs):
        """
        Initialize simple player with a no-argument strategy function.

        Args:
            name: Player name
            strategy_func: Function that takes no arguments and returns Action.
                          Defaults to always cooperate.
        """
        super().__init__(name=name, **kwargs)
        self.strategy_function = strategy_function

    def strategy(self, game_description: GameDescription, history: PlayerHistory) -> Action:
        """Execute the strategy function (ignoring game context)."""
        return self.strategy_function()


    def clone(self):
        """Create a copy of this player."""
        return SimplePlayer(
            name=self.name,
            strategy_function=self.strategy_function,
        )
