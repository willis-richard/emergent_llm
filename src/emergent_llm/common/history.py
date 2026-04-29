"""Game history classes for tournament and player use."""
from dataclasses import dataclass, field

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


@dataclass
class GameHistory:
    """
    Game history sized for n_rounds × n_players. Rounds are recorded one at a
    time via `record`. Until a round is recorded, its row is zero-filled and
    excluded from views and aggregates.
    """
    n_rounds: int
    n_players: int
    actions: NDArray[np.bool_] = field(init=False)
    payoffs: NDArray[np.float64] = field(init=False)
    round_number: int = field(init=False, default=0)

    def __post_init__(self):
        if self.n_rounds <= 0:
            raise ValueError(f"n_rounds must be positive, got {self.n_rounds}")
        if self.n_players <= 0:
            raise ValueError(f"n_players must be positive, got {self.n_players}")
        self.actions = np.zeros((self.n_rounds, self.n_players), dtype=np.bool_)
        self.payoffs = np.zeros((self.n_rounds, self.n_players), dtype=np.float64)

    def record(self,
               actions_row: NDArray[np.bool_],
               payoffs_row: NDArray[np.float64]) -> None:
        """Write the next round's results."""
        r = self.round_number
        assert r < self.n_rounds, f"Game already complete"
        self.actions[r] = actions_row
        self.payoffs[r] = payoffs_row
        self.round_number += 1

    def for_player(self, player_index: int) -> PlayerHistory:
        """Anonymised view for the given player, covering rounds recorded so far."""
        r = self.round_number
        my_actions = self.actions[:r, player_index]
        my_payoffs = self.payoffs[:r, player_index]

        opponent_mask = np.ones(self.n_players, dtype=bool)
        opponent_mask[player_index] = False
        opponent_cooperators = self.actions[:r][:, opponent_mask].sum(axis=1).astype(np.int_)

        return PlayerHistory(
            my_actions=my_actions,
            my_payoffs=my_payoffs,
            opponent_cooperators=opponent_cooperators,
        )

    def total_payoffs(self) -> list[float]:
        return self.payoffs[:self.round_number].sum(axis=0).tolist()

    def total_cooperations(self) -> list[int]:
        return self.actions[:self.round_number].sum(axis=0).tolist()

    def cooperations_by_round(self) -> list[int]:
        return self.actions[:self.round_number].sum(axis=1).tolist()
