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
class Strategy_ALTRUISTIC_55(BaseStrategy):
    """
    Altruistic Collective Risk Strategy with reciprocity and endgame boost.
    
    Leads with cooperation, maintains baseline willingness to contribute,
    and concentrates altruistic effort in final rounds.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_opponents = game_description.n_players - 1

    def __call__(self, history: PlayerHistory) -> Action:
        round_num = history.round_number
        r = self.game_description.n_rounds
        m = self.game_description.m
        if round_num == 0:
            return Action.C
        prev_cooperators = history.opponent_cooperators[round_num - 1]
        observed_coop_rate = prev_cooperators / self.n_opponents if self.n_opponents > 0 else 0.0
        base_altruism = 0.6
        reciprocity_weight = 0.3
        if round_num >= 3:
            recent_coop = history.opponent_cooperators[round_num - 3:round_num]
            coop_avg = np.mean(recent_coop) / self.n_opponents if self.n_opponents > 0 else 0.0
            prev_coop = history.opponent_cooperators[max(0, round_num - 4):round_num - 1]
            prev_avg = np.mean(prev_coop) / self.n_opponents if self.n_opponents > 0 else 0.0
            if coop_avg < prev_avg:
                reciprocity_weight = 0.4
        reciprocity_factor = min(0.2, observed_coop_rate * reciprocity_weight)
        endgame_boost = 0.15 if round_num > 0.8 * r else 0.0
        if round_num >= 3:
            recent_coop = history.opponent_cooperators[round_num - 3:round_num]
            coop_avg = np.mean(recent_coop) / self.n_opponents if self.n_opponents > 0 else 0.0
            prev_coop = history.opponent_cooperators[max(0, round_num - 4):round_num - 1]
            prev_avg = np.mean(prev_coop) / self.n_opponents if self.n_opponents > 0 else 0.0
            if coop_avg > prev_avg and coop_avg > 0:
                endgame_boost = max(0.0, endgame_boost - 0.05)
        p_coop = base_altruism + reciprocity_factor + endgame_boost
        if prev_cooperators >= m - 1:
            p_coop += 0.1
        if observed_coop_rate < 0.3:
            p_coop = max(p_coop, 0.55)
        if round_num == r - 1:
            p_coop += 0.25
        return Action.C if random.random() < p_coop else Action.D

# claude-haiku-4-5
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

# gemini-3.1-flash-lite-preview
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

# gemini-3.1-flash-lite-preview
class Strategy_OPPORTUNISTIC_29(BaseStrategy):
    """
    Implements the Conditional Threshold-Opportunist strategy.
    
    This strategy aims to maximize payoffs by contributing just enough to reach 
    the threshold when necessary, free-riding when the threshold is safe, 
    and conserving resources when the group is uncooperative.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.consecutive_underperformance = 0

    def __call__(self, history: PlayerHistory) -> Action:
        n = self.game_description.n_players
        m = self.game_description.m
        k = self.game_description.k
        r = self.game_description.n_rounds
        t = history.round_number
        if k <= 1.0:
            return Action.D
        if t == 0:
            if random.random() < m / n:
                return Action.C
            return Action.D
        last_my_action = history.my_actions[-1]
        last_my_contrib = 1 if last_my_action else 0
        last_total_cooperators = history.opponent_cooperators[-1] + last_my_contrib
        if last_total_cooperators < m - 1:
            self.consecutive_underperformance += 1
        else:
            self.consecutive_underperformance = 0
        if self.consecutive_underperformance >= 3:
            return Action.D
        if t == r - 1:
            return Action.D
        threshold_met = last_total_cooperators >= m
        if threshold_met:
            return Action.D
        else:
            if last_total_cooperators == m - 1:
                return Action.C
            return Action.D

# gpt-5.4-mini
class Strategy_PROSOCIAL_69(BaseStrategy):
    """
    Adaptive collective-risk strategy:
    - Cooperate initially.
    - Reward recent cooperation with continued cooperation.
    - Enter a defensive mode after clear defections.
    - Use a bounded trust variable to smooth decisions.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.trust = 0

    def __call__(self, history: PlayerHistory) -> Action:
        n = self.game_description.n_players
        m = self.game_description.m
        r = self.game_description.n_rounds
        threshold = m - 1
        x_prev = int(history.opponent_cooperators[-1]) if history.round_number > 0 else 0
        if history.round_number == 0:
            self.trust = 0
            return Action.C
        if x_prev >= threshold:
            self.trust = min(3, self.trust + 1)
        elif x_prev <= m - 3:
            self.trust = max(-3, self.trust - 2)
        if history.round_number >= 2:
            x_prev2 = int(history.opponent_cooperators[-2])
            if x_prev >= threshold and x_prev2 >= threshold:
                self.trust = 3
            elif x_prev < threshold and x_prev2 < threshold:
                self.trust = -3
        if history.round_number == r - 1:
            if x_prev >= threshold:
                return Action.C
            return Action.C if self.trust >= 0 else Action.D
        if x_prev >= threshold:
            return Action.C
        if x_prev == m - 2:
            if history.round_number >= 2:
                x_prev2 = int(history.opponent_cooperators[-2])
                if x_prev2 >= threshold:
                    return Action.C
            return Action.C if random.random() < 0.5 else Action.D
        return Action.C if self.trust >= 0 else Action.D

# gpt-5.4-mini
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

