import random

import numpy as np

from emergent_llm.common import C, D

Cooperator = lambda x: C
Defector = lambda x: D
Random = lambda x : random.choice([C, D])
RandomCooperator = lambda x: C if np.random.random() < 0.9 else D
RandomDefector = lambda x: D if np.random.random() < 0.9 else C

class GradualDefector:

    def __init__(self, threshold=10):
        self.threshold = threshold

    def __call__(self, round_number: int):
        return C if round_number <= self.threshold else D

class PeriodicDefector:

    def __init__(self, period):
        self.period = period

    def __call__(self, round_number: int):
        return D if round_number % self.period == 0 else C
