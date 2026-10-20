import logging
from pathlib import Path

from emergent_llm.common import C
from emergent_llm.common import COLLECTIVE
from emergent_llm.common import D
from emergent_llm.common import EXPLOITATIVE
from emergent_llm.common import GameDescription
from emergent_llm.common import GameState
from emergent_llm.common import Gene
from emergent_llm.common import PlayerHistory
from emergent_llm.games import CollectiveRiskDescription
from emergent_llm.games import CommonPoolDescription
from emergent_llm.games import CommonPoolGame
from emergent_llm.games import PublicGoodsDescription
from emergent_llm.generation import StrategyRegistry
from emergent_llm.players import Altenator
from emergent_llm.players import BaseStrategy
from emergent_llm.players import Cooperator
from emergent_llm.players import Defector
from emergent_llm.players import LLMPlayer
from emergent_llm.players import SimplePlayer
from emergent_llm.players import StrategySpec
from emergent_llm.tournament import BaseTournamentConfig
from emergent_llm.tournament import BatchCulturalEvolution
from emergent_llm.tournament import BatchCulturalEvolutionConfig
from emergent_llm.tournament import BatchCulturalEvolutionResults
from emergent_llm.tournament import BatchFairTournament
from emergent_llm.tournament import BatchFairTournamentResults
from emergent_llm.tournament import BatchMixtureTournament
from emergent_llm.tournament import BatchMixtureTournamentResults
from emergent_llm.tournament import BatchTournamentConfig
from emergent_llm.tournament import CulturalEvolution
from emergent_llm.tournament import CulturalEvolutionConfig
from emergent_llm.tournament import CulturalEvolutionResults
from emergent_llm.tournament import FairTournament
from emergent_llm.tournament import FairTournamentResults
from emergent_llm.tournament import MixtureTournament
from emergent_llm.tournament import MixtureTournamentResults

n = 5
players = [SimplePlayer("Def", Defector)]
# players = [SimplePlayer("Def", Altenator(D))]
for i in range(n - 1):
    players.append(SimplePlayer("Coop", Cooperator))
description = CommonPoolDescription(n_players=n, n_rounds=100, capacity=4 * n)

import time

start = time.time()
for _ in range(100000):
    for n in [2, 4, 10, 100]:
        description = CommonPoolDescription(n_players=n, n_rounds=10, capacity=4 * n)
        description.min_payoff()
        description.max_payoff()
        # print(description.min_payoff(), description.max_payoff())
end = time.time()
print(end - start)
# game = CommonPoolGame(players, description)
# results = game.play_game()

# print(results.history.payoffs[:,0])
