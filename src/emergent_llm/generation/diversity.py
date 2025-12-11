from itertools import combinations_with_replacement, product
from collections import defaultdict

import numpy as np

from emergent_llm.common import COLLECTIVE, EXPLOITATIVE, C, D, Gene, Action
from emergent_llm.games import PublicGoodsDescription, PublicGoodsGame
from emergent_llm.generation.strategy_registry import StrategyRegistry
from emergent_llm.players import LLMPlayer, SimplePlayer, RandomCooperator

model = "claude-sonnet-4-0"
registry = StrategyRegistry("strategies", "public_goods", [model])
gene = Gene(model, EXPLOITATIVE)

n_rounds = 5
n_opponents = 3
n_games = 10

all_actions = tuple(combination for combination in product([D, C], repeat=n_rounds - 1))
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

# player = SimplePlayer("player", RandomCooperator)



def hashable(arr):
    return tuple(map(tuple, arr))

output = []

def compute_features(player):
    features = defaultdict(list)
    for combo in unique_combos:
        actions_1, actions_2, actions_3 = combo
        # last round action of opponents does not matter
        opponent_1.strategy_function.fixed_actions = list(actions_1) + [C]
        opponent_2.strategy_function.fixed_actions = list(actions_2) + [C]
        opponent_3.strategy_function.fixed_actions = list(actions_3) + [C]
        players = [player, opponent_1, opponent_2, opponent_3]

        results = [PublicGoodsGame(players, description).play_game() for _ in range(n_games)]
        player_history = results[0].history.for_player(0)
        for r in range(0, n_rounds):
            context = Action.from_bool_array(player_history.opponent_actions[:r])
            actions = [Action(result.history.actions[r,0]) for result in results]
            features[hashable(context)] += actions
    return features

for i in range(5):
    algo = registry.get_all_specs(gene)[i].strategy_class
    print(algo.__name__)
    player = LLMPlayer("testing", gene, description, algo)

    features = compute_features(player)
    all_values = [x for v in features.values() for x in Action.to_bool_array(v)]
    mean = sum(all_values) / len(all_values)
    print(mean)


# print(features)
# feature_means = {k: sum(Action.to_bool_array(v)) / len(v) for k, v in features.items()}
# print(feature_means)
# all_values = [x for v in features.values() for x in Action.to_bool_array(v)]
# mean = sum(all_values) / len(all_values)
# print(mean)
