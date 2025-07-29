"""Common Poll Resource implementation."""
from dataclasses import dataclass

from numpy.typing import NDArray
import numpy as np

from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.base_game import BaseGame
from emergent_llm.players.base_player import BasePlayer


@dataclass
class CommonPoolDescription(GameDescription):
    """Description for Public Goods Game."""
    capacity: int  # capacity of the resource

    def __post_init__(self):
        super().__post_init__()
        if not (1 < self.capacity < self.n_players):
            raise ValueError(f"capacity must be greater than {2*self.n_players}, got {self.capacity}")


class PublicGoodsGame(BaseGame):
    """
    Common pool resource with growth rate of 2 * x * (1 - x/capacity)

    Rules:
    - Defect consumes stock/n
    - Cooperate consumes stock/2n
    - Remaining stock grows by growth rate
    """

    def __init__(self, players: list[BasePlayer], description: CommonPoolDescription):
        super().__init__(players, description)
        self.stock = self.description.capacity

    def _calculate_payoffs(self, actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        """Calculate payoffs for a single round."""
        share = self.stock / self.description.n_players

        payoffs = share + share * (~actions).astype(np.float64)

        self.stock -= np.sum(payoffs)
        self.stock += 2 * self.stock * (1 - self.stock/self.description.capacity)

        return payoffs

    def reset(self):
        """Reset game to initial state."""
        super().reset()
        self.stock = self.description.capacity
