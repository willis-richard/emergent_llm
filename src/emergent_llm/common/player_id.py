from dataclasses import dataclass
from emergent_llm.common.attitudes import Attitude

@dataclass(frozen=True)
class PlayerId:
    name: str
    attitude: Attitude | None
    strategy: str | None

    def __str__(self) -> str:
        """Human-readable representation"""
        if self.attitude is None:
            return self.name
        return f"{self.name}[{self.attitude.value}, {self.strategy}]"
