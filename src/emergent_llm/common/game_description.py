from dataclasses import dataclass, asdict, fields
from abc import ABC


@dataclass
class GameDescription(ABC):
    """Base class for all game descriptions."""
    n_players: int
    n_rounds: int

    def to_dict(self) -> dict:
        """Convert GameDescription to dictionary for serialization."""
        return asdict(self)

    def __post_init__(self):
        """Validate common parameters."""
        if self.n_players <= 0:
            raise ValueError("n_players must be positive")
        if self.n_rounds <= 0:
            raise ValueError("n_rounds must be positive")

    def __repr__(self):
        return str(self.to_dict())

    @classmethod
    def print_definition(cls):
        print("@dataclass")
        print(f"class {cls.__name__}:")

        for field in fields(cls):
            type_name = field.type.__name__ if hasattr(field.type, '__name__') else str(field.type)
            print(f"    {field.name}: {type_name}")
