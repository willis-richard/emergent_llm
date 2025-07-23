"""Minimal action enum for social dilemma games."""
from enum import Enum


class Action(Enum):
    """Core actions in social dilemma games.
    There are only two possible actions, namely Cooperate or Defect,
    which are called C and D for convenience.
    """
    C = 0  # Cooperate
    D = 1  # Defect

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __bool__(self) -> bool:
        """Convert to boolean. C=False, D=True."""
        return bool(self.value)

    def flip(self) -> "Action":
        return Action(1 - self.value)

    @classmethod
    def print_definition(cls) -> str:
        """For printing in prompts"""
        definition = f"class {cls.__name__}(Enum):\n"

        definition += "\n".join(
            f"    {member.name} = \"{member.value}\""
            if isinstance(member.value, str)
            else f"    {member.name} = {member.value}"
            for member in cls)

        return definition


# Export for convenience
C, D = Action.C, Action.D

__all__ = ['Action', 'C', 'D']
