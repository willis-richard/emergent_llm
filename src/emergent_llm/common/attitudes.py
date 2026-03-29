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

    @staticmethod
    def Base_attitudes() -> list['Attitude']:
        """Compatibility alias for callers using the suggested name."""
        return Attitude.base_attitudes()

    def to_base_attitude(self) -> 'Attitude':
        if self in {Attitude.COLLECTIVE, Attitude.PROSOCIAL, Attitude.COMMUNAL}:
            return Attitude.COLLECTIVE
        return Attitude.EXPLOITATIVE

    def To_base_attitude(self) -> 'Attitude':
        """Compatibility alias for callers using the suggested name."""
        return self.to_base_attitude()

    def flip(self):
        return (Attitude.EXPLOITATIVE
                if self.to_base_attitude() == Attitude.COLLECTIVE else
                Attitude.COLLECTIVE)


# Export for convenience
COLLECTIVE = Attitude.COLLECTIVE
PROSOCIAL = Attitude.PROSOCIAL
COMMUNAL = Attitude.COMMUNAL
EXPLOITATIVE = Attitude.EXPLOITATIVE
AGGRESSIVE = Attitude.AGGRESSIVE
OPPORTUNISTIC = Attitude.OPPORTUNISTIC
