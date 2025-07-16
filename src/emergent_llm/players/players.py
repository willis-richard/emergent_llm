"""Player classes for social dilemma experiments."""
from abc import ABC, abstractmethod
from typing import Callable, Optional

from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.history import PlayerHistory


class BasePlayer(ABC):
    """Abstract base class for players in social dilemma games."""

    def __init__(self, name: str = None, **kwargs):
        """Initialize player with name and strategy parameters."""
        self.name = name or self.__class__.__name__
        self.init_kwargs = kwargs
        self.reset()

    def reset(self):
        """Reset player to initial state."""
        # Override in subclasses if needed
        pass

    @abstractmethod
    def strategy(self, history: PlayerHistory) -> Action:
        """
        Player's strategy function.

        Args:
            history: Player-specific view of game history

        Returns:
            Action: C (cooperate) or D (defect)
        """
        pass

    def clone(self):
        """Create a copy of this player."""
        cls = self.__class__
        new_player = cls(name=self.name, **self.init_kwargs)
        return new_player

    def __repr__(self):
        """String representation of the player."""
        return f"{self.__class__.__name__}({self.name})"


class LLMPlayer(BasePlayer):
    """Player that uses an LLM-generated strategy."""

    def __init__(self, name: str, strategy_function: Callable,
                 attitude: Attitude, strategy_description: str = "", **kwargs):
        """
        Initialize LLM player with generated strategy.

        Args:
            name: Player name
            strategy_function: Python function implementing the strategy
            attitude: Player's attitude (cooperative/aggressive)
            strategy_description: Natural language description of strategy
        """
        super().__init__(name=name, **kwargs)
        self.strategy_function = strategy_function
        self.strategy_description = strategy_description
        self.attitude = attitude


    def strategy(self, history: PlayerHistory) -> Action:
        """Execute the LLM-generated strategy."""
        return self.strategy_function(history)

    def reset(self):
        """Reset strategy state."""
        self.strategy_state = {}

    def clone(self):
        """Create a copy of this player."""
        return LLMPlayer(
            name=self.name,
            strategy_function=self.strategy_function,
            attitude=self.attitude,
            strategy_description=self.strategy_description,
            **self.init_kwargs
        )

    def __repr__(self):
        """String representation of the player."""
        return f"LLMPlayer({self.name}, {self.attitude})"


class SimplePlayer(BasePlayer):
    """Simple player for testing with no-argument strategy function."""

    def __init__(self, name: str, strategy_func: Callable[[], Action], **kwargs):
        """
        Initialize simple player with a no-argument strategy function.

        Args:
            name: Player name
            strategy_func: Function that takes no arguments and returns Action.
                          Defaults to always cooperate.
        """
        super().__init__(name=name, **kwargs)
        self.strategy_func = strategy_func

    def strategy(self, history: PlayerHistory) -> Action:
        """Execute the strategy function (ignoring game context)."""
        return self.strategy_func()
