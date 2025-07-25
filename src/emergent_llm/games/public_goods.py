"""Public Goods Game implementation."""
from dataclasses import dataclass

from numpy.typing import NDArray
import numpy as np

from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.base_game import BaseGame
from emergent_llm.players.base_player import BasePlayer


@dataclass
class PublicGoodsDescription(GameDescription):
    """Description for Public Goods Game."""
    k: float  # Cooperation multiplier

    def __post_init__(self):
        super().__post_init__()
        if not (1 < self.k < self.n_players):
            raise ValueError(f"k must be between 1 and {self.n_players}, got {self.k}")


class PublicGoodsGame(BaseGame):
    """
    Public Goods Game implementation.

    Rules:
    - Defect gives player payoff of 1
    - Cooperate gives all players payoff of k/n
    - If player defects while others cooperate, they get 1 + (cooperators * k/n)
    """

    def __init__(self, players: list[BasePlayer], description: PublicGoodsDescription):
        """Initialize Public Goods Game with typed description."""
        super().__init__(players, description)

    def _calculate_payoffs(self, actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round."""
        n_cooperators = np.sum(actions)
        cooperation_benefit = n_cooperators * self.description.k / self.n_players

        return cooperation_benefit + (~actions).astype(np.float64)
