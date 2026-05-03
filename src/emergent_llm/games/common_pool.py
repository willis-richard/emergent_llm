"""Common Pool Resource implementation."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from emergent_llm.common import GameDescription
from emergent_llm.games.base_game import BaseGame
from emergent_llm.players import BasePlayer


@lru_cache(maxsize=None)
def _compute_payoff_bounds(n_players: int, n_rounds: int,
                           capacity: int) -> tuple[float, float]:
    """Compute (min_payoff, max_payoff) for one focal player over r rounds.

    Stock dynamics replicate CommonPoolGame._calculate_payoffs exactly.

    min: focal All-C, others All-D.
    max: focal cooperates for some prefix then defects for the rest, others
         All-C. Switch round chosen to maximize the focal's total. (Optimum
         within this strategy class; not provably the global optimum.)

    Cached on the primitive (n, r, K) tuple, so all CommonPoolDescription
    instances sharing those values reuse the result.
    """
    n, r, K = n_players, n_rounds, float(capacity)

    # --- min payoff: focal C, others D ---------------------------------------
    # Per round: focal extracts share = S/(2n); each of the n-1 others
    # extracts 2*share = S/n. Remaining stock before growth = S/(2n).
    S = K
    min_payoff = 0.0
    for _ in range(r):
        share = 0.5 * S / n
        focal = share                          # cooperate
        total_extracted = share + (n - 1) * 2 * share
        min_payoff += focal
        S = max(S - total_extracted, 0.0)
        S = S + 2 * S * (1 - S / K)
        S = min(S, K)

    # --- max payoff: focal switches C->D, others always C --------------------
    # While focal cooperates and everyone else cooperates, S = K is a fixed
    # point of the dynamics, so during the cooperation prefix S stays at K and
    # focal earns K/(2n) each round. The defection trajectory therefore always
    # starts from S = K, regardless of how long the prefix is.
    coop_payoff = K / (2 * n)

    S = K
    def_payoffs: list[float] = []
    for _ in range(r):
        share = 0.5 * S / n
        focal = 2 * share                      # defect
        total_extracted = focal + (n - 1) * share
        def_payoffs.append(focal)
        S = max(S - total_extracted, 0.0)
        S = S + 2 * S * (1 - S / K)
        S = min(S, K)

    # Sweep switch points: k = number of trailing defection rounds, 0..r.
    max_payoff = r * coop_payoff               # k = 0 (always cooperate)
    cum_def = 0.0
    for k in range(1, r + 1):
        cum_def += def_payoffs[k - 1]
        total = (r - k) * coop_payoff + cum_def
        if total > max_payoff:
            max_payoff = total

    return min_payoff, max_payoff


@dataclass(frozen=True)
class CommonPoolDescription(GameDescription):
    """Description for Common Pool Game."""
    capacity: int

    def __post_init__(self):
        super().__post_init__()
        if not (self.capacity >= 2 * self.n_players):
            raise ValueError(
                f"capacity must be greater than {2*self.n_players}, got {self.capacity}"
            )

    @classmethod
    def has_stock(cls) -> bool:
        return True

    @classmethod
    def game_type(cls) -> type[CommonPoolGame]:
        return CommonPoolGame

    def max_player_welfare(self) -> float:
        """All-C every round, except All-D in the last"""
        return 0.5 * (self.capacity / self.n_players) * (self.n_rounds + 1)

    def min_player_welfare(self) -> float:
        """All-D in the first round"""
        return self.capacity / self.n_players

    def max_payoff(self) -> float:
        """Optimal C-then-D against (n-1) All-C opponents (cached)."""
        return _compute_payoff_bounds(
            self.n_players, self.n_rounds, self.capacity)[1]

    def min_payoff(self) -> float:
        """Focal All-C against (n-1) All-D opponents (cached)."""
        return _compute_payoff_bounds(
            self.n_players, self.n_rounds, self.capacity)[0]


class CommonPoolGame(BaseGame):
    """
    Common pool resource with growth rate of 2 * x * (1 - x / capacity).
    - Defect consumes stock/n
    - Cooperate consumes stock/2n
    - Remaining stock grows by growth rate
    """

    def __init__(self, players: Sequence[BasePlayer],
                 description: CommonPoolDescription):
        super().__init__(players, description)
        self.stock = self.description.capacity

    def _calculate_payoffs(self,
                           actions: NDArray[np.bool_]) -> NDArray[np.float64]:
        share = 0.5 * self.stock / self.description.n_players
        payoffs = share + share * (~actions).astype(np.float64)

        self.stock -= np.sum(payoffs)
        self.stock = max(self.stock, 0)
        self.stock += 2 * self.stock * (1 - self.stock / self.description.capacity)
        self.stock = min(self.stock, self.description.capacity)

        return payoffs

    def get_current_stock(self) -> float:
        return self.stock

    def reset(self):
        super().reset()
        self.stock = self.description.capacity
