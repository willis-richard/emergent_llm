"""Attitudes for LLM players in social dilemma experiments."""
from enum import StrEnum


class Attitude(StrEnum):
    """Player attitudes for strategy generation."""
    COLLECTIVE = "collective"
    PROSOCIAL = "prosocial"
    COMMUNAL = "communal"
    EXPLOITATIVE = "exploitative"
    AGGRESSIVE = "aggressive"
    OPPORTUNISTIC = "opportunistic"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Attitude.{self.name}"

    @staticmethod
    def base_attitudes() -> list['Attitude']:
        return [Attitude.COLLECTIVE, Attitude.EXPLOITATIVE]

    def to_base_attitude(self) -> 'Attitude':
        if self in {Attitude.COLLECTIVE, Attitude.PROSOCIAL, Attitude.COMMUNAL}:
            return Attitude.COLLECTIVE
        return Attitude.EXPLOITATIVE

    def flip(self):
        assert self.value in self.base_attitudes(), f"{self.value} not a base attitude"
        return COLLECTIVE if self.value == EXPLOITATIVE else EXPLOITATIVE


# Export for convenience
COLLECTIVE = Attitude.COLLECTIVE
PROSOCIAL = Attitude.PROSOCIAL
COMMUNAL = Attitude.COMMUNAL
EXPLOITATIVE = Attitude.EXPLOITATIVE
AGGRESSIVE = Attitude.AGGRESSIVE
OPPORTUNISTIC = Attitude.OPPORTUNISTIC
