# claude-haiku-4-5[collective]
class Strategy_COLLECTIVE_359(BaseStrategy):
    """
    Adaptive Stewardship with Defensive Stabilization strategy for Common Pool Resource Game.
    
    This strategy prioritizes long-term collective payoff by conditioning cooperation on stock health.
    It cooperates when stock is abundant, probabilistically adapts in the middle range, and defects
    when stock is critically depleted. End-game adjustments slightly increase defection bias to
    account for reduced future value of stock.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.capacity = game_description.capacity
        self.n_rounds = game_description.n_rounds
        self.threshold_high = 0.75 * self.capacity
        self.threshold_low = 0.2 * self.capacity

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        stock_level = state.current_stock
        round_number = state.round_number
        if stock_level >= self.capacity:
            return Action.C
        if stock_level <= 0:
            return Action.D
        rounds_remaining = self.n_rounds - round_number
        normalized_progress = round_number / self.n_rounds if self.n_rounds > 0 else 0
        end_game_factor = 1.0 - 0.15 * normalized_progress
        if stock_level > self.threshold_high:
            cooperation_prob = 1.0
        elif stock_level < self.threshold_low:
            cooperation_prob = 0.0
        else:
            cooperation_prob = (stock_level - self.threshold_low) / (self.threshold_high - self.threshold_low)
        cooperation_prob = cooperation_prob * end_game_factor
        if history is not None and round_number > 0:
            last_round_actions = history.opponent_actions[-1, :]
            defection_count = np.sum(~last_round_actions)
            defection_rate = defection_count / len(last_round_actions) if len(last_round_actions) > 0 else 0
            if defection_rate > 0.5:
                cooperation_prob = cooperation_prob * 0.8
        cooperation_prob = max(0.0, min(1.0, cooperation_prob))
        if random.random() < cooperation_prob:
            return Action.C
        else:
            return Action.D


# claude-haiku-4-5[exploitative]
class Strategy_EXPLOITATIVE_229(BaseStrategy):
    """
    Exploitative strategy using dynamic defection with adaptive thresholds.
    Maximizes individual payoff by exploiting cooperative players while adapting
    to pool degradation through stock-level sensing and round-dependent adjustments.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.depletion_threshold = game_description.capacity * 0.4
        self.defection_rate = 0.7

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.D
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D
        rounds_remaining = self.game_description.n_rounds - state.round_number
        if state.current_stock > self.depletion_threshold:
            base_rate = state.current_stock / self.game_description.capacity * 0.9 + 0.3
        else:
            base_rate = 0.5
        if rounds_remaining <= self.game_description.n_rounds / 3:
            defection_rate = min(0.95, base_rate * 1.3)
        else:
            defection_rate = base_rate
        if state.round_number >= 1:
            previous_stock = history.my_payoffs[state.round_number - 1] * self.game_description.n_players
            if previous_stock > 0:
                stock_change_ratio = (state.current_stock - previous_stock) / previous_stock
                if stock_change_ratio > 0.1:
                    defection_rate = min(0.95, defection_rate + 0.05)
                elif stock_change_ratio < -0.3:
                    defection_rate = max(0.3, defection_rate - 0.1)
        if state.current_stock < self.game_description.n_players * 2 * 0.1:
            defection_rate = max(0.5, defection_rate)
        if random.random() < defection_rate:
            return Action.D
        else:
            return Action.C


# deepseek-r1-distill-llama-70b[collective]
class Strategy_COLLECTIVE_108(BaseStrategy):
    """
    Adaptive Cooperation with Forgiveness strategy balances immediate gains with long-term sustainability
    by using dynamic thresholds, reciprocity, and sustainability checks to decide actions.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.stock_history = []
        self.n_opponents = game_description.n_players - 1
        self.capacity = game_description.capacity
        self.K = 3

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            self.stock_history.append(state.current_stock)
            return Action.C
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D
        self.stock_history.append(state.current_stock)
        current_stock = state.current_stock
        p_sustainability = 1 - current_stock / (2 * self.capacity)
        p_sustainability = max(0, min(1, p_sustainability))
        if len(self.stock_history) >= 2:
            previous_stock = self.stock_history[-2]
            current_stock_before = self.stock_history[-1]
            delta = current_stock_before - previous_stock
            max_delta = 0.5 * self.capacity
            trend = delta / max_delta
            trend_factor = 0.5 + trend * 0.5
            trend_factor = max(0, min(1, trend_factor))
        else:
            trend_factor = 0.5
        p_sustainability *= (1 + trend_factor) / 2
        p_sustainability = max(0, min(1, p_sustainability))
        sum_coop = 0
        if history is not None and len(history.opponent_actions) >= 1:
            for i in range(1, self.K + 1):
                round_idx = state.round_number - i
                if round_idx < 0:
                    break
                opp_actions = history.opponent_actions[round_idx]
                sum_coop += sum(opp_actions)
            avg_coop_prop = sum_coop / (self.K * self.n_opponents) if self.K * self.n_opponents != 0 else 0
        else:
            avg_coop_prop = 0
        p_reciprocity = avg_coop_prop
        p_total = p_sustainability * p_reciprocity
        p_total = max(0, min(1, p_total))
        if random.random() < p_total:
            return Action.C
        else:
            return Action.D


# deepseek-r1-distill-llama-70b[exploitative]
class Strategy_EXPLOITATIVE_465(BaseStrategy):
    """
    A strategy for the Common Pool Resource Game that balances immediate payoff maximization with long-term sustainability.
    It uses a combination of conservation thresholds, cooperation incentives, and probabilistic decisions based on historical behavior.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description

    def __call__(self, state: CommonPoolState, history: PlayerHistory | None) -> Action:
        if state.round_number == 0:
            return Action.C
        elif state.round_number == self.game_description.n_rounds - 1:
            return Action.D
        else:
            current_round = state.round_number
            n_players = self.game_description.n_players
            capacity = self.game_description.capacity
            current_stock = state.current_stock
            total_C = 0
            for round in range(current_round):
                if history.my_actions[round]:
                    total_C += 1
                for opponent in range(n_players - 1):
                    if history.opponent_actions[round, opponent]:
                        total_C += 1
            total_possible = n_players * current_round
            avg_coop = total_C / total_possible if total_possible != 0 else 0.0
            if current_stock <= 0.5 * capacity:
                action = Action.C
            elif avg_coop >= 0.5:
                action = Action.C
            else:
                action = Action.D
            defectors = set()
            for opponent in range(n_players - 1):
                coop_count = 0
                for round in range(current_round):
                    if history.opponent_actions[round, opponent]:
                        coop_count += 1
                coop_rate = coop_count / current_round
                if coop_rate < 0.3:
                    defectors.add(opponent)
            if len(defectors) > 0 and avg_coop < 0.5:
                action = Action.D
            cooperation_prob = max(0.2, min(avg_coop, 1.0))
            if random.random() < cooperation_prob:
                action = Action.C
            else:
                action = Action.D
            return action


# gemini-2.5-flash[collective]
class Strategy_COLLECTIVE_118(BaseStrategy):
    """
    Adaptive Stock-Preserving Cooperator (ASPC) strategy.
    This strategy balances resource sustainability with individual performance.
    It starts cooperatively, enforces conservation via stock thresholds, and
    dynamically adjusts to defection based on group size and number of defectors.
    It's more forgiving in larger groups but employs a stricter Tit-for-Tat in two-player games.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.capacity = game_description.capacity
        self.S_threshold_danger = self.capacity / 4.0

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_round_number = state.round_number
        current_stock = state.current_stock
        if current_round_number == 0:
            return Action.C
        if current_round_number == self.n_rounds - 1:
            return Action.D
        if current_stock < self.S_threshold_danger:
            return Action.C
        else:
            prev_round_idx = current_round_number - 1
            my_action_prev = history.my_actions[prev_round_idx]
            opponent_actions_prev = history.opponent_actions[prev_round_idx]
            total_cooperators_prev = np.sum(opponent_actions_prev) + (1 if my_action_prev else 0)
            num_defectors_prev_round = self.n_players - total_cooperators_prev
            if self.n_players == 2:
                if num_defectors_prev_round == 0:
                    return Action.C
                else:
                    return Action.D
            elif num_defectors_prev_round == 0:
                return Action.C
            elif num_defectors_prev_round == 1:
                return Action.C
            else:
                return Action.D


# gemini-2.5-flash[exploitative]
class Strategy_EXPLOITATIVE_234(BaseStrategy):
    """
    The "Adaptive Resource Predator" strategy is designed to maximize its own total payoff.
    It primarily defects to gain higher immediate rewards, while adaptively cooperating
    only when necessary to prevent resource collapse that would significantly harm its
    own future payoffs. It strategically leverages the cooperation of other players.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.r = game_description.n_rounds
        self.capacity = game_description.capacity

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        current_round_1_indexed = state.round_number + 1
        current_stock = state.current_stock
        if state.round_number == 0:
            return Action.D
        if current_round_1_indexed == self.r:
            return Action.D
        stock_ratio = current_stock / self.capacity
        previous_round_opponent_actions = history.opponent_actions[state.round_number - 1, :]
        num_C_opponents_prev_round = int(np.sum(previous_round_opponent_actions))
        is_others_cooperating_sufficiently = num_C_opponents_prev_round >= (self.n - 1) // 2 + 1
        if stock_ratio < 0.15:
            if is_others_cooperating_sufficiently:
                return Action.C
            else:
                return Action.D
        elif stock_ratio < 0.4:
            if is_others_cooperating_sufficiently:
                return Action.D
            else:
                remaining_rounds = self.r - current_round_1_indexed
                if remaining_rounds >= self.r / 2:
                    return Action.C
                else:
                    return Action.D
        else:
            return Action.D


# gpt-5-mini[collective]
class Strategy_COLLECTIVE_300(BaseStrategy):
    """
    Adaptive Fare-Share with Forgiving Trigger (AFFT).

    - Starts cooperatively, defects in the final round.
    - Monitors recent group cooperation (window m) and cooperates if group is sufficiently cooperative.
    - If the group is not cooperative, initiates a proportional, temporary punishment whose length
      scales with the fraction of defectors in the immediately previous round (up to K).
    - After a punishment window ends, attempts probabilistic forgiveness on the first post-punishment
      round; if forgiveness fails, extends punishment by one round and then re-evaluates.
    - Includes a safety rule for very low stock: cooperate when group is cooperative, defect when
      group is non-cooperative and stock is nearly exhausted.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n_players = int(game_description.n_players)
        self.n_rounds = int(game_description.n_rounds)
        self.capacity = float(game_description.capacity)
        self.m = 3
        self.theta = 0.7
        self.K = 3
        self.p_forgive = 0.2
        self.punish_until_round = -1
        self.last_punished_round_end = -1

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        t = int(state.round_number)
        opponents = max(0, self.n_players - 1)
        if t == 0 or history is None:
            return Action.C
        if t == self.n_rounds - 1:
            return Action.D
        if self.punish_until_round >= 0 and t <= self.punish_until_round:
            return Action.D
        if self.last_punished_round_end >= 0 and t == self.last_punished_round_end + 1:
            if random.random() < self.p_forgive:
                self.last_punished_round_end = -1
                return Action.C
            else:
                self.punish_until_round = t
                self.last_punished_round_end = t
                return Action.D
        lookback = min(self.m, t)
        coop_rate = 0.0
        try:
            recent_slice = history.opponent_actions[t - lookback:t, :]
            if opponents <= 0:
                coop_rate = 1.0
            else:
                coop_rate = float(np.mean(recent_slice.astype(float)))
        except Exception:
            coop_rate = 0.0
        low_stock_threshold = max(1e-08, 0.01 * self.capacity)
        stock_low = state.current_stock <= low_stock_threshold
        if coop_rate >= self.theta:
            return Action.C
        try:
            last_round_actions = history.opponent_actions[t - 1, :]
            coop_last = int(np.sum(last_round_actions.astype(int)))
            d_last = opponents - coop_last
        except Exception:
            d_last = opponents
        if d_last <= 0:
            return Action.C
        if stock_low and coop_rate < self.theta:
            return Action.D
        max_allowed_length = max(1, self.n_rounds - 1 - t)
        proportion = d_last / max(1, opponents)
        punishment_length = int(math.ceil(proportion * self.K))
        punishment_length = max(1, min(punishment_length, max_allowed_length))
        self.punish_until_round = t + punishment_length - 1
        self.last_punished_round_end = self.punish_until_round
        return Action.D


# gpt-5-mini[exploitative]
class Strategy_EXPLOITATIVE_205(BaseStrategy):
    """
    Exploitative-but-safe common-pool strategy.

    - Starts by cooperating to identify cooperators.
    - Maintains per-opponent recent cooperation rates over a short window.
    - Exploits identified cooperators by defecting with high probability,
      but only when expected immediate post-consumption stock stays above a safety threshold.
    - Uses short punishments if exploited after cooperating, but forgives quickly if cooperators reappear.
    - Switches to greedy defection if few cooperators remain.
    - Always defects in the final round and biases toward defection in a short endgame window.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.n = float(game_description.n_players)
        self.n_int = int(game_description.n_players)
        self.r = int(game_description.n_rounds)
        self.capacity = float(game_description.capacity)
        self.w = min(5, max(1, self.r - 1))
        self.coop_threshold = 0.7
        self.p_exploit = 0.9
        self.p_punish = 0.6
        self.L_punish = 2
        self.S_safe = max(0.0, self.capacity / 3.0)
        self.endgame_len = min(3, max(1, self.r - 1))
        self.S_min = 0.0
        self.punish_timer = 0
        self._forgive_avg_threshold = 0.85

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        t = int(state.round_number)
        S = float(state.current_stock)
        if S < 0.0:
            S = 0.0
        last_idx = t - 1
        if t == 0 or history is None:
            return Action.C
        opp_actions = history.opponent_actions
        my_actions = history.my_actions
        n_opp = max(0, opp_actions.shape[1]) if opp_actions.size != 0 else max(0, self.n_int - 1)
        window = min(self.w, t)
        coop_rates = [0.0] * n_opp
        if window > 0 and opp_actions.size != 0:
            recent_slice = opp_actions[-window:, :]
            means = np.mean(recent_slice.astype(float), axis=0)
            for j in range(n_opp):
                coop_rates[j] = float(means[j])
        else:
            coop_rates = [0.0] * n_opp
        E_coop = float(sum(coop_rates))
        exploitable_count = sum((1 for q in coop_rates if q >= self.coop_threshold))
        if t == self.r - 1:
            return Action.D
        if t >= self.r - self.endgame_len:
            if random.random() < self.p_exploit:
                return Action.D
            else:
                return Action.C
        if self.punish_timer > 0:
            avg_coop = E_coop / max(1.0, float(n_opp)) if n_opp > 0 else 0.0
            if avg_coop >= self._forgive_avg_threshold:
                self.punish_timer = 0
            else:
                self.punish_timer = max(0, self.punish_timer - 1)
                return Action.D
        if last_idx >= 0:
            my_last = bool(my_actions[last_idx]) if my_actions.size != 0 else False
            others_last = opp_actions[last_idx, :] if opp_actions.size != 0 else np.array([], dtype=bool)
            if my_last and others_last.size > 0 and (not np.all(others_last)):
                self.punish_timer = self.L_punish
                self.punish_timer = max(0, self.punish_timer - 1)
                return Action.D
        denom_n = max(1.0, self.n)
        denom_2n = max(1.0, 2.0 * self.n)
        expected_consumption_others = 0.0
        cons_C_each = S / denom_2n
        cons_D_each = S / denom_n
        for q in coop_rates:
            expected_consumption_others += float(q) * cons_C_each + (1.0 - float(q)) * cons_D_each
        my_cons_if_defect = cons_D_each
        expected_total_consumption_defect = my_cons_if_defect + expected_consumption_others
        S_after_defect = S - expected_total_consumption_defect
        if S_after_defect < self.S_min:
            S_after_defect = self.S_min
        g = 2.0 * S_after_defect * (1.0 - S_after_defect / max(1.0, self.capacity))
        expected_next_stock_defect = min(S_after_defect + g, self.capacity)
        if exploitable_count >= 1 and S_after_defect >= self.S_safe:
            if random.random() < self.p_exploit:
                return Action.D
            else:
                return Action.C
        if E_coop <= float(self.n_int - 1) / 4.0:
            return Action.D
        everyone_coop_last = False
        if last_idx >= 0:
            my_last_val = bool(my_actions[last_idx]) if my_actions.size != 0 else False
            opps_last_all = bool(np.all(opp_actions[last_idx, :])) if opp_actions.size != 0 else False
            everyone_coop_last = my_last_val and opps_last_all
        if everyone_coop_last:
            return Action.C
        elif random.random() < self.p_punish:
            return Action.D
        else:
            return Action.C


# llama3.1-70b[collective]
class Strategy_COLLECTIVE_393(BaseStrategy):
    """
    Adaptive Stock Conservation (ASC) strategy: 
    Balance collective sustainability with individual gains in the Common Pool Resource Game.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C if random.random() < 0.5 else Action.D
        if history is not None and history.my_actions.size > 0 and (sum(history.opponent_actions[0, :]) == 0):
            cautious_mode = True
        else:
            cautious_mode = False
        if state.round_number == 1:
            previous_stock = self.game_description.capacity
        else:
            previous_stock = history.my_payoffs[-2] * 2 * self.game_description.n_players + history.opponent_payoffs[-2, :].sum() * self.game_description.n_players
        stock_diff = state.current_stock - previous_stock
        if stock_diff >= 0 and state.current_stock > self.game_description.capacity / 2:
            prob_cooperate = 0.7 if not cautious_mode else 0.4
            return Action.C if random.random() < prob_cooperate else Action.D
        elif state.current_stock < self.game_description.capacity / 3:
            prob_defect = 0.8
            return Action.D if random.random() < prob_defect else Action.C
        else:
            return Action.C if random.random() < 0.5 else Action.D
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D


# llama3.1-70b[exploitative]
class Strategy_EXPLOITATIVE_115(BaseStrategy):
    """
    The Adaptive Stock Raider strategy, an exploitative approach to maximize payoffs in a Common Pool Resource Game.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.opponents_behaviors = []
        self.my_payoffs = []

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        n = self.game_description.n_players
        capacity = self.game_description.capacity
        t = state.round_number
        if t == 0 or t <= n:
            return random.choice([Action.C, Action.D])
        stock = state.current_stock
        prev_round_payoffs = history.my_payoffs if len(history.my_payoffs) > 0 else [0]
        if len(self.opponents_behaviors) == 0:
            self.opponents_behaviors.append([bool(action) for action in history.opponent_actions[-1]])
        opponents_behaviors = np.array(self.opponents_behaviors)
        prev_round_opponent_actions = history.opponent_actions[-1] if len(history.opponent_actions) > 0 else [False]
        self.my_payoffs.append(prev_round_payoffs[-1])
        if stock > capacity / 2:
            for i, opponent_action in enumerate(prev_round_opponent_actions):
                if not opponent_action and prev_round_payoffs[i] > prev_round_payoffs[-1]:
                    return Action.D
            if len(self.opponents_behaviors) > 0:
                last_opponent_behavior = np.array([behavior[-1] for behavior in self.opponents_behaviors])
                if sum(last_opponent_behavior == False) >= n // 2 or any((np.all(opp_behavior[:-1]) and (not opp_behavior[-1]) for opp_behavior in opponents_behaviors)):
                    return Action.D
            return Action.C
        else:
            return Action.C
        if t >= self.game_description.n_rounds - n:
            return Action.D


# mistral-7b[collective]
class Strategy_COLLECTIVE_484(BaseStrategy):
    """
    Strategy name: Tit-for-Tat with Adaptive Cooperation Threshold (TFT-ACT)
    This strategy follows a forgiving approach, cooperating in the first round and adapting cooperation rate based on opponents' behavior.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.cooperation_threshold = 0.5
        self.average_opponent_cooperation = 0

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        if history is not None:
            self.average_opponent_cooperation = np.mean(history.opponent_actions[:, :state.round_number])
            if history.my_actions[-1] == Action.C and self.average_opponent_cooperation >= self.cooperation_threshold:
                self.cooperation_threshold *= 0.95
            elif history.my_actions[-1] != Action.C and self.average_opponent_cooperation < self.cooperation_threshold:
                self.cooperation_threshold *= 1.05
        return Action.C if self.cooperation_threshold >= random.random() else Action.D


# mistral-7b[exploitative]
class Strategy_EXPLOITATIVE_404(BaseStrategy):
    """
    Strategy Name: Tit-for-Tat with Adaptive Cooperation Threshold (TFT-ACT)
    Summary: A strategy that cooperates or defects based on the current stock level and the average cooperation rate of previous rounds.
    """

    def __init__(self, game_description: CommonPoolDescription):
        self.game_description = game_description
        self.p = random.uniform(0, 1)
        self.T = 20

    def __call__(self, state: CommonPoolState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0 or state.round_number == self.game_description.n_rounds:
            return Action.C if random.random() < self.p else Action.D
        if history is not None and len(history.opponent_actions) > self.T:
            R_t = np.mean(history.my_actions[-self.T:])
            S_t = calculate_threshold(history, self.T)
            return Action.C if R_t > self.p and state.current_stock >= S_t else Action.D
        else:
            return Action.C if random.random() < self.p else Action.D
