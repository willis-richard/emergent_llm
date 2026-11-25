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
class Strategy_ALTRUISTIC_15(BaseStrategy):
    """
    Altruistic Reciprocal Contribution Strategy for N-Player Public Goods Game.

    Cooperates in round 1, then adjusts cooperation probability based on the
    observed cooperation rate from the previous round. Maintains a strong bias
    toward cooperation across all conditions to signal willingness to cooperate
    and enable collective benefit.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description

    def __call__(self, history: PlayerHistory) -> Action:
        if history.round_number == 0:
            return Action.C
        cooperators_last_round = history.opponent_cooperators[-1]
        n_opponents = self.game_description.n_players - 1
        cooperation_rate = cooperators_last_round / n_opponents
        if cooperation_rate >= 0.5:
            return Action.C
        elif cooperation_rate >= 0.25:
            return Action.C if random.random() < 0.7 else Action.D
        elif cooperation_rate >= 0.1:
            return Action.C if random.random() < 0.4 else Action.D
        else:
            return Action.C if random.random() < 0.25 else Action.D

# claude-haiku-4-5/selfish
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

# gemini-3.1-flash-lite-preview/collective
class Strategy_BENEVOLENT_107(BaseStrategy):
    """
    A conditional cooperator strategy with a forgiving punishment mechanism.
    Maintains a 'Cooperative' or 'Punitive' state. If the number of cooperators
    falls below the sustainability threshold (floor(n/k)), the player defects
    and enters the 'Punitive' state. In subsequent rounds, the player attempts
    probabilistic reconciliation (50% chance) to return to cooperation.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.state = 0
        self.n = game_description.n_players
        self.k = game_description.k
        if self.k <= 0:
            self.threshold = self.n + 1
        else:
            self.threshold = math.floor(self.n / self.k)

    def __call__(self, history: PlayerHistory) -> Action:
        if self.k >= self.n - 1:
            return Action.C
        if self.k <= 1:
            return Action.D
        round_num = history.round_number
        if round_num == 0:
            self.state = 0
            return Action.C
        last_cooperators = history.opponent_cooperators[-1]
        if round_num == self.game_description.n_rounds - 1:
            if self.state == 0 and last_cooperators >= self.threshold:
                return Action.C
            return Action.D
        if self.state == 0:
            if last_cooperators >= self.threshold:
                self.state = 0
                return Action.C
            else:
                self.state = 1
                return Action.D
        elif random.random() < 0.5:
            self.state = 0
            return Action.C
        else:
            self.state = 1
            return Action.D

# gemini-3.1-flash-lite-preview/selfish
class Strategy_SELFISH_41(BaseStrategy):
    """
    A Win-Stay, Lose-Shift inspired strategy for N-player Public Goods Games.
    It defaults to defection, calculates cooperation thresholds, and uses
    probabilistic reciprocation when conditions favor it, while ensuring
    terminal defection.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        n = self.game_description.n_players
        k = self.game_description.k
        self.cooperation_threshold = math.ceil(n / k)

    def __call__(self, history: PlayerHistory) -> Action:
        current_round = history.round_number
        total_rounds = self.game_description.n_rounds
        if current_round == total_rounds - 1:
            return Action.D
        if current_round == 0:
            return Action.D
        last_action_c = bool(history.my_actions[-1])
        last_payoff = history.my_payoffs[-1]
        my_contribution = 1 if last_action_c else 0
        s_prev = history.opponent_cooperators[-1] + my_contribution
        if last_action_c:
            if last_payoff >= 1.0:
                return Action.C
            else:
                return Action.D
        elif s_prev < self.cooperation_threshold:
            return Action.D
        else:
            probability = s_prev / self.game_description.n_players
            if random.random() < probability:
                return Action.C
            else:
                return Action.D

# gpt-5.4-mini/collective
class Strategy_BENEVOLENT_12(BaseStrategy):
    """
    Benevolent public-goods strategy:
    - Cooperate initially.
    - Cooperate whenever the previous round met the cooperation floor.
    - Defect only after a recent round fell below the floor, and keep defecting
      until cooperation recovers.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        n = getattr(game_description, 'n_players', 0)
        self.floor = math.ceil(n / 2) if n and n > 0 else 1
        if self.floor < 1:
            self.floor = 1

    def __call__(self, history: PlayerHistory) -> Action:
        if history.round_number == 0:
            return Action.C
        n_players = getattr(self.game_description, 'n_players', 0)
        floor = self.floor if self.floor >= 1 else 1
        my_actions = history.my_actions
        opp_coop = history.opponent_cooperators
        bad_streak = 0
        rounds_played = history.round_number
        for idx in range(rounds_played - 1, -1, -1):
            my_cooperated = bool(my_actions[idx])
            x_t = int(opp_coop[idx]) if idx < len(opp_coop) else 0
            if x_t < 0:
                x_t = 0
            T_t = x_t + (1 if my_cooperated else 0)
            if T_t >= floor:
                break
            bad_streak += 1
        if bad_streak == 0:
            return Action.C
        return Action.D

# gpt-5.4-mini/selfish
class Strategy_SELFISH_31(BaseStrategy):
    """
    Default-defect strategy that only cooperates in the middle of the game
    after sustained, non-declining majority cooperation by opponents, with
    strict endgame defection and cooldowns after low-cooperation rounds.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n_players = int(game_description.n_players)
        self.n_rounds = int(game_description.n_rounds)
        self.k = float(game_description.k)
        self.n_opponents = max(0, self.n_players - 1)
        self.half_threshold_count = int(math.ceil(self.n_opponents / 2)) if self.n_opponents > 0 else 0

    def __call__(self, history: PlayerHistory) -> Action:
        t = history.round_number
        if t == 0:
            return Action.D
        if t == self.n_rounds - 1:
            return Action.D
        opp = history.opponent_cooperators
        played_rounds = len(opp)

        def rate_at(idx: int) -> float:
            if self.n_opponents <= 0:
                return 0.0
            return float(opp[idx]) / float(self.n_opponents)
        permanent_defect = False
        last_low_idx = -10 ** 9
        for i in range(played_rounds):
            if rate_at(i) < 0.5:
                if i > 0 and rate_at(i - 1) < 0.5:
                    permanent_defect = True
                    break
                last_low_idx = i
        if permanent_defect:
            return Action.D
        if t - last_low_idx <= 2 and last_low_idx >= 0:
            return Action.D
        if t == self.n_rounds - 2:
            if played_rounds >= 2:
                if rate_at(played_rounds - 1) == 1.0 and rate_at(played_rounds - 2) == 1.0:
                    return Action.C
            return Action.D
        q_t = rate_at(played_rounds - 1)
        streak = 0
        for i in range(played_rounds - 1, -1, -1):
            if rate_at(i) >= 0.5:
                streak += 1
            else:
                break
        if played_rounds >= 2:
            q_prev = rate_at(played_rounds - 2)
            drop = q_t < q_prev
        else:
            drop = False
        if t <= self.n_rounds - 2 and streak >= 2 and (q_t >= 0.5) and (not drop):
            return Action.C
        return Action.D
