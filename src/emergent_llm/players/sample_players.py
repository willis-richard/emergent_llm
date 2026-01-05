import random
from typing import Callable

import numpy as np

from emergent_llm.common import C, D, Action, GameState, PlayerHistory

Cooperator = lambda _, __: C
Defector = lambda _, __: D
Random = lambda _, __ : random.choice([C, D])
RandomCooperator = lambda _, __: C if np.random.random() < 0.9 else D
RandomDefector = lambda _, __: D if np.random.random() < 0.9 else C

class GradualDefector:

    def __init__(self, threshold=10):
        self.threshold = threshold

    def __call__(self, state: GameState, _):
        return C if state.round_number <= self.threshold else D

class PeriodicDefector:

    def __init__(self, period):
        self.period = period

    def __call__(self, state: GameState, _):
        return D if state.round_number % self.period == 0 else C

class Altenator:

    def __init__(self, initial_action: Action):
        self.action = initial_action

    def __call__(self, state: GameState, _):
        return self.action if state.round_number % 2 == 0 else self.action.flip()

class ConditionalCooperator:

    def __init__(self, initial_action: Action, threshold: int, include_self: bool = False):
        self.initial_action = initial_action
        self.threshold = threshold
        self.include_self = include_self

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return self.initial_action
        assert history is not None

        if self.include_self:
            return C if (sum(history.opponent_actions[-1,:]) + history.my_actions[-1]) >= self.threshold else D
        return C if sum(history.opponent_actions[-1,:]) >= self.threshold else D

class HistoricalCooperator:

    def __init__(self, initial_action: Action, threshold: int, include_self: bool = False):
        self.initial_action = initial_action
        self.threshold = threshold
        self.include_self = include_self

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return self.initial_action
        assert history is not None

        if self.include_self:
            return C if (np.sum(history.opponent_actions) + sum(history.my_actions)) / state.round_number >= self.threshold else D
        return C if np.sum(history.opponent_actions) / state.round_number >= self.threshold else D

class AntiTFT:

    def __init__(self, initial_action: Action, threshold: int):
        self.initial_action = initial_action
        self.threshold = threshold

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return self.initial_action
        assert history is not None

        return D if sum(history.opponent_actions[-1,:]) >= self.threshold else C

class Grim:

    def __init__(self, initial_action: Action, threshold: int):
        self.initial_action = initial_action
        self.threshold = threshold

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return self.initial_action
        assert history is not None

        number_opponents_who_have_defected = (~history.opponent_actions.all(axis=0)).sum()
        return D if number_opponents_who_have_defected >= self.threshold else C

class AntiGrim:

    def __init__(self, initial_action: Action, threshold: int):
        self.initial_action = initial_action
        self.threshold = threshold

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return self.initial_action
        assert history is not None

        number_opponents_who_have_cooperated = np.any(history.opponent_actions, axis=0).sum()
        return C if number_opponents_who_have_cooperated >= self.threshold else D

class FirstImpressions:

    def __init__(self, initial_action: Action, threshold: int):
        self.initial_action = initial_action
        self.threshold = threshold

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return self.initial_action
        assert history is not None

        return C if sum(history.opponent_actions[0,:]) >= self.threshold else D

class Flipper:
    def __init__(self, flip_action: Action, n_rounds: int, default: Callable[[GameState, PlayerHistory | None], Action]):
        self.flip_action = flip_action
        self.n_rounds = n_rounds
        self.default = default

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number != 0 and \
           len(history.my_actions) >= self.n_rounds + 1 and \
           all(a == self.flip_action for a in Action.from_bool_array(history.my_actions[-self.n_rounds:])):
            return self.flip_action.flip()
        return self.default(state, history)

class SpecialRounds:
    def __init__(self, default: Callable[[GameState, PlayerHistory | None], Action], special: Callable[[GameState, PlayerHistory | None], Action], rounds: list[int]):
        self.default = default
        self.special = special
        self.rounds = rounds

    def __call__(self, state: GameState, history: PlayerHistory | None) -> Action:
        if state.round_number in self.rounds:
            return self.special(state, history)
        return self.default(state, history)
