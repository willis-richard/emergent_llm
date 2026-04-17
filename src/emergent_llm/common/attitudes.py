"""Attitudes for LLM players in social dilemma experiments."""
from enum import StrEnum


class Attitude(StrEnum):
    """Player attitudes for strategy generation."""
    COLLECTIVE = "collective"
    PROSOCIAL = "prosocial"
    ALTRUISTIC = "altruistic"
    COOPERATIVE = "cooperative"

    EXPLOITATIVE = "exploitative"
    AGGRESSIVE = "aggressive"
    PREDATORY = "predatory"
    PARASITIC = "parasitic"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Attitude.{self.name}"

    @staticmethod
    def base_attitudes() -> list['Attitude']:
        return [Attitude.COLLECTIVE, Attitude.EXPLOITATIVE]

    def to_base_attitude(self) -> 'Attitude':
        if self in {Attitude.COLLECTIVE, Attitude.PROSOCIAL, Attitude.ALTRUISTIC, Attitude.COOPERATIVE}:
            return Attitude.COLLECTIVE
        return Attitude.EXPLOITATIVE

    def flip(self):
        assert self in self.base_attitudes(), f"{self.value} not a base attitude"
        return COLLECTIVE if self.value == EXPLOITATIVE else EXPLOITATIVE


# Export for convenience
COLLECTIVE = Attitude.COLLECTIVE
EXPLOITATIVE = Attitude.EXPLOITATIVE
