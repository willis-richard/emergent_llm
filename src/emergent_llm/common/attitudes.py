"""Attitudes for LLM players in social dilemma experiments."""
from enum import StrEnum


class Attitude(StrEnum):
    """Player attitudes for strategy generation."""
    COLLECTIVE = "collective"
    PROSOCIAL = "prosocial"
    ALTRUISTIC = "altruistic"
    BENEVOLENT = "benevolent"

    SELFISH = "selfish"
    SELFINTERESTED = "self-interested"
    OPPORTUNISTIC = "opportunistic"
    INDIVIDUALISTIC = "individualistic"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Attitude.{self.name}"

    @staticmethod
    def base_attitudes() -> list['Attitude']:
        return [Attitude.COLLECTIVE, Attitude.SELFISH]

    def to_base_attitude(self) -> 'Attitude':
        if self in {Attitude.COLLECTIVE, Attitude.PROSOCIAL, Attitude.ALTRUISTIC, Attitude.BENEVOLENT}:
            return Attitude.COLLECTIVE
        return Attitude.SELFISH

    def flip(self):
        assert self in self.base_attitudes(), f"{self.value} not a base attitude"
        return COLLECTIVE if self.value == SELFISH else SELFISH


# Export for convenience
COLLECTIVE = Attitude.COLLECTIVE
SELFISH = Attitude.SELFISH
