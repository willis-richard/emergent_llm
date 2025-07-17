"""Collective Risk Dilemma implementation."""
from dataclasses import dataclass

from emergent_llm.common.actions import Action, C, D
from emergent_llm.common.game_description import GameDescription
from emergent_llm.games.base_game import BaseGame
from emergent_llm.players.base_player import BasePlayer


@dataclass
class CollectiveRiskDescription(GameDescription):
    """Description for Collective Risk Dilemma."""
    m: int    # Minimum cooperators needed to avoid disaster
    k: float  # Reward if threshold is met

    def __post_init__(self):
        super().__post_init__()
        if not (1 < self.m <= self.n_players):
            raise ValueError(f"m must be between 1 and {self.n_players}, got {self.m}")
        if self.k <= 0:
            raise ValueError(f"k must be positive, got {self.k}")


class CollectiveRiskGame(BaseGame):
    """
    Collective Risk Dilemma implementation.

    Rules:
    - Defect gives player payoff of 1
    - If at least m players cooperate, everyone gets reward k
    - If fewer than m players cooperate, everyone gets 0
    """

    def __init__(self, players: list[BasePlayer], description: CollectiveRiskDescription):
        """Initialize Collective Risk Game with typed description."""
        super().__init__(players, description)

    def calculate_payoffs(self, actions: list[Action]) -> list[float]:
        """Calculate payoffs for a single round."""
        cooperators = sum(1 for action in actions if action == C)
        threshold_met = cooperators >= self.description.m

        collective_reward = self.description.k if threshold_met else 0.0

        return [
            1.0 + collective_reward if action == D else collective_reward
            for action in actions
        ]
