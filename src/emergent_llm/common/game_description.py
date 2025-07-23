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
    def print_definition(cls) -> str:
        """Print the definition, for use in the prompts"""
        definition = "@dataclass\n"
        definition += f"class {cls.__name__}:\n"

        for field in fields(cls):
            type_name = field.type.__name__ if hasattr(field.type, '__name__') else str(field.type)
            definition += f"    {field.name}: {type_name}\n"

        return definition

    def print_constructor(self) -> str:
        """Return a string showing how to construct this game description."""
        class_name = self.__class__.__name__
        params = []
        for field_name, field_value in self.to_dict().items():
            if isinstance(field_value, str):
                params.append(f"{field_name}='{field_value}'")
            else:
                params.append(f"{field_name}={field_value}")
        return f"{class_name}({', '.join(params)})"
