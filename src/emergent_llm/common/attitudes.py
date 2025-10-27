"""Attitudes for LLM players in social dilemma experiments."""
from enum import StrEnum


class Attitude(StrEnum):
    """Player attitudes for strategy generation."""
    COLLECTIVE = "collective"
    EXPLOITATIVE = "exploitative"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Attitude.{self.name}"

    def flip(self):
        return COLLECTIVE if self.value == EXPLOITATIVE else EXPLOITATIVE


# Export for convenience
COLLECTIVE = Attitude.COLLECTIVE
EXPLOITATIVE = Attitude.EXPLOITATIVE
