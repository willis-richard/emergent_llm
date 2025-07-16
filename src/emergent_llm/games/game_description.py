from dataclasses import dataclass
from abc import ABC


@dataclass
class GameDescription(ABC):
    """Base class for all game descriptions."""
    n_players: int
    n_rounds: int

    def __post_init__(self):
        """Validate common parameters."""
        if self.n_players <= 0:
            raise ValueError("n_players must be positive")
        if self.n_rounds <= 0:
            raise ValueError("n_rounds must be positive")


@dataclass
class PublicGoodsDescription(GameDescription):
    """Description for Public Goods Game."""
    k: float  # Cooperation multiplier

    def __post_init__(self):
        super().__post_init__()
        if not (1 < self.k < self.n_players):
            raise ValueError(f"k must be between 1 and {self.n_players}, got {self.k}")


@dataclass
class CollectiveRiskDescription(GameDescription):
    """Description for Collective Risk Dilemma."""
    m: int    # Minimum cooperators needed to avoid disaster
    k: float  # Reward if threshold is met

    def __post_init__(self):
        super().__post_init__()
        if not (1 <= self.m <= self.n_players):
            raise ValueError(f"m must be between 1 and {self.n_players}, got {self.m}")
        if self.k <= 0:
            raise ValueError(f"k must be positive, got {self.k}")
