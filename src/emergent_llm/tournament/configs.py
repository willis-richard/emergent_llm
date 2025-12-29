from dataclasses import asdict, dataclass
from typing import Callable

from emergent_llm.common import GameDescription, Gene
from emergent_llm.games import (
    STANDARD_GENERATORS,
    BaseGame,
    CollectiveRiskDescription,
    CollectiveRiskGame,
    CommonPoolDescription,
    CommonPoolGame,
    PublicGoodsDescription,
    PublicGoodsGame,
)


@dataclass(frozen=True)
class MixtureKey:
    n_collective: int
    n_exploitative: int


@dataclass
class BaseTournamentConfig:
    game_description: GameDescription
    repetitions: int = 1
    processes: int = 1

    def serialise(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        return {
            'game_description_type': self.game_description.__class__.__name__,
            'game_description': asdict(self.game_description),
            'repetitions': self.repetitions
        }

    @classmethod
    def from_dict(cls, config_data: dict) -> 'BaseTournamentConfig':
        """Load BaseTournamentConfig from dictionary data."""
        game_class_map = {
            'PublicGoodsDescription': PublicGoodsDescription,
            'CollectiveRiskDescription': CollectiveRiskDescription,
            'CommonPoolDescription': CommonPoolDescription,
        }

        game_cls = game_class_map[config_data['game_description_type']]
        game_description = game_cls(**config_data['game_description'])

        return cls(game_description=game_description,
                   repetitions=config_data['repetitions'])


@dataclass
class BatchTournamentConfig:
    """Configuration for multi-group fair tournament."""
    group_sizes: list[int]
    repetitions: int
    processes: int
    results_dir: str
    generator_name: str  # Key from STANDARD_GENERATORS

    def __post_init__(self):
        """Validate generator name exists."""
        if self.generator_name not in STANDARD_GENERATORS:
            available = list(STANDARD_GENERATORS.keys())
            raise ValueError(
                f"Unknown generator '{self.generator_name}'. Available: {available}"
            )

    @property
    def game_description_generator(self) -> Callable[[int], GameDescription]:
        """Get the game description generator function."""
        return STANDARD_GENERATORS[self.generator_name]

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchTournamentConfig':
        """Load BatchTournamentConfig from dictionary data."""
        return cls(**data)  # Simple since all fields are basic types


@dataclass
class CulturalEvolutionConfig:
    """Configuration for cultural evolution tournament."""
    game_description: GameDescription
    population_size: int
    top_k: int  # Number of survivors each generation
    mutation_rate: float  # Probability of mutation during reproduction
    threshold_pct: float  # Terminate when any gene reaches this % (0-1)
    max_generations: int
    repetitions_per_generation: int  # How many games each player plays per generation

    def __post_init__(self):
        """Validate configuration parameters."""
        if self.population_size <= 0:
            raise ValueError("population_size must be positive")

        if self.population_size % self.game_description.n_players != 0:
            raise ValueError(
                f"population_size ({self.population_size}) must be divisible by "
                f"n_players ({self.game_description.n_players})")

        if not (0 < self.top_k < self.population_size):
            raise ValueError(
                f"top_k ({self.top_k}) must be between 0 and population_size ({self.population_size})"
            )

        if not (0 <= self.mutation_rate <= 1):
            raise ValueError(
                f"mutation_rate must be between 0 and 1, got {self.mutation_rate}"
            )

        if not (0 < self.threshold_pct <= 1):
            raise ValueError(
                f"threshold_pct must be between 0 and 1, got {self.threshold_pct}"
            )

        if self.max_generations <= 0:
            raise ValueError("max_generations must be positive")

        if self.repetitions_per_generation <= 0:
            raise ValueError("repetitions_per_generation must be positive")
