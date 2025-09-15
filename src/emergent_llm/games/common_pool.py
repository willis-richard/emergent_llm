"""Common Poll Resource implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from emergent_llm.common import GameDescription, GameState
from emergent_llm.games.base_game import BaseGame
from emergent_llm.players import BasePlayer
from numpy.typing import NDArray


@dataclass
class CommonPoolState(GameState):
    current_stock: float


@dataclass
class CommonPoolDescription(GameDescription):
    """Description for Public Goods Game."""
    capacity: int  # capacity of the resource

    def __post_init__(self):
        super().__post_init__()
        if not (self.capacity >= 2 * self.n_players):
            raise ValueError(f"capacity must be greater than {2*self.n_players}, got {self.capacity}")

    @classmethod
    def game_state_type(cls) -> type[CommonPoolState]:
        return CommonPoolState

    @classmethod
    def game_type(cls) -> type[CommonPoolGame]:
        return CommonPoolGame

    def max_social_welfare(self) -> float:
        """All-C every round, except All-D in the last"""
        return 0.5 * (self.capacity / self.n_players) * (self.n_rounds + 1)

    def min_social_welfare(self) -> float:
        """All-D in the first round"""
        return self.capacity / self.n_players

    def max_payoff(self) -> float:
        """This one is difficult to compute: estimate as All-C for all opponents, All-D for player, perfect stock somehow"""
        return (self.capacity / self.n_players) * self.n_rounds

    def min_payoff(self) -> float:
        """All-D in the first round"""
        return self.capacity / self.n_players

class CommonPoolGame(BaseGame):
    """
    Common pool resource with growth rate of 2 * x * (1 - x / capacity)

    Rules:
    - Defect consumes stock/n
    - Cooperate consumes stock/2n
    - Remaining stock grows by growth rate
    """

    def __init__(self, players: Sequence[BasePlayer], description: CommonPoolDescription):
        super().__init__(players, description)
        self.stock = self.description.capacity

    def _calculate_payoffs(self, actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round."""
        share = 0.5 * self.stock / self.description.n_players

        payoffs = share + share * (~actions).astype(np.float64)

        self.stock -= np.sum(payoffs)
        self.stock += 2 * self.stock * (1 - self.stock / self.description.capacity)
        self.stock = min(self.stock, self.description.capacity)

        return payoffs

    def get_state(self):
        return CommonPoolState(self.current_round, current_stock=self.stock)

    def reset(self):
        """Reset game to initial state."""
        super().reset()
        self.stock = self.description.capacity
