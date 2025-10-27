"""Gene representation for cultural evolution tournaments."""
import random
from dataclasses import dataclass

from emergent_llm.common.attitudes import Attitude


@dataclass(frozen=True)
class Gene:
    """
    Immutable gene that can be hashed for frequency tracking.
    """
    provider_model: str  # e.g., "anthropic_claude-sonnet-4"
    attitude: Attitude

    def __str__(self) -> str:
        return f"{self.provider_model}[{self.attitude.value}]"
