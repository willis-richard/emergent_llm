"""Public Goods Game implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from emergent_llm.common import GameDescription
from emergent_llm.games.base_game import BaseGame
from emergent_llm.players import BasePlayer


@dataclass(frozen=True)
class PublicGoodsDescription(GameDescription):
    """Description for Public Goods Game."""
    k: float  # Cooperation multiplier

    def __post_init__(self):
        super().__post_init__()
        if not (1 < self.k < self.n_players):
            raise ValueError(
                f"k must be between 1 and {self.n_players}, got {self.k}")

    @classmethod
    def game_type(cls) -> type[PublicGoodsGame]:
        return PublicGoodsGame

    def max_social_welfare(self) -> float:
        return self.k * self.n_rounds

    def min_social_welfare(self) -> float:
        return self.n_rounds

    def max_payoff(self) -> float:
        return (1 + self.k) * self.n_rounds - self.min_payoff()

    def min_payoff(self) -> float:
        return self.n_rounds * self.k / self.n_players


class PublicGoodsGame(BaseGame):
    """
    Public Goods Game implementation.

    Rules:
    - Defect gives player payoff of 1
    - Cooperate gives all players payoff of k/n
    - If player defects while others cooperate, they get 1 + (cooperators * k/n)
    """

    def __init__(self, players: Sequence[BasePlayer],
                 description: PublicGoodsDescription):
        """Initialize Public Goods Game with typed description."""
        super().__init__(players, description)

    def _calculate_payoffs(self,
                           actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round."""
        n_cooperators = np.sum(actions)
        cooperation_benefit = n_cooperators * self.description.k / self.description.n_players

        return cooperation_benefit + (~actions).astype(np.float64)
