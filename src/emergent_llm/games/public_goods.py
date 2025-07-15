"""Public Goods Game implementation."""
from emergent_llm.games.base_game import BaseGame
from emergent_llm.common.actions import Action, C, D
from emergent_llm.players import BasePlayer


class PublicGoodsGame(BaseGame):
    """
    Public Goods Game implementation.

    Rules:
    - Defect gives player payoff of 1
    - Cooperate gives all players payoff of k/n
    - If player defects while others cooperate, they get 1 + (cooperators * k/n)
    """

    def __init__(self, players: list[BasePlayer], k: float = 2.0, **kwargs):
        """
        Initialize Public Goods Game.

        Args:
            players: List of players
            k: Cooperation multiplier (should be 1 < k < n)
        """
        super().__init__(players, **kwargs)
        self.k = k

        # Validate k parameter
        if not (1 < k < self.n_players):
            raise ValueError(f"k must be between 1 and {self.n_players}, got {k}")

    def calculate_payoffs(self, actions: list[Action]) -> list[float]:
        """Calculate payoffs for a single round."""
        cooperators = sum(1 for action in actions if action == C)
        cooperation_benefit = cooperators * self.k / self.n_players

        return [
            1.0 + cooperation_benefit if action == D else cooperation_benefit
            for action in actions
        ]

    def game_description(self) -> dict[str, any]:
        """Return game parameters for strategy generation."""
        return {
            'game_type': 'public_goods',
            'n_players': self.n_players,
            'k': self.k,
            'defect_payoff': 1.0,
            'cooperate_benefit_per_player': self.k / self.n_players,
            'rules': {
                'defect': f"Gives you a payoff of 1.0",
                'cooperate': f"Gives all players a payoff of {self.k}/{self.n_players} = {self.k/self.n_players}",
                'example': f"If you defect and {self.n_players-1} others cooperate, you get 1.0 + {self.n_players-1} * {self.k/self.n_players} = {1.0 + (self.n_players-1) * self.k/self.n_players}"
            }
        }
