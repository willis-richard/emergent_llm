"""Attitudes for LLM players in social dilemma experiments."""
from enum import Enum


class Attitude(Enum):
    """Player attitudes for strategy generation."""
    COOPERATIVE = "cooperative"
    AGGRESSIVE = "aggressive"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Attitude.{self.name}"


# Export for convenience
COOPERATIVE = Attitude.COOPERATIVE
AGGRESSIVE = Attitude.AGGRESSIVE

__all__ = ['Attitude', 'COOPERATIVE', 'AGGRESSIVE']
