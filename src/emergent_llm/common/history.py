"""Game history classes for tournament and player use."""
from dataclasses import dataclass
import numpy as np
from typing import List
from emergent_llm.common.actions import Action

@dataclass
class GameHistory:
    """
    Complete game history for tournament/logging use.
    Just stores the raw data without player-specific processing.
    """
    actions: np.ndarray     # All players' actions [round, player] -> Action
    payoffs: np.ndarray     # All players' payoffs [round, player] -> float

    def for_player(self, player_index: int) -> 'PlayerHistory':
        """Create player-specific view from this game history."""

        if len(self.actions) == 0:  # First round - no history yet
            return PlayerHistory(
                my_actions=np.array([], dtype=object),
                my_payoffs=np.array([]),
                opponent_actions=np.array([[]]),
                opponent_payoffs=np.array([[]])
            )

        # Extract player-specific data
        my_actions = self.actions[:, player_index]
        my_payoffs = self.payoffs[:, player_index]

        # Extract opponent data (exclude this player's column)
        opponent_mask = np.ones(self.actions.shape[1], dtype=bool)
        opponent_mask[player_index] = False
        opponent_actions = self.actions[:, opponent_mask]
        opponent_payoffs = self.payoffs[:, opponent_mask]

        return PlayerHistory(
            my_actions=my_actions,
            my_payoffs=my_payoffs,
            opponent_actions=opponent_actions,
            opponent_payoffs=opponent_payoffs
        )


@dataclass
class PlayerHistory:
    """
    Player-specific view of game history with convenience access.
    """
    my_actions: np.ndarray      # This player's actions
    my_payoffs: np.ndarray      # This player's payoffs
    opponent_actions: np.ndarray  # Opponents' actions [round, opponent]
    opponent_payoffs: np.ndarray  # Opponents' payoffs [round, opponent]

    @property
    def round_number(self) -> int:
        """Current round number (number of completed rounds)."""
        return len(self.my_actions)

    @property
    def is_first_round(self) -> bool:
        """True if this is the first round (no history yet)."""
        return self.round_number == 0
