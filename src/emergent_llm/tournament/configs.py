from dataclasses import dataclass, asdict
from typing import Callable

from emergent_llm.common import GameDescription
from emergent_llm.games import (BaseGame, CollectiveRiskDescription,
                                CollectiveRiskGame, CommonPoolDescription,
                                CommonPoolGame, PublicGoodsDescription,
                                PublicGoodsGame)


@dataclass
class BaseTournamentConfig:
    game_description: GameDescription
    repetitions: int = 1

    def get_game_class(self) -> type[BaseGame]:
        """Get appropriate game class from description type."""
        if isinstance(self.game_description, PublicGoodsDescription):
            return PublicGoodsGame
        elif isinstance(self.game_description, CollectiveRiskDescription):
            return CollectiveRiskGame
        elif isinstance(self.game_description, CommonPoolDescription):
            return CommonPoolGame
        else:
            raise ValueError(f"No game class found for description type: {type(self.game_description)}")

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

        return cls(
            game_description=game_description,
            repetitions=config_data['repetitions']
        )


@dataclass
class BatchTournamentConfig:
    """Configuration for multi-group fair tournament."""
    group_sizes: list[int]
    repetitions: int
    results_dir: str
    generator_name: str  # Key from STANDARD_GENERATORS

    def __post_init__(self):
        """Validate generator name exists."""
        if self.generator_name not in STANDARD_GENERATORS:
            available = list(STANDARD_GENERATORS.keys())
            raise ValueError(f"Unknown generator '{self.generator_name}'. Available: {available}")

    @property
    def game_description_generator(self) -> Callable[[int], GameDescription]:
        """Get the game description generator function."""
        return STANDARD_GENERATORS[self.generator_name]

    @classmethod
    def from_dict(cls, data: dict) -> 'BatchTournamentConfig':
        """Load BatchTournamentConfig from dictionary data."""
        return cls(**data)  # Simple since all fields are basic types



STANDARD_GENERATORS: dict[str, Callable[[int], GameDescription]] = {
    'public_goods_default': lambda n: PublicGoodsDescription(
        n_players=n, n_rounds=20, k=2.0
    ),
    'collective_risk_default': lambda n: CollectiveRiskDescription(
        n_players=n, n_rounds=20, m=max(2, n//2), k=2.0
    ),
    'common_pool_default': lambda n: CommonPoolDescription(
        n_players=n, n_rounds=20, capacity=n*4
    ),
}
