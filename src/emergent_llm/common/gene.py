"""Gene representation for cultural evolution tournaments."""
import random
from dataclasses import dataclass

from emergent_llm.common.attitudes import Attitude


@dataclass(frozen=True)
class Gene:
    """
    Immutable gene that can be hashed for frequency tracking.
    """
    model: str
    attitude: Attitude

    def __str__(self) -> str:
        return f"{self.model}[{self.attitude.value}]"

    @classmethod
    def from_dict(cls, data: dict) -> 'Gene':
        """Load Gene from dictionary data."""
        return cls(
            model=data['model'],
            attitude=Attitude(data['attitude'])
        )
