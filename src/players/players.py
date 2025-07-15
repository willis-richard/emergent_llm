"""Player classes for social dilemma experiments."""
from abc import ABC, abstractmethod
from typing import Callable

from ..common.actions import Action, C, D


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
    def strategy(self, history: list[list[Action]], player_index: int,
                game_info: dict[str, any]) -> Action:
        """
        Player's strategy function.

        Args:
            history: List of previous rounds, each round is list of actions
            player_index: This player's index in the game
            game_info: Game parameters and rules

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
                 strategy_description: str = "", attitude: str = "neutral", **kwargs):
        """
        Initialize LLM player with generated strategy.

        Args:
            name: Player name
            strategy_function: Python function implementing the strategy
            strategy_description: Natural language description of strategy
            attitude: "cooperative", "aggressive", or "neutral"
        """
        super().__init__(name=name, **kwargs)
        self.strategy_function = strategy_function
        self.strategy_description = strategy_description
        self.attitude = attitude

        # Store any additional state the strategy might need
        self.strategy_state = {}

    def strategy(self, history: list[list[Action]], player_index: int,
                game_info: dict[str, any]) -> Action:
        """Execute the LLM-generated strategy."""
        return self.strategy_function(history, player_index, game_info, self.strategy_state)

    def reset(self):
        """Reset strategy state."""
        self.strategy_state = {}


class SimplePlayer(BasePlayer):
    """Simple player for testing with no-argument strategy function."""

    def __init__(self, name: str, strategy_func: Callable[[], Action] = None, **kwargs):
        """
        Initialize simple player with a no-argument strategy function.

        Args:
            name: Player name
            strategy_func: Function that takes no arguments and returns Action.
                          Defaults to always cooperate.
        """
        super().__init__(name=name, **kwargs)
        self.strategy_func = strategy_func or (lambda: C)

    def strategy(self, history: list[list[Action]], player_index: int,
                game_info: dict[str, any]) -> Action:
        """Execute the strategy function (ignoring game context)."""
        return self.strategy_func()
