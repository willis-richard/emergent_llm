"""Player classes for social dilemma experiments."""
import logging
from dataclasses import dataclass
from typing import Callable

from emergent_llm.common import (
    Action,
    Attitude,
    GameDescription,
    Gene,
    PlayerHistory,
    PlayerId,
)
from emergent_llm.players.base_player import BasePlayer, BaseStrategy


class LLMPlayer(BasePlayer):
    """Player that uses an LLM-generated strategy."""

    def __init__(self,
                 name: str,
                 gene: Gene,
                 game_description: GameDescription,
                 strategy_class: type[BaseStrategy],
                 max_errors: int = 2):
        super().__init__(name)
        self.gene = gene
        self.id = PlayerId(
            name, gene,
            f"{strategy_class.__module__}.{strategy_class.__name__}")
        self.game_description: GameDescription = game_description
        self.strategy_class: type[BaseStrategy] = strategy_class
        self._takes_stock = game_description.has_stock()

        self.logger = logging.getLogger(f"{repr(self)}")

        self.error_count = 0
        self.max_errors = max_errors

        self.reset()

    def reset(self):
        self.strategy_function = self.strategy_class(self.game_description)
        self.error_count = 0

    def __call__(self, history: PlayerHistory, current_stock=None) -> Action:
        try:
            if self._takes_stock:
                action = self.strategy_function(history, current_stock)
            else:
                action = self.strategy_function(history)

            if not isinstance(action, Action):
                raise TypeError(
                    f"Strategy returned {type(action).__name__} instead of Action"
                )
            return action

        except Exception as e:
            self.error_count += 1
            self.logger.warning(
                f"Strategy {self.id} error #{self.error_count} in round {history.round_number}: "
                f"{e.__class__.__name__}: {e}")

            if self.error_count > self.max_errors:
                self.logger.error(f"Strategy {self.id} exceeded error limit")
                raise

            base_attitude = self.id.attitude.to_base_attitude()
            return Action.C if base_attitude == Attitude.COLLECTIVE else Action.D

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def __del__(self):
        if hasattr(self, 'strategy_function'):
            del self.strategy_function


class SimplePlayer(BasePlayer):
    """Simple player for testing. Strategy function takes history only."""

    def __init__(self, name: str,
                 strategy_function: Callable[[PlayerHistory], Action]):
        super().__init__(name)
        self.strategy_function = strategy_function

    def reset(self):
        pass

    def __call__(self, history: PlayerHistory, current_stock=None) -> Action:
        return self.strategy_function(history)


@dataclass(frozen=True)
class StrategySpec:
    """Associates a strategy class with its generating gene."""
    gene: Gene
    strategy_class: type[BaseStrategy]

    def create_player(self, name: str,
                      game_description: GameDescription) -> LLMPlayer:
        return LLMPlayer(name=name,
                         gene=self.gene,
                         game_description=game_description,
                         strategy_class=self.strategy_class)

    def __str__(self) -> str:
        return f"{self.gene}:{self.strategy_class.__name__}"
