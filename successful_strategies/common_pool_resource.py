# n=4
# gemini-2.5-flash[collective][Strategy_COLLECTIVE_332]
class Strategy_EXPLOITATIVE_322(BaseStrategy):
    """
    The "Calculated Exploiter" strategy prioritizes immediate personal gain by defecting,
    while maintaining a vigilant watch over the common resource. It only cooperates when a
    calculated self-interested assessment shows that continued defection will lead to a
    resource collapse so severe it jeopardizes its own future payoffs, and its cooperation
    can meaningfully avert or mitigate this collapse. It adapts by using past observed
    actions of other players to inform its decision-making.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.total_rounds = game_description.n_rounds
        self.capacity = float(game_description.capacity)
        self.ABUNDANT_STOCK_THRESHOLD = 0.75 * self.capacity
        self.CRITICAL_COLLAPSE_THRESHOLD_D_ME = 0.05 * self.capacity
        self.RECOVERABLE_STOCK_THRESHOLD_C_ME = 0.15 * self.capacity
        self.SUBSTANTIAL_DIFFERENCE_THRESHOLD = self.capacity / (2 * self.n_players)

    def _calculate_next_stock(self, current_S: float, total_C: float) -> float:
        """
        Helper function to calculate the new stock level after consumption and growth.
        This function uses the game's stock dynamics rules.
        """
        S_remaining = current_S - total_C
        if S_remaining < 0:
            S_remaining = 0.0
        if self.capacity == 0:
            growth = 0.0
        else:
            growth = 2 * S_remaining * (1 - S_remaining / self.capacity)
        new_stock = min(S_remaining + growth, self.capacity)
        return new_stock

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_round_number = state.round_number
        current_stock = state.current_stock
        if current_round_number == self.total_rounds - 1:
            return Action.D
        if current_round_number == 0:
            return Action.D
        if current_stock >= self.ABUNDANT_STOCK_THRESHOLD:
            return Action.D
        previous_round_index = current_round_number - 1
        opponent_prev_actions = history.opponent_actions[previous_round_index, :]
        num_defectors_others_prev_round = np.sum(~opponent_prev_actions)
        num_cooperators_others_prev_round = np.sum(opponent_prev_actions)
        consumption_by_others = num_defectors_others_prev_round * current_stock / self.n_players + num_cooperators_others_prev_round * current_stock / (2 * self.n_players)
        my_consumption_if_D = current_stock / self.n_players
        total_consumption_if_I_D = consumption_by_others + my_consumption_if_D
        S_next_D_me = self._calculate_next_stock(current_stock, total_consumption_if_I_D)
        my_consumption_if_C = current_stock / (2 * self.n_players)
        total_consumption_if_I_C = consumption_by_others + my_consumption_if_C
        S_next_C_me = self._calculate_next_stock(current_stock, total_consumption_if_I_C)
        condition_1_D_critical = S_next_D_me < self.CRITICAL_COLLAPSE_THRESHOLD_D_ME
        condition_2_C_recoverable = S_next_C_me > self.RECOVERABLE_STOCK_THRESHOLD_C_ME
        condition_3_C_substantial_diff = S_next_C_me > S_next_D_me + self.SUBSTANTIAL_DIFFERENCE_THRESHOLD
        if condition_1_D_critical and condition_2_C_recoverable and condition_3_C_substantial_diff:
            return Action.C
        return Action.D


# gemini-2.5-flash[collective][Strategy_COLLECTIVE_374]
class Strategy_EXPLOITATIVE_374(BaseStrategy):
    """
    Adaptive Predator strategy for the Common Pool Resource game.

    Overall Philosophy:
    The Adaptive Predator aims to maximize cumulative payoff by defaulting to defection
    to exploit cooperators, while strategically cooperating only when necessary
    to prevent resource collapse (to preserve future exploitation opportunities)
    or when such cooperation might induce a more favorable environment. It adapts
    its aggression based on the observed behavior of others and the current health
    of the common pool stock.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.capacity = game_description.capacity
        self.min_stock_threshold = self.capacity / 4.0
        self.num_others_defecting_before_caution = max(1, math.floor((self.n_players - 1) / 3.0))
        self.resource_preservation_min = math.ceil((self.n_players - 1) / 2.0)

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_stock = state.current_stock
        round_number = state.round_number
        n_others = self.n_players - 1
        if round_number == self.n_rounds - 1:
            return Action.D
        if current_stock < self.min_stock_threshold:
            return Action.C
        if round_number == 0:
            return Action.C
        num_defectors_prev_round = np.sum(~history.opponent_actions[-1, :])
        if num_defectors_prev_round == n_others:
            return Action.D
        if num_defectors_prev_round <= self.num_others_defecting_before_caution:
            return Action.D
        if num_defectors_prev_round >= self.resource_preservation_min:
            return Action.C
        return Action.D


# gemini-2.5-flash[collective][Strategy_COLLECTIVE_397]
class Strategy_EXPLOITATIVE_397(BaseStrategy):
    """
    The Opportunist Predator strategy aims to maximize individual payoff by exploiting the common pool
    resource. It prioritizes immediate personal gain through defection, but strategically cooperates
    under specific conditions: in the initial round(s) to establish the resource and observe,
    or when the resource is critically low to prevent its collapse and ensure future exploitation.
    In the final rounds, it abandons long-term considerations to maximize terminal payoffs through defection.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.final_rounds_aggressive_defection: int = 1
        self.stock_critical_low_threshold_factor: float = 0.25
        self.initial_observation_rounds: int = 1

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_round = state.round_number
        total_rounds = self.game_description.n_rounds
        current_stock = state.current_stock
        capacity = self.game_description.capacity
        if current_round >= total_rounds - self.final_rounds_aggressive_defection:
            return Action.D
        if current_stock <= capacity * self.stock_critical_low_threshold_factor:
            return Action.C
        if current_round < self.initial_observation_rounds:
            return Action.C
        return Action.D


# n=64
# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_189]
class Strategy_COLLECTIVE_189(BaseStrategy):
    """
    Adaptive Stewardship Strategy (ASS) for Common Pool Resource Game.
    
    Balances individual payoff maximization with collective resource sustainability.
    Adapts to observed cooperation levels while maintaining commitment to resource preservation.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.capacity = game_description.capacity
        self.consecutive_shrink_rounds = 0
        self.chi_threshold_high = 0.75
        self.chi_threshold_low = 0.4
        self.stock_healthy_threshold = 0.6
        self.stock_critical_threshold = 0.4
        self.stock_collapse_threshold = 0.1
        self.perfect_coop_lock = False
        self.perfect_coop_rounds = 0

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        if state.round_number == self.n_rounds - 1:
            return Action.D
        return self._adaptive_decision(state, history)

    def _adaptive_decision(self, state: CommonPoolState, history: PlayerHistory) -> Action:
        current_stock = state.current_stock
        round_num = state.round_number
        if current_stock < self.capacity * self.stock_collapse_threshold:
            return Action.C
        if self.perfect_coop_lock:
            return Action.C
        prev_round_idx = round_num - 1
        cooperators_prev = np.sum(history.opponent_actions[prev_round_idx, :])
        chi = cooperators_prev / self.n_players
        if chi == 1.0:
            self.perfect_coop_rounds += 1
            if self.perfect_coop_rounds >= 3:
                self.perfect_coop_lock = True
                return Action.C
        else:
            self.perfect_coop_rounds = 0
        if round_num >= 2:
            prev_prev_stock = self._estimate_stock_at_round(history, round_num - 2)
            if prev_prev_stock is not None and prev_prev_stock > current_stock:
                self.consecutive_shrink_rounds += 1
                if self.consecutive_shrink_rounds >= 2:
                    self.chi_threshold_high = 0.5
            else:
                self.consecutive_shrink_rounds = 0
        if chi >= self.chi_threshold_high:
            return Action.C
        elif chi > self.chi_threshold_low:
            if current_stock > self.capacity * self.stock_healthy_threshold:
                return Action.C
            else:
                return Action.D
        elif current_stock > self.capacity * self.stock_critical_threshold:
            return Action.D
        else:
            return Action.C

    def _estimate_stock_at_round(self, history: PlayerHistory, target_round: int) -> float | None:
        """
        Estimate stock level at a given round by reconstructing from initial state.
        Returns None if estimate is not reliable.
        """
        if target_round < 0 or target_round >= len(history.my_actions):
            return None
        stock = float(self.capacity)
        for round_idx in range(target_round + 1):
            my_action = 1 if history.my_actions[round_idx] else 0
            opponent_actions = np.sum(history.opponent_actions[round_idx, :])
            total_cooperators = my_action + opponent_actions
            c_consumption = stock / (2 * self.n_players)
            d_consumption = stock / self.n_players
            total_consumption = total_cooperators * c_consumption + (self.n_players - total_cooperators) * d_consumption
            stock_after = stock - total_consumption
            stock_after = max(0.0, stock_after)
            if stock_after > 0:
                growth = 2 * stock_after * (1 - stock_after / self.capacity)
            else:
                growth = 0.0
            stock = min(stock_after + growth, float(self.capacity))
        return stock


# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_52]
class Strategy_EXPLOITATIVE_52(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Extraction with Depletion Tracking
    
    Treats the common pool as a resource to extract maximum personal value.
    Defaults to defection, cooperating only when mathematical analysis proves
    it yields higher cumulative payoff under worst-case opponent assumptions.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.r = game_description.n_rounds
        self.capacity = game_description.capacity

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_stock = state.current_stock
        round_t = state.round_number
        if current_stock <= 0:
            return Action.D
        if round_t >= 2 * self.r / 3:
            return Action.D
        if current_stock <= self.capacity / 4:
            return Action.D
        remaining_rounds = self.r - round_t
        scenario_a_payoff = self._estimate_payoff(action=True, current_stock=current_stock, remaining_rounds=remaining_rounds)
        scenario_b_payoff = self._estimate_payoff(action=False, current_stock=current_stock, remaining_rounds=remaining_rounds)
        if scenario_b_payoff >= scenario_a_payoff:
            return Action.D
        elif scenario_a_payoff > scenario_b_payoff and current_stock > self.capacity / 4:
            return Action.C
        else:
            return Action.D

    def _estimate_payoff(self, action: bool, current_stock: float, remaining_rounds: int) -> float:
        """
        Estimate total payoff over remaining rounds.
        
        Args:
            action: True for COOPERATE, False for DEFECT
            current_stock: Current pool stock level
            remaining_rounds: Number of rounds left (including this one)
        
        Returns:
            Estimated cumulative payoff over remaining rounds
        """
        total_payoff = 0.0
        stock = current_stock
        for round_idx in range(remaining_rounds):
            if action:
                round_payoff = stock / (2 * self.n)
                my_consumption = stock / (2 * self.n)
            else:
                round_payoff = stock / self.n
                my_consumption = stock / self.n
            total_payoff += round_payoff
            opponent_consumption = (self.n - 1) * (stock / self.n)
            total_consumption = my_consumption + opponent_consumption
            stock = max(0, stock - total_consumption)
            if stock > 0:
                growth = 2 * stock * (1 - stock / self.capacity)
                stock = min(stock + growth, self.capacity)
            action = False
        return total_payoff


# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_129]
class Strategy_EXPLOITATIVE_129(BaseStrategy):
    """
    Exploitative Common Pool Resource Strategy
    
    Operates on the principle of maximizing immediate extraction while exploiting
    cooperators and only cooperating when scarcity forces it to be rational.
    Key tactics: unconditional defection in first and last rounds, adaptive defection
    in middle rounds based on stock level, and aggressive extraction to suppress regrowth.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.capacity = game_description.capacity

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_round = state.round_number
        current_stock = state.current_stock
        if current_round == self.n_rounds - 1:
            return Action.D
        if current_round == 0:
            return Action.D
        scarcity_threshold = self.capacity * 0.5
        if current_stock < 2 * self.n_players:
            return Action.D
        if current_stock > scarcity_threshold:
            return Action.D
        defection_payoff = current_stock / self.n_players
        cooperation_payoff = current_stock / (2 * self.n_players)
        stock_after_all_defect = current_stock - current_stock
        estimated_growth_all_defect = 0.0
        total_coop_consumption = current_stock / 2.0
        stock_after_all_coop = current_stock - total_coop_consumption
        if stock_after_all_coop > 0 and stock_after_all_coop <= self.capacity:
            estimated_growth_all_coop = 2.0 * stock_after_all_coop * (1.0 - stock_after_all_coop / self.capacity)
        else:
            estimated_growth_all_coop = 0.0
        estimated_next_stock_coop = min(stock_after_all_coop + estimated_growth_all_coop, self.capacity)
        remaining_rounds = self.n_rounds - current_round
        if remaining_rounds > 0:
            estimated_future_coop_payoff = estimated_next_stock_coop / (2 * self.n_players) / remaining_rounds
        else:
            estimated_future_coop_payoff = 0.0
        if defection_payoff < cooperation_payoff + estimated_future_coop_payoff:
            return Action.C
        return Action.D
