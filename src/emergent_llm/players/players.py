"""Player classes for social dilemma experiments."""
from typing import Callable

from emergent_llm.common.actions import Action
from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.history import PlayerHistory
from emergent_llm.common.game_description import GameDescription
from emergent_llm.players.base_player import BasePlayer, BaseStrategy


class LLMPlayer(BasePlayer):
    """Player that uses an LLM-generated strategy."""

    def __init__(self, name: str, attitude: Attitude,
                 game_description: GameDescription,
                 strategy_class: type[BaseStrategy]):
        """
        Initialize LLM player with generated strategy.

        Args:
            name: Player name
            attitude: Player's attitude (cooperative/aggressive)
            strategy_class: Callable class implementing the strategy
        """
        super().__init__(name=name)
        self.attitude = attitude
        self.game_description = game_description
        self.strategy_class = strategy_class
        self.reset()

    def reset(self):
        self.strategy_function = self.strategy_class(self.game_description)

    def __call__(self, history: None | PlayerHistory) -> Action:
        """Execute the strategy function (ignoring game context)."""
        return self.strategy_function(history)

    def __repr__(self):
        """String representation of the player."""
        return f"LLMPlayer({self.name}, {self.attitude}, {self.strategy_class.__name__})"

    @property
    def strategy_name(self) -> str:
        """Get the strategy class name."""
        return self.strategy_class.__name__


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

    def reset(self):
        pass

    def __call__(self, history: None | PlayerHistory) -> Action:
        """Execute the strategy function (ignoring game context)."""
        return self.strategy_function()
