import random

import numpy as np

from emergent_llm.common import C, D

Cooperator = lambda _, __: C
Defector = lambda _, __: D
Random = lambda _, __ : random.choice([C, D])
RandomCooperator = lambda _, __: C if np.random.random() < 0.9 else D
RandomDefector = lambda _, __: D if np.random.random() < 0.9 else C

class GradualDefector:

    def __init__(self, threshold=10):
        self.threshold = threshold

    def __call__(self, state, _):
        return C if state.round_number <= self.threshold else D

class PeriodicDefector:

    def __init__(self, period):
        self.period = period

    def __call__(self, state, _):
        return D if state.round_number % self.period == 0 else C

class ConditionalCooperator:

    def __init__(self, threshold):
        self.threshold = threshold

    def __call__(self, state, history):
        if state.round_number == 0:
            return C
        return D if sum(history.opponent_actions[-1,:]) >= self.threshold else C
