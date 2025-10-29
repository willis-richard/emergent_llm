from dataclasses import dataclass

from emergent_llm.common.attitudes import Attitude
from emergent_llm.common.gene import Gene


@dataclass(frozen=True)
class PlayerId:
    name: str
    gene: Gene | None  # None only for SimplePlayer
    strategy: str | None  # None only for SimplePlayer

    @property
    def attitude(self) -> Attitude | None:
        """Derive attitude from gene."""
        return self.gene.attitude if self.gene else None

    def __str__(self) -> str:
        """Human-readable representation"""
        if self.gene is None:
            return self.name
        return f"{self.name}[{self.gene}, {self.strategy}]"

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerId':
        """Load PlayerId from dictionary data."""
        gene = None
        if data['gene'] is not None:
            gene = Gene(model=data['gene']['model'],
                        attitude=Attitude(data['gene']['attitude']))

        return cls(name=data['name'], gene=gene, strategy=data['strategy'])
