"""
Strategies that are closest to the centroid mean, for each LLM
"""

from dataclasses import dataclass
from enum import Enum
import math
import numpy as np
from numpy.typing import NDArray
import random

from emergent_llm.players import BaseStrategy
from emergent_llm.games import PublicGoodsDescription, CollectiveRiskDescription, CommonPoolDescription
from emergent_llm.common import Action, C, D, PlayerHistory

# claude-haiku-4-5
class Strategy_ALTRUISTIC_49(BaseStrategy):
    """
    Altruistic Public Goods Strategy that signals cooperation in round 1,
    adapts based on others' behavior in mid-game with a baseline altruistic floor,
    and uses stricter thresholds in the final round to avoid exploitation.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.r = game_description.n_rounds
        self.k = game_description.k

    def __call__(self, history: PlayerHistory) -> Action:
        round_num = history.round_number
        if round_num == 0:
            return Action.C
        baseline = (1 - self.k / self.n) * 0.5
        if baseline < 0:
            baseline = 0.3
        others_cooperated = history.opponent_cooperators[-1]
        others_cooperation_rate = others_cooperated / (self.n - 1)
        if round_num == self.r - 1:
            threshold = (1 - self.k / self.n) * 0.75
            if others_cooperation_rate >= threshold:
                return Action.C
            if random.random() < 0.4:
                return Action.C
            return Action.D
        p_cooperate = others_cooperation_rate + baseline
        p_cooperate = min(1.0, max(0.0, p_cooperate))
        if random.random() < p_cooperate:
            return Action.C
        return Action.D

# claude-haiku-4-5
class Strategy_INDIVIDUALISTIC_16(BaseStrategy):
    """
    Adaptive Threshold Exploitation Strategy for N-Player Public Goods Game.
    
    Gathers information in early rounds, applies threshold-based probabilistic 
    cooperation in middle rounds based on observed cooperation rates, and defects 
    in the final round to maximize immediate payoff.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.threshold = math.ceil(game_description.k)

    def __call__(self, history: PlayerHistory) -> Action:
        round_number = history.round_number
        n_rounds = self.game_description.n_rounds
        n_players = self.game_description.n_players
        if round_number <= 1:
            return Action.D
        if round_number == n_rounds - 1:
            return Action.D
        m_t_minus_1 = history.opponent_cooperators[-1]
        if m_t_minus_1 >= self.threshold:
            p = (m_t_minus_1 - 1) / n_players
            if random.random() < p:
                return Action.C
            else:
                return Action.D
        else:
            return Action.D

# gemini-3.1-flash-lite-preview
class Strategy_ALTRUISTIC_7(BaseStrategy):
    """
    Implements conditional reciprocity with a forgiveness mechanism for an N-Player Public Goods Game.
    Starts by cooperating, then dynamically adjusts cooperation based on whether the total 
    number of cooperators meets a threshold required for individual rationality. 
    Includes a probabilistic response to insufficient cooperation and defects on the final round.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.threshold = self.game_description.n_players / self.game_description.k + 0.1

    def __call__(self, history: PlayerHistory) -> Action:
        current_round = history.round_number
        if current_round == 0:
            return Action.C
        if current_round == self.game_description.n_rounds - 1:
            return Action.D
        last_observed_cooperators = history.opponent_cooperators[-1]
        if last_observed_cooperators >= self.threshold:
            return Action.C
        else:
            prob_cooperate = max(0.0, last_observed_cooperators / self.threshold)
            if random.random() < prob_cooperate:
                return Action.C
            else:
                return Action.D

# gemini-3.1-flash-lite-preview
class Strategy_SELFINTERESTED_65(BaseStrategy):
    """
    Win-Stay, Lose-Shift with Threshold-Based Reciprocity.
    
    Target threshold T = n/k.
    1. Round 1: Always Cooperate (C).
    2. Last Round (r): Always Defect (D).
    3. Intermediate Rounds (1 < t < r):
       - Based on previous round result (my_action, total_cooperators):
         - If (C and C_{t-1} >= T) OR (D and C_{t-1} >= T): Stay/Switch to C.
         - If (C and C_{t-1} < T) OR (D and C_{t-1} < T): Stay/Switch to D.
       - Exception Handling (Stochastic):
         - If C_{t-1} == T - 1, play C with 50% probability.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.threshold = self.game_description.n_players / self.game_description.k

    def __call__(self, history: PlayerHistory) -> Action:
        if history.round_number == 0:
            return Action.C
        if history.round_number == self.game_description.n_rounds - 1:
            return Action.D
        last_action = history.my_actions[-1]
        c_prev = history.opponent_cooperators[-1]
        t_floor = math.floor(self.threshold)
        if c_prev == t_floor - 1:
            return Action.C if random.random() < 0.5 else Action.D
        if c_prev >= self.threshold:
            return Action.C
        else:
            return Action.D

# gpt-5.4-mini
class Strategy_ALTRUISTIC_42(BaseStrategy):
    """
    Adaptive public-goods strategy:
    - Cooperate in round 1.
    - Afterwards, respond to the previous round's opponent cooperation rate q.
    - Include special handling for repeated zero-cooperation streaks,
      periodic generosity, and a last-round cooperation bias.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds

    def __call__(self, history: PlayerHistory) -> Action:
        round_number = history.round_number
        if round_number == 0:
            return Action.C
        n_opponents = max(self.n_players - 1, 1)
        last_opponents = int(history.opponent_cooperators[-1])
        q = last_opponents / n_opponents
        zero_streak = 0
        idx = round_number - 1
        while idx >= 0 and int(history.opponent_cooperators[idx]) == 0:
            zero_streak += 1
            idx -= 1
        is_last_round = round_number == self.n_rounds - 1
        is_fourth_round = (round_number + 1) % 4 == 0
        if zero_streak >= 2 and q == 0:
            return Action.D
        if is_last_round and q >= 0.25:
            return Action.C
        if is_fourth_round and q > 0:
            return Action.C
        if q >= 0.5:
            return Action.C
        if q >= 0.25:
            return Action.C if random.random() < 2.0 * q else Action.D
        return Action.D

# gpt-5.4-mini
class Strategy_SELFINTERESTED_124(BaseStrategy):
    """
    Adaptive public-goods strategy:
    - Start with defection.
    - Cooperate only after sustained high cooperation is observed.
    - Enter defection mode after collapse signals.
    - Never cooperate in the last two rounds.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.defection_mode = False

    def __call__(self, history: PlayerHistory) -> Action:
        n_rounds = self.game_description.n_rounds
        n_players = self.game_description.n_players
        n_opponents = max(1, n_players - 1)

        def q_at(idx: int) -> float:
            if idx < 0 or idx >= history.round_number:
                return 0.0
            return float(history.opponent_cooperators[idx]) / float(n_opponents)
        if history.round_number == 0:
            self.defection_mode = False
            return Action.D
        if history.round_number >= n_rounds - 2:
            self.defection_mode = True
            return Action.D
        last_q = q_at(history.round_number - 1)
        prev_q = q_at(history.round_number - 2)
        if self.defection_mode:
            if last_q == 1.0 or (history.round_number >= 2 and last_q >= 2.0 / 3.0 and (prev_q >= 2.0 / 3.0)):
                self.defection_mode = False
            else:
                return Action.D
        elif history.round_number >= 2 and last_q <= 1.0 / 3.0 and (prev_q <= 1.0 / 3.0):
            self.defection_mode = True
            return Action.D
        window_len = min(3, history.round_number)
        if window_len <= 0:
            avg_q = 0.0
        else:
            start = history.round_number - window_len
            qs = [q_at(i) for i in range(start, history.round_number)]
            avg_q = float(np.mean(qs)) if qs else 0.0
        trend = last_q - prev_q
        if avg_q >= 2.0 / 3.0 and prev_q >= 2.0 / 3.0 and (trend >= 0.0):
            return Action.C
        return Action.D

