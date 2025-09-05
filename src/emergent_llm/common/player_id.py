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

    def serialise(self) -> dict:
        return {
            'name': self.name,
            'attitude': self.attitude.value if self.attitude else None,
            'strategy': self.strategy
        }

    @classmethod
    def deserialise(cls, data: dict) -> 'PlayerId':
        return cls(
            name=data['name'],
            attitude=Attitude(data['attitude']) if data['attitude'] else None,
            strategy=data['strategy']
        )
