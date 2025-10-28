from typing import Callable

from emergent_llm.games.base_game import BaseGame, GameDescription
from emergent_llm.games.collective_risk import CollectiveRiskDescription, CollectiveRiskGame
from emergent_llm.games.common_pool import CommonPoolDescription, CommonPoolGame
from emergent_llm.games.public_goods import PublicGoodsDescription, PublicGoodsGame


def get_game_class(game_type: str) -> type[BaseGame]:
    """Get game class based on type."""
    if game_type == "public_goods":
        return PublicGoodsGame
    elif game_type == "collective_risk":
        return CollectiveRiskGame
    elif game_type == "common_pool":
        return CommonPoolGame
    else:
        raise ValueError(f"Unknown game type: {game_type}")


STANDARD_GENERATORS: dict[str, Callable] = {
    'public_goods_default':
        lambda n_players, n_rounds=20: PublicGoodsDescription(
            n_players=n_players, n_rounds=n_rounds, k=2.0),
    'collective_risk_default':
        lambda n_players, n_rounds=20: CollectiveRiskDescription(
            n_players=n_players,
            n_rounds=n_rounds,
            m=max(2, n_players // 2),
            k=2.0),
    'common_pool_default':
        lambda n_players, n_rounds=20: CommonPoolDescription(
            n_players=n_players, n_rounds=n_rounds, capacity=n_players * 4),
}
