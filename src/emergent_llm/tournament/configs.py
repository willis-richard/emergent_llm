from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable

from emergent_llm.common import GameDescription, Gene
from emergent_llm.games import (
    STANDARD_GENERATORS,
    CollectiveRiskDescription,
    CommonPoolDescription,
    PublicGoodsDescription,
)


class OutputStyle(StrEnum):
    FULL = "full"
    COMPRESSED = "compressed"
    SUMMARY = "summary"

    def get_suffix(self) -> str:
        return ".json.gz" if self.value == OutputStyle.COMPRESSED else ".json"


@dataclass(frozen=True)
class MixtureKey:
    n_collective: int
    n_exploitative: int


@dataclass
class BaseTournamentConfig:
    game_description: GameDescription
    repetitions: int = 1
    n_processes: int = 1

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
@dataclass
class BatchTournamentConfig:
    """Configuration for batch tournaments (fair or mixture)."""
    group_sizes: list[int]
    repetitions: int
    generator_name: str  # Key from STANDARD_GENERATORS
    n_processes: int
    output_dir: str
    output_style: OutputStyle

    def __post_init__(self):
        if isinstance(self.output_style, str):
            self.output_style = OutputStyle(self.output_style)
        if self.generator_name not in STANDARD_GENERATORS:
            available = list(STANDARD_GENERATORS.keys())
            raise ValueError(
                f"Unknown generator '{self.generator_name}'. Available: {available}"
            )

    @property
    def game_description_generator(self) -> Callable[..., GameDescription]:
        return STANDARD_GENERATORS[self.generator_name]


@dataclass(frozen=True)
class SurvivorRecord:
    """Record of a survivor from selection."""
    gene: Gene
    strategy_name: str
    fitness: float

    def to_dict(self) -> dict:
        return {
            'gene': {
                'model': self.gene.model,
                'attitude': self.gene.attitude.value
            },
            'strategy_name': self.strategy_name,
            'fitness': self.fitness
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SurvivorRecord':
        gene = Gene.from_dict(data['gene'])
        return cls(gene=gene,
                   strategy_name=data['strategy_name'],
                   fitness=data['fitness'])

    @property
    def name(self):
        return f"{self.gene}[{self.strategy_name}]"


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


@dataclass
class BatchCulturalEvolutionConfig:
    """Configuration for batch cultural evolution tournament with incremental saving."""
    evolution_config: CulturalEvolutionConfig
    n_runs: int
    n_processes: int
    results_dir: str
    output_style: OutputStyle

    strategies_dir: str
    game_name: str
    models: list[str] | None = None

    def __post_init__(self):
        if self.n_runs <= 0:
            raise ValueError("n_runs must be positive")
        if self.n_processes <= 0:
            raise ValueError("n_processes must be positive")
        if isinstance(self.output_style, str):
            self.output_style = OutputStyle(self.output_style)

    @property
    def output_dir(self) -> Path:
        """Full output directory including experiment subdirectory."""
        return Path(
            self.results_dir
        ) / "cultural_evolution" / self.game_name / self._experiment_dir_name

    @property
    def _experiment_dir_name(self) -> str:
        """Generate unique experiment directory name from config."""

        cfg = self.evolution_config
        gd = cfg.game_description

        parts = [
            f"n{gd.n_players}",
            f"r{gd.n_rounds}",
            f"pop{cfg.population_size}",
            f"top{cfg.top_k}",
            f"mut{cfg.mutation_rate}",
            f"thr{cfg.threshold_pct}",
            f"gen{cfg.max_generations}",
            f"rep{cfg.repetitions_per_generation}",
        ]

        if self.models:
            models_str = "-".join(sorted(self.models))
            parts.append(f"models_{models_str}")

        return "_".join(parts)
