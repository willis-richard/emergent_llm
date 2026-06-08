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

# claude-haiku-4-5/collective
class Strategy_ALTRUISTIC_76(BaseStrategy):
    """
    Threshold-Sensitive Cooperation with Adaptive Support.

    Cooperates based on observed cooperator counts from previous rounds,
    with time-dependent probabilities and special handling for threshold-near situations.
    Prioritizes completing the cooperation threshold for the group while adapting
    strategy based on observed cooperation levels and remaining rounds.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description

    def __call__(self, history: PlayerHistory) -> Action:
        n = self.game_description.n_players
        m = self.game_description.m
        r = self.game_description.n_rounds
        current_round = history.round_number
        if current_round == 0:
            p = min(1.0, 2.0 * m / n)
            return Action.C if random.random() < p else Action.D
        c_prev = history.opponent_cooperators[-1]
        if current_round == r - 1:
            if c_prev >= m - 1:
                return Action.C
            elif c_prev >= m - 2:
                return Action.C if random.random() < 0.75 else Action.D
            else:
                p = m / n * 0.5
                return Action.C if random.random() < p else Action.D
        if c_prev >= m - 1:
            return Action.C
        elif c_prev >= m - 2:
            return Action.C if random.random() < 0.8 else Action.D
        else:
            p = m / n * (r - current_round) / r
            return Action.C if random.random() < p else Action.D

# claude-haiku-4-5/selfish
class Strategy_OPPORTUNISTIC_109(BaseStrategy):
    """
    Opportunistic Threshold Rider - Free-rides on others' cooperation when sustainable,
    contributes only when threshold failure threatens payoffs. Stochastic insurance when
    threshold is at moderate risk.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.collapse_detected = False

    def __call__(self, history: PlayerHistory) -> Action:
        game = self.game_description
        round_num = history.round_number
        if round_num >= 2:
            if history.opponent_cooperators[-1] == 0 and history.opponent_cooperators[-2] == 0:
                self.collapse_detected = True
        if self.collapse_detected:
            return Action.D
        if round_num == game.n_rounds - 1:
            return Action.D
        if round_num == 0:
            return Action.D
        avg = np.mean(history.opponent_cooperators[:round_num])
        m = game.m
        n = game.n_players
        if avg >= m:
            return Action.D
        elif m - 2 <= avg < m:
            p = max(0.7, 1 - (m - avg) / (n - 1))
            if random.random() < p:
                return Action.D
            else:
                return Action.C
        else:
            return Action.C

# gemini-3.1-flash-lite-preview/collective
class Strategy_PROSOCIAL_101(BaseStrategy):
    """
    Threshold-Responsive Tit-for-Tat (TR-TFT):
    A strategy that adapts cooperation based on whether the collective threshold (m)
    was met in the previous round. It includes a recovery mechanism for past defections
    and a probabilistic noise component to test cooperation levels. It tracks
    consecutive failures to reach the threshold to implement a periodic punishment.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.n = game_description.n_players
        self.m = game_description.m
        self.k = game_description.k
        self.punishment_counter = 0

    def __call__(self, history: PlayerHistory) -> Action:
        if history.round_number == 0:
            return Action.C
        prev_round = history.round_number - 1
        c_prev_total = history.opponent_cooperators[prev_round] + int(history.my_actions[prev_round])
        others_c_prev = history.opponent_cooperators[prev_round]
        my_prev_action = history.my_actions[prev_round]
        if c_prev_total < self.m:
            self.punishment_counter += 1
        else:
            self.punishment_counter = 0
        if self.punishment_counter >= 3:
            if self.punishment_counter <= 4:
                return Action.D
            else:
                self.punishment_counter = 0
                return Action.C
        if c_prev_total >= self.m:
            return Action.C
        if my_prev_action:
            if others_c_prev == self.m - 1:
                return Action.D
            else:
                prob = 1.0 - c_prev_total / self.m
                if random.random() < prob:
                    return Action.C
                else:
                    return Action.D
        else:
            return Action.C

# gemini-3.1-flash-lite-preview/selfish
class Strategy_SELFINTERESTED_91(BaseStrategy):
    """
    Implements Conditional Reciprocity with Threshold Sensitivity:
    - Rounds 0-2 (first 3): Play Defect (D).
    - Rounds 3 to r-2:
        - If previous N_C >= m: Defect (D) to free-ride.
        - If previous N_C == m-1: Cooperate (C) with prob (k-1)/k to hit threshold.
        - Otherwise: Defect (D).
    - Final round (r-1): Same logic as standard rounds but treats the immediate payoff as the priority.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.m = game_description.m
        self.k = game_description.k
        self.r = game_description.n_rounds

    def __call__(self, history: PlayerHistory) -> Action:
        if history.round_number <= 2:
            return Action.D
        my_prev_action = history.my_actions[-1]
        others_prev_count = history.opponent_cooperators[-1]
        n_c_prev = (1 if my_prev_action else 0) + others_prev_count
        if n_c_prev >= self.m:
            return Action.D
        elif n_c_prev == self.m - 1:
            prob_c = (self.k - 1) / self.k
            if random.random() < prob_c:
                return Action.C
            else:
                return Action.D
        else:
            return Action.D

# gpt-5.4-mini/collective
class Strategy_ALTRUISTIC_97(BaseStrategy):
    """
    Forgiving threshold tracker for the Collective Risk Dilemma.

    - Cooperate in round 1.
    - In later rounds, respond to the previous round's cooperation level:
      * well above or at threshold: cooperate
      * one short: cooperate with probability 1/2
      * two or more short: defect
    - In the final round, be slightly more generous when exactly one short.
    - If the last two observed rounds both met the threshold, cooperate.
    - If the last two observed rounds were both below m-2, defect until recovery.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = int(game_description.n_players)
        self.n_rounds = int(game_description.n_rounds)
        self.m = int(game_description.m)
        self.k = float(game_description.k)

    def __call__(self, history: PlayerHistory) -> Action:
        round_number = int(history.round_number)
        if round_number == 0:
            return Action.C
        opp = history.opponent_cooperators
        last_x = int(opp[-1])
        threshold_opponents = self.m - 1
        one_short = self.m - 2
        low_zone_cutoff = self.m - 3
        prev_x = int(opp[-2]) if round_number >= 2 else None
        if prev_x is not None and prev_x >= threshold_opponents and (last_x >= threshold_opponents):
            return Action.C
        if prev_x is not None and prev_x <= one_short - 1 and (last_x <= one_short - 1):
            return Action.D
        if round_number == self.n_rounds - 1:
            if last_x >= threshold_opponents:
                return Action.C
            if last_x == one_short:
                return Action.C
            return Action.D
        if last_x >= threshold_opponents:
            return Action.C
        if last_x == one_short:
            return Action.C if random.random() < 0.5 else Action.D
        if last_x <= low_zone_cutoff:
            return Action.D
        return Action.D

# gpt-5.4-mini/selfish
class Strategy_OPPORTUNISTIC_6(BaseStrategy):
    """
    Knife-edge conditional cooperator:
    - Defect in round 1
    - Defect in the final round
    - In intermediate rounds, cooperate only when the previous round's opponent
      cooperations were exactly m-1 and the round before that was also at least m-1
      (or unavailable in round 2)
    - Otherwise defect
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.m = game_description.m
        self.k = game_description.k

    def __call__(self, history: PlayerHistory) -> Action:
        t = history.round_number + 1
        if t == 1:
            return Action.D
        if t == self.n_rounds:
            return Action.D
        if history.round_number >= 1:
            x_prev = int(history.opponent_cooperators[-1])
        else:
            x_prev = 0
        if history.round_number >= 2:
            x_prev2 = int(history.opponent_cooperators[-2])
        else:
            x_prev2 = None
        if x_prev >= self.m:
            return Action.D
        if x_prev == self.m - 1 and (t == 2 or (x_prev2 is not None and x_prev2 >= self.m - 1)):
            return Action.C
        return Action.D
