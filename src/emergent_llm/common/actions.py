"""Minimal action enum for social dilemma games."""
from enum import Enum

import numpy as np
from numpy.typing import NDArray


class Action(Enum):
    """Core actions in social dilemma games.
    There are only two possible actions, namely Cooperate or Defect,
    which are called C and D for convenience.
    """
    D = 0  # Defect - represented as False/0 in boolean arrays
    C = 1  # Cooperate - represented as True/1 in boolean arrays

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __bool__(self) -> bool:
        """Convert to boolean. C=True, D=False."""
        return bool(self.value)

    def flip(self) -> "Action":
        return Action(1 - self.value)

    def __add__(self, other):
        """Add Action value to number."""
        if isinstance(other, (int, float)):
            return self.value + other
        return NotImplemented

    def __radd__(self, other):
        """Support sum() by allowing 0 + Action."""
        if isinstance(other, (int, float)):
            return other + self.value
        return NotImplemented

    @classmethod
    def print_definition(cls) -> str:
        """For printing in prompts"""
        definition = f"class {cls.__name__}(Enum):\n"

        definition += "\n".join(
            f"    {member.name} = \"{member.value}\"" if isinstance(
                member.value, str) else f"    {member.name} = {member.value}"
            for member in cls)

        return definition

    @classmethod
    def to_bool_array(cls, actions: list['Action']) -> NDArray[np.bool_]:
        """Convert list of Actions to numpy boolean array."""
        result = np.array([action == cls.C for action in actions],
                          dtype=np.bool_)
        assert result.dtype == np.bool_, f"Expected bool array, got {result.dtype}"
        return result

    @classmethod
    def from_bool_array(cls, bool_array: NDArray[np.bool_]):
        """Convert numpy boolean array to list/nested lists of Actions."""
        assert bool_array.dtype == np.bool_, f"Expected bool array, got {bool_array.dtype}"

        # Convert all elements using flat iteration
        flat_actions = [cls.C if val else cls.D for val in bool_array.flat]

        # Return in original shape
        if bool_array.ndim == 1:
            return flat_actions
        else:
            # Reshape to nested lists matching input dimensions
            arr = np.array(flat_actions, dtype=object).reshape(bool_array.shape)
            return arr.tolist()


# Export for convenience
C, D = Action.C, Action.D

__all__ = ['Action', 'C', 'D']
