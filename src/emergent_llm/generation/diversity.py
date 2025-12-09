from itertools import combinations_with_replacement, product

import numpy as np

from emergent_llm.common import COLLECTIVE, EXPLOITATIVE, C, D, Gene
from emergent_llm.games import PublicGoodsDescription, PublicGoodsGame
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.players import LLMPlayer, SimplePlayer

model = "claude-sonnet-4-0"
registry = StrategyRegistry("strategies", "public_goods", [model])
gene = Gene(model, EXPLOITATIVE)
algo = registry.get_all_specs(gene)[0].strategy_class
print(algo.__name__)

n_rounds = 5
n_opponents = 3
n_games = 10

all_actions = tuple(combination for combination in product([D, C], repeat=n_rounds))
print(len(all_actions))

unique_combos = tuple(combinations_with_replacement(all_actions, n_opponents))
print(len(unique_combos))


class FixedOpponent:
    fixed_actions = None

    def __call__(self, round_number: int):
        return self.fixed_actions[round_number]

opponent_1 = SimplePlayer("opponent_1", FixedOpponent())
opponent_2 = SimplePlayer("opponent_2", FixedOpponent())
opponent_3 = SimplePlayer("opponent_3", FixedOpponent())

description = PublicGoodsDescription(n_players=n_opponents+1, n_rounds=n_rounds, k=2)
player = LLMPlayer("testing", gene, description, algo)


i = 0
output = []
for combo in unique_combos:
    actions_1, actions_2, actions_3 = combo
    opponent_1.strategy_function.fixed_actions = actions_1
    opponent_2.strategy_function.fixed_actions = actions_2
    opponent_3.strategy_function.fixed_actions = actions_3
    players = [player, opponent_1, opponent_2, opponent_3]

    results = [PublicGoodsGame(players, description).play_game() for _ in range(n_games)]
    actions = [r.history.actions[:,0] for r in results]
    mean_C = np.mean(actions, axis=0)
    output += [mean_C]

features = np.concatenate(output)
print(np.mean(features))
