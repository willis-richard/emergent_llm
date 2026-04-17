import random
from typing import Callable

import numpy as np

from emergent_llm.common import C, D, Action, GameState, PlayerHistory

Cooperator = lambda _, __: C
Defector = lambda _, __: D
Random = lambda _, __: random.choice([C, D])
RandomCooperator = lambda _, __: C if np.random.random() < 0.9 else D
RandomDefector = lambda _, __: D if np.random.random() < 0.9 else C


class GradualDefector:
    def __init__(self, threshold=10):
        self.threshold = threshold

    def __call__(self, state: GameState, _: PlayerHistory):
        return C if state.round_number <= self.threshold else D


class PeriodicDefector:
    def __init__(self, period):
        self.period = period

    def __call__(self, state: GameState, _: PlayerHistory):
        return D if state.round_number % self.period == 0 else C


class Altenator:
    def __init__(self, initial_action: Action):
        self.action = initial_action

    def __call__(self, state: GameState, _: PlayerHistory):
        return self.action if state.round_number % 2 == 0 else self.action.flip()


class ConditionalCooperator:
    def __init__(self, initial_action: Action, threshold: int, include_self: bool = False):
        self.initial_action = initial_action
        self.threshold = threshold
        self.include_self = include_self

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number == 0:
            return self.initial_action

        last_opponent_cooperators = int(history.opponent_cooperators[-1])
        if self.include_self:
            total = last_opponent_cooperators + int(history.my_actions[-1])
            return C if total >= self.threshold else D
        return C if last_opponent_cooperators >= self.threshold else D


class ConditionalDefector:
    def __init__(self, initial_action: Action, threshold: int, include_self: bool = False):
        self.initial_action = initial_action
        self.threshold = threshold
        self.include_self = include_self

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number == 0:
            return self.initial_action

        last_opponent_cooperators = int(history.opponent_cooperators[-1])
        if self.include_self:
            total = last_opponent_cooperators + int(history.my_actions[-1])
            return D if total >= self.threshold else C
        return D if last_opponent_cooperators >= self.threshold else C


class HistoricalCooperator:
    def __init__(self, initial_action: Action, threshold: float, include_self: bool = False):
        self.initial_action = initial_action
        self.threshold = threshold
        self.include_self = include_self

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number == 0:
            return self.initial_action

        total_opponent_coops = int(history.opponent_cooperators.sum())
        if self.include_self:
            total = total_opponent_coops + int(history.my_actions.sum())
            avg = total / state.round_number
        else:
            avg = total_opponent_coops / state.round_number
        return C if avg >= self.threshold else D


class AntiTFT:
    def __init__(self, initial_action: Action, threshold: int):
        self.initial_action = initial_action
        self.threshold = threshold

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number == 0:
            return self.initial_action
        return D if int(history.opponent_cooperators[-1]) >= self.threshold else C


class FirstImpressions:
    def __init__(self, initial_action: Action, threshold: int):
        self.initial_action = initial_action
        self.threshold = threshold

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number == 0:
            return self.initial_action
        return C if int(history.opponent_cooperators[0]) >= self.threshold else D


class Flipper:
    def __init__(self, flip_action: Action, n_rounds: int,
                 default: Callable[[GameState, PlayerHistory], Action]):
        self.flip_action = flip_action
        self.n_rounds = n_rounds
        self.default = default

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number >= self.n_rounds and \
           all(a == self.flip_action
               for a in Action.from_bool_array(history.my_actions[-self.n_rounds:])):
            return self.flip_action.flip()
        return self.default(state, history)


class SpecialRounds:
    def __init__(self, default: Callable[[GameState, PlayerHistory], Action],
                 special: Callable[[GameState, PlayerHistory], Action],
                 rounds: list[int]):
        self.default = default
        self.special = special
        self.rounds = rounds

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number in self.rounds:
            return self.special(state, history)
        return self.default(state, history)
