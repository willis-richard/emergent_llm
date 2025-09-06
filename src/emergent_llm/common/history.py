"""Game history classes for tournament and player use."""
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from emergent_llm.common.actions import Action


@dataclass
class PlayerHistory:
    my_actions: NDArray[np.bool_]    # This player's actions, indexed [round]
    my_payoffs: NDArray[np.float64]  # This player's payoffs, indexed [round]
    opponent_actions: NDArray[np.bool_]    # Opponents' actions, indexed [round, opponent]
    opponent_payoffs: NDArray[np.float64]  # Opponents' payoffs, indexed [round, opponent]

    @property
    def round_number(self) -> int:
        """Current round number (number of completed rounds)."""
        return len(self.my_actions)


@dataclass
class GameHistory:
    """
    Complete game history for tournament/logging use.
    Just stores the raw data without player-specific processing.
    """
    actions: NDArray[np.bool_]    # All players' actions,  indexed [round, player]
    payoffs: NDArray[np.float64]  # All players' payoffs,  indexed [round, player]

    def __post_init__(self):
        """Ensure arrays are always 2D."""
        if self.actions.dtype != np.bool_:
            raise TypeError(f"actions must be boolean array, got {self.actions.dtype}")
        if self.payoffs.dtype != np.float64:
            raise TypeError(f"payoffs must be float64 array, got {self.payoffs.dtype}")
        if self.actions.ndim == 1:
            self.actions = self.actions.reshape(1, -1)
        if self.payoffs.ndim == 1:
            self.payoffs = self.payoffs.reshape(1, -1)

    def for_player(self, player_index: int) -> None | PlayerHistory:
        """Create player-specific view from this game history."""

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

    def update(self, actions: NDArray[np.bool_], payoffs: NDArray[np.float64]):
        # Ensure input arrays are 2D
        if actions.ndim == 1:
            actions = actions.reshape(1, -1)
        if payoffs.ndim == 1:
            payoffs = payoffs.reshape(1, -1)

        self.actions = np.vstack([self.actions, actions])
        self.payoffs = np.vstack([self.payoffs, payoffs])

    def actions_as_string_array(self):
        fn = lambda a: str(Action(a))
        vec_fn = np.vectorize(fn)
        return vec_fn(self.actions)

    def total_payoffs(self) -> list[float]:
        return self.payoffs.sum(axis=0).tolist()

    def total_cooperations(self) -> list[bool]:
        return self.actions.sum(axis=0).tolist()

    def cooperations_by_round(self) -> list[bool]:
        return self.actions.sum(axis=1).tolist()
