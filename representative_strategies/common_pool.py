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
class Strategy_PROSOCIAL_75(BaseStrategy):
    """
    Adaptive Reciprocal Stewardship Strategy: A prosocial approach that defaults to
    cooperation, uses graduated punishment based on opponent behavior, and prioritizes
    collective resource sustainability especially during stock depletion.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description

    def __call__(self, history: PlayerHistory, current_stock: float) -> Action:
        n_players = self.game_description.n_players
        n_rounds = self.game_description.n_rounds
        capacity = self.game_description.capacity
        if history.round_number == 0:
            return Action.C
        opp_coop_count = history.opponent_cooperators[-1]
        coop_rate = opp_coop_count / (n_players - 1) if n_players > 1 else 0
        stock_health = current_stock / capacity if capacity > 0 else 0
        rounds_remaining = n_rounds - history.round_number
        if coop_rate >= 0.5:
            defect_prob = 0.0
        elif coop_rate >= 0.25:
            defect_prob = (0.5 - coop_rate) / 0.25
        else:
            defect_prob = 0.8
        if current_stock < 0.25 * capacity and rounds_remaining >= 2:
            defect_prob = max(0.0, defect_prob - 0.3)
        if rounds_remaining <= 2 and coop_rate >= 0.4:
            defect_prob = 0.0
        if random.random() < defect_prob:
            return Action.D
        else:
            return Action.C

# claude-haiku-4-5/selfish
class Strategy_OPPORTUNISTIC_107(BaseStrategy):
    """
    Opportunistic Adaptive Strategy: Defect when stock is abundant, cooperate
    when stock is critical. Always defect in the final round.

    Uses stock-to-capacity ratio (ρ) to trigger opportunism:
    - ρ > 0.5: Always defect (abundant regime)
    - 0.2 < ρ ≤ 0.5: Defect with probability (ρ - 0.2) / 0.3 (moderate regime)
    - ρ ≤ 0.2: Always cooperate (critical regime)
    - Final round: Always defect regardless of stock
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description

    def __call__(self, history: PlayerHistory, current_stock: float) -> Action:
        if history.round_number == self.game_description.n_rounds - 1:
            return Action.D
        rho = current_stock / self.game_description.capacity
        if rho > 0.5:
            return Action.D
        if rho > 0.2:
            defection_probability = (rho - 0.2) / 0.3
            if random.random() < defection_probability:
                return Action.D
            else:
                return Action.C
        return Action.C

# gemini-3.1-flash-lite-preview/collective
class Strategy_BENEVOLENT_102(BaseStrategy):
    """
    Triggered Tit-for-Tat with Resource Maintenance.
    Maintains a trust score based on aggregate cooperation history.
    Adapts cooperation probability based on trust, stock levels, and terminal game conditions.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.trust_score = 1.0
        self.alpha = 0.8
        self.cooperation_streak = 0
        self.consecutive_coop_threshold = 3

    def __call__(self, history: PlayerHistory, current_stock: float) -> Action:
        n = self.game_description.n_players
        capacity = self.game_description.capacity
        r = self.game_description.n_rounds
        current_round = history.round_number
        if current_round == r - 1:
            return Action.D
        if current_round == 0:
            self.trust_score = 1.0
            return Action.C
        prev_coop_count = history.opponent_cooperators[-1]
        my_prev_action = history.my_actions[-1]
        my_prev_coop = 1 if my_prev_action else 0
        total_cooperators = prev_coop_count + my_prev_coop
        p_t = total_cooperators / n
        self.trust_score = self.alpha * self.trust_score + (1 - self.alpha) * p_t
        if p_t > 0:
            self.cooperation_streak += 1
        else:
            self.cooperation_streak = 0
            self.trust_score = 0.0
        if current_stock < capacity * 0.2 or current_stock < 0.0001:
            return Action.D
        if self.cooperation_streak >= self.consecutive_coop_threshold and self.trust_score > 0.8:
            return Action.C
        prob_c = max(0.0, min(1.0, self.trust_score))
        if random.random() <= prob_c:
            return Action.C
        else:
            return Action.D

# gemini-3.1-flash-lite-preview/selfish
class Strategy_OPPORTUNISTIC_95(BaseStrategy):
    """
    Calculated Opportunism: Maximizes individual payoff by tracking sustainability.
    Plays C (Cooperate) to build resources when the pool is healthy, but
    shifts to D (Defect) when the stock is critically low or when others
    defect and threaten the resource.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description

    def __call__(self, history: PlayerHistory, current_stock: float) -> Action:
        if history.round_number == 0:
            return Action.C
        if history.round_number == self.game_description.n_rounds - 1:
            return Action.D
        if current_stock < 0.1:
            return Action.D
        n = self.game_description.n_players
        prev_my_action = history.my_actions[-1]
        prev_opp_cooperators = history.opponent_cooperators[-1]
        prev_num_cooperators = prev_opp_cooperators + (1 if prev_my_action else 0)
        prev_num_defectors = n - prev_num_cooperators
        if prev_num_defectors == 0:
            return Action.C
        cons_per_c = current_stock / (2 * n)
        cons_per_d = current_stock / n
        total_consumption = prev_num_cooperators * cons_per_c + prev_num_defectors * cons_per_d
        stock_remaining = max(0.0, current_stock - total_consumption)
        growth = 2 * stock_remaining * (1 - stock_remaining / self.game_description.capacity)
        projected_next_stock = min(stock_remaining + growth, self.game_description.capacity)
        if projected_next_stock < 0.1 * self.game_description.capacity:
            return Action.D
        if random.random() < prev_num_defectors / n:
            return Action.D
        return Action.C

# gpt-5.4-mini/collective
class Strategy_PROSOCIAL_8(BaseStrategy):
    """
    Cooperative default strategy with brief, state-aware defections after
    clear overuse of the common pool.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = int(game_description.n_players)
        self.n_rounds = int(game_description.n_rounds)
        self.capacity = float(game_description.capacity)
        self.n_opponents = max(self.n_players - 1, 1)

    def __call__(self, history: PlayerHistory, current_stock: float) -> Action:
        round_number = int(history.round_number)
        if round_number == 0 or round_number >= self.n_rounds - 1:
            return Action.C
        if self.capacity > 0:
            s = current_stock / self.capacity
        else:
            s = 0.0
        if s < 0.0:
            s = 0.0
        elif s > 1.0:
            s = 1.0
        last_count = int(history.opponent_cooperators[-1]) if len(history.opponent_cooperators) > 0 else 0
        q = last_count / self.n_opponents if self.n_opponents > 0 else 0.0
        if round_number > 1 and len(history.opponent_cooperators) > 1:
            prev_count = int(history.opponent_cooperators[-2])
            q_prev = prev_count / self.n_opponents if self.n_opponents > 0 else 0.0
        else:
            q_prev = None
        if q >= 0.5:
            return Action.C
        if q >= 1.0 / 3.0 and s >= 0.5:
            return Action.C
        if s >= 0.75 and q > 0.0:
            return Action.C
        if s <= 0.25:
            if q < 1.0 / 3.0:
                return Action.D
            return Action.C
        if q < 1.0 / 3.0:
            if s < 0.5:
                if q_prev is None or q_prev < 0.25:
                    return Action.D
        return Action.C

# gpt-5.4-mini/selfish
class Strategy_OPPORTUNISTIC_39(BaseStrategy):
    """
    Adaptive common-pool strategy:
    - cooperate in healthy, sustained-cooperation states
    - defect when the pool is stressed, cooperation is dropping, or in the endgame
    - use a one-shot recovery test after successful post-defection recovery signals
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = int(game_description.n_players)
        self.n_rounds = int(game_description.n_rounds)
        self.capacity = float(game_description.capacity)
        self._high_threshold = self.capacity / 2.0
        self._medium_threshold = self.capacity / 4.0
        self._last_seen_round = -1
        self._last_stock = None
        self._last_action = Action.D
        self._recovery_test_pending = False
        self._recovery_lockout = False

    def __call__(self, history: PlayerHistory, current_stock: float) -> Action:
        round_number = history.round_number
        stock = float(current_stock)
        n_opponents = max(self.n_players - 1, 1)
        if round_number > 0 and len(history.opponent_cooperators) > 0:
            k = int(history.opponent_cooperators[-1])
        else:
            k = 0
        k = max(0, min(k, n_opponents))
        p = k / n_opponents if n_opponents > 0 else 0.0
        opp = history.opponent_cooperators
        last_p = None
        prev_p = None
        if len(opp) >= 1:
            last_p = int(opp[-1]) / n_opponents if n_opponents > 0 else 0.0
        if len(opp) >= 2:
            prev_p = int(opp[-2]) / n_opponents if n_opponents > 0 else 0.0
        last_two_full = False
        if len(opp) >= 2:
            last_two_full = int(opp[-1]) == n_opponents and int(opp[-2]) == n_opponents
        cooperation_not_fallen_two = True
        if len(opp) >= 3:
            a = int(opp[-3])
            b = int(opp[-2])
            c = int(opp[-1])
            cooperation_not_fallen_two = not a > b > c
        very_high_stock = stock >= self.capacity * 0.75
        if round_number >= self.n_rounds - 1:
            self._last_seen_round = round_number
            self._last_stock = stock
            self._last_action = Action.D
            self._recovery_test_pending = False
            self._recovery_lockout = False
            return Action.D
        if round_number == self.n_rounds - 2:
            action = Action.D
            if stock >= self._high_threshold and last_p == 1.0 and (prev_p == 1.0) and very_high_stock:
                action = Action.C
            self._last_seen_round = round_number
            self._last_stock = stock
            self._last_action = action
            self._recovery_test_pending = False
            return action
        if self._recovery_test_pending:
            self._recovery_test_pending = False
            action = Action.C
            self._last_seen_round = round_number
            self._last_stock = stock
            self._last_action = action
            return action
        if self._recovery_lockout:
            if stock >= self._high_threshold and p >= 0.5 and cooperation_not_fallen_two:
                self._recovery_lockout = False
            else:
                self._last_seen_round = round_number
                self._last_stock = stock
                self._last_action = Action.D
                return Action.D
        if round_number == 0:
            action = Action.C if stock >= self._high_threshold else Action.D
            self._last_seen_round = round_number
            self._last_stock = stock
            self._last_action = action
            return action
        if self._last_action == Action.D and self._last_stock is not None:
            if stock > float(self._last_stock) and p == 1.0:
                self._recovery_test_pending = True
                action = Action.C
                self._last_seen_round = round_number
                self._last_stock = stock
                self._last_action = action
                return action
        if stock < self._medium_threshold:
            action = Action.D
        elif stock < self._high_threshold:
            action = Action.D
        elif p < 0.5:
            action = Action.D
        elif p >= 2.0 / 3.0:
            if last_two_full:
                action = Action.C
            else:
                action = Action.D if random.random() < 0.5 else Action.C
        elif cooperation_not_fallen_two:
            action = Action.C
        else:
            action = Action.D
        if stock >= self._high_threshold and p >= 0.5 and (not cooperation_not_fallen_two):
            action = Action.D
        if action == Action.D and self._last_action == Action.C and (self._recovery_test_pending is False):
            if stock < self._high_threshold or p < 1.0:
                self._recovery_lockout = True
        self._last_seen_round = round_number
        self._last_stock = stock
        self._last_action = action
        return action
