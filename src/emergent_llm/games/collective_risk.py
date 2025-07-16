# src/emergent_llm/games/collective_risk.py
"""Collective Risk Dilemma implementation."""
from emergent_llm.games.base_game import BaseGame
from emergent_llm.games.game_description import CollectiveRiskDescription
from emergent_llm.common.actions import Action, C, D
from emergent_llm.players import BasePlayer


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
