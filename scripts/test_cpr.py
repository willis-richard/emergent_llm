import logging
from pathlib import Path

from emergent_llm.common import (
    COLLECTIVE,
    EXPLOITATIVE,
    C,
    D,
    GameDescription,
    GameState,
    Gene,
    PlayerHistory,
)
from emergent_llm.games import CollectiveRiskDescription, PublicGoodsDescription, CommonPoolDescription, CommonPoolGame
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import BaseStrategy, LLMPlayer, StrategySpec, SimplePlayer, Cooperator, Defector, Altenator
from emergent_llm.tournament import (
    BaseTournamentConfig,
    BatchFairTournament,
    BatchFairTournamentResults,
    BatchMixtureTournament,
    BatchMixtureTournamentResults,
    BatchTournamentConfig,
    FairTournament,
    FairTournamentResults,
    MixtureTournament,
    MixtureTournamentResults,
    CulturalEvolutionConfig,
    CulturalEvolution,
    CulturalEvolutionResults,
    BatchCulturalEvolutionConfig,
    BatchCulturalEvolution,
    BatchCulturalEvolutionResults
)


n=5
players = [SimplePlayer("Def", Defector)]
# players = [SimplePlayer("Def", Altenator(D))]
for i in range(n-1):
    players.append(SimplePlayer("Coop", Cooperator))
description = CommonPoolDescription(n_players = n, n_rounds=100, capacity=4*n)

import time
start = time.time()
for _ in range(100000):
    for n in [2, 4, 10, 100]:
        description = CommonPoolDescription(n_players = n, n_rounds=10, capacity=4*n)
        description.min_payoff()
        description.max_payoff()
        # print(description.min_payoff(), description.max_payoff())
end = time.time()
print(end - start)
    # game = CommonPoolGame(players, description)
    # results = game.play_game()

    # print(results.history.payoffs[:,0])
