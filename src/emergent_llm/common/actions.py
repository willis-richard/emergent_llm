"""Minimal action enum for social dilemma games."""
from enum import Enum
from functools import total_ordering

class Action(Enum):
    """Core actions in social dilemma games.
    There are only two possible actions, namely Cooperate or Defect,
    which are called C and D for convenience.
    """
    C = 0  # Cooperate
    D = 1  # Defect

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def flip(self):
        """Returns the opposite Action."""
        if self == Action.C:
            return Action.D
        return Action.C

    @classmethod
    def print_definition(cls):
        print(f"class {cls.__name__}(Enum):")

        for member in cls:
            if isinstance(member.value, str):
                print(f"    {member.name} = \"{member.value}\"")
            else:
                print(f"    {member.name} = {member.value}")

# Export for convenience
C, D = Action.C, Action.D

__all__ = ['Action', 'C', 'D']
