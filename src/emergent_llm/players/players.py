"""Player classes for social dilemma experiments."""
import logging
from dataclasses import dataclass
from typing import Callable

from emergent_llm.common import (Action, Attitude, GameDescription, GameState,
                                 Gene, PlayerHistory, PlayerId)
from emergent_llm.players.base_player import BasePlayer, BaseStrategy


class LLMPlayer(BasePlayer):
    """Player that uses an LLM-generated strategy."""

    def __init__(self, name: str, gene: Gene,
                 game_description: GameDescription,
                 strategy_class: type[BaseStrategy],
                 max_errors: int=2):
        """
        Initialise LLM player with generated strategy.

        Args:
            name: Player name
            attitude: Player's attitude (collective/exploitative)
            game_description: Game description
            strategy_class: Callable class implementing the strategy
            max_errors: Number of tolerated errors
        """
        super().__init__(name)
        self.gene = gene
        self.id = PlayerId(name, gene, f"{strategy_class.__module__}.{strategy_class.__name__}")
        self.game_description: GameDescription = game_description
        self.strategy_class: type[BaseStrategy] = strategy_class

        # Setup logging
        self.logger = logging.getLogger(f"{repr(self)}")

        # Error tracking (reset per game)
        self.error_count = 0
        self.max_errors = max_errors

        self.reset()

    def reset(self):
        """Reset for a new game."""
        self.strategy_function = self.strategy_class(self.game_description)
        self.error_count = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        """Execute the strategy function with limited error handling."""
        try:
            action = self.strategy_function(state, history)

            # Validate the returned action
            if not isinstance(action, Action):
                raise TypeError(f"Strategy returned {type(action).__name__} instead of Action")

            return action

        except Exception as e:
            self.error_count += 1

            # Log the error with context
            round_info = "first round" if history is None else f"round {history.round_number + 1}"
            self.logger.warning(
                f"Strategy {self.strategy_class.__name__} error #{self.error_count} at {round_info}: "
                f"{e.__class__.__name__}: {e}"
            )

            # Only allow 2 fallbacks, then let it crash
            if self.error_count > self.max_errors:
                self.logger.error(f"Strategy {self.strategy_class.__name__} exceeded error limit")
                raise

            # Return fallback action based on attitude
            return Action.C if self.id.attitude == Attitude.COLLECTIVE else Action.D

    def __repr__(self):
        """String representation of the player."""
        return f"{self.__class__.__name__}({self.id})"

    def __del__(self):
        """Clean up strategy function reference."""
        if hasattr(self, 'strategy_function'):
            del self.strategy_function


class SimplePlayer(BasePlayer):
    """Simple player for testing with no-argument strategy function."""

    def __init__(self, name: str, strategy_function: Callable[[], Action]):
        """
        Initialize simple player with a no-argument strategy function.

        Args:
            name: Player name
            strategy_func: Function that takes no arguments and returns Action.
                          Defaults to always cooperate.
        """
        super().__init__(name)
        self.strategy_function = strategy_function

    def reset(self):
        pass

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        """Execute the strategy function (ignoring game context)."""
        return self.strategy_function()


@dataclass(frozen=True)
class StrategySpec:
    """Associates a strategy class with its generating gene."""
    gene: Gene
    strategy_class: type[BaseStrategy]

    def create_player(self, name: str, game_description: GameDescription) -> LLMPlayer:
        """Convenience method to create a player from this spec."""
        return LLMPlayer(
            name=name,
            gene=self.gene,
            game_description=game_description,
            strategy_class=self.strategy_class
        )

    def __str__(self) -> str:
        return f"{self.gene}:{self.strategy_class.__name__}"
