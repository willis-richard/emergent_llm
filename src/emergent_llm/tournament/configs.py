from dataclasses import dataclass
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


@dataclass
class BatchTournamentConfig:
    """Configuration for multi-group fair tournament."""
    group_sizes: list[int]
    repetitions: int
    results_dir: str
    game_description_generator: Callable[[int], GameDescription]
