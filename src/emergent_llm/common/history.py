"""Game history classes for tournament and player use."""
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from emergent_llm.common.actions import Action


@dataclass
class PlayerHistory:
    """
    Anonymous, aggregated history from one player's perspective.

    Opponents are anonymous: only the *count* of cooperating opponents is
    visible per round, not which specific opponents cooperated.

    On round 0, all arrays have length 0 (not None).
    """
    my_actions: NDArray[np.bool_]           # [round] — this player's actions
    my_payoffs: NDArray[np.float64]         # [round] — this player's payoffs
    opponent_cooperators: NDArray[np.int_]  # [round] — count of cooperating opponents

    def __post_init__(self):
        """Make all arrays read-only."""
        self.my_actions.flags.writeable = False
        self.my_payoffs.flags.writeable = False
        self.opponent_cooperators.flags.writeable = False

    @property
    def round_number(self) -> int:
        """Current round index (0 on first call, equal to rounds completed so far)."""
        return len(self.my_actions)

    @classmethod
    def empty(cls) -> "PlayerHistory":
        """Construct an empty history for round 0."""
        return cls(
            my_actions=np.zeros(0, dtype=np.bool_),
            my_payoffs=np.zeros(0, dtype=np.float64),
            opponent_cooperators=np.zeros(0, dtype=np.int_),
        )


@dataclass
class GameHistory:
    """
    Complete game history for tournament/logging use.
    This retains the full per-player information.
    """
    actions: NDArray[np.bool_]    # [round, player]
    payoffs: NDArray[np.float64]  # [round, player]

    def __post_init__(self):
        if self.actions.dtype != np.bool_:
            raise TypeError(
                f"actions must be boolean array, got {self.actions.dtype}")
        if self.payoffs.dtype != np.float64:
            raise TypeError(
                f"payoffs must be float64 array, got {self.payoffs.dtype}")
        if self.actions.ndim == 1:
            self.actions = self.actions.reshape(1, -1)
        if self.payoffs.ndim == 1:
            self.payoffs = self.payoffs.reshape(1, -1)

    def for_player(self, player_index: int) -> PlayerHistory:
        """
        Create an anonymised, aggregated view for the given player.
        """
        my_actions = self.actions[:, player_index]
        my_payoffs = self.payoffs[:, player_index]

        opponent_mask = np.ones(self.actions.shape[1], dtype=bool)
        opponent_mask[player_index] = False
        opponent_actions = self.actions[:, opponent_mask]
        opponent_cooperators = opponent_actions.sum(axis=1).astype(np.int_)

        return PlayerHistory(
            my_actions=my_actions,
            my_payoffs=my_payoffs,
            opponent_cooperators=opponent_cooperators,
        )

    def update(self, actions: NDArray[np.bool_], payoffs: NDArray[np.float64]):
        if actions.ndim == 1:
            actions = actions.reshape(1, -1)
        if payoffs.ndim == 1:
            payoffs = payoffs.reshape(1, -1)

        self.actions = np.vstack([self.actions, actions])
        self.payoffs = np.vstack([self.payoffs, payoffs])

    def total_payoffs(self) -> list[float]:
        return self.payoffs.sum(axis=0).tolist()

    def total_cooperations(self) -> list[int]:
        return self.actions.sum(axis=0).tolist()

    def cooperations_by_round(self) -> list[int]:
        return self.actions.sum(axis=1).tolist()
