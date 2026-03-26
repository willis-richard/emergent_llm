# claude-haiku-4-5[collective]
class Strategy_COLLECTIVE_161(BaseStrategy):
    """
    Adaptive Reciprocal Contribution (ARC) Strategy

    A probabilistic strategy that cooperates with probability proportional to
    observed cooperation in the previous round. This balances collective welfare
    maximization with protection against exploitation.

    Decision Rule:
    - Round 1: p_1 = (k-1)/2
    - Round t>1: p_t = (k-1) × (C_{t-1}/n)

    Where C_{t-1} is the number of cooperators in the previous round.
    Cooperate with probability p_t, defect otherwise.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.k = game_description.k

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            p = (self.k - 1) / 2
        else:
            cooperators_last_round = np.sum(history.opponent_actions[-1, :])
            if history.my_actions[-1]:
                cooperators_last_round += 1
            p = (self.k - 1) * (cooperators_last_round / self.n)
        p = max(0, min(1, p))
        if random.random() <= p:
            return Action.C
        else:
            return Action.D


# claude-haiku-4-5[exploitative]
class Strategy_EXPLOITATIVE_487(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Selective Exploitation

    This strategy exploits the fundamental asymmetry in the Public Goods Game by:
    1. Defecting in round 1 to probe for cooperators
    2. Adaptively defecting based on observed cooperation rates vs. a calculated threshold
    3. Intensifying defection in the final 5 rounds
    4. Pure defection in the terminal round

    The strategy uses stochastic defection at low cooperation to hedge against all-defector
    punishment and avoid predictability.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.k = game_description.k

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        round_number = state.round_number
        if round_number == 0:
            return Action.D
        if round_number == self.n_rounds - 1:
            return Action.D
        if round_number >= self.n_rounds - 5:
            rand_val = random.random()
            if rand_val < 0.95:
                return Action.D
            else:
                return Action.C
        cooperators_last_round = int(np.sum(history.opponent_actions[-1, :]))
        cooperation_rate = cooperators_last_round / self.n_players - 1 / self.n_players
        threshold = 1 / self.k - 1 / self.n_players
        net_benefit_of_defection = cooperation_rate * (self.k / self.n_players - 1)
        if cooperation_rate > threshold:
            return Action.D
        else:
            rand_val = random.random()
            if rand_val < 0.85:
                return Action.D
            else:
                return Action.C


# deepseek-r1-distill-llama-70b[collective]
class Strategy_COLLECTIVE_212(BaseStrategy):
    """
    An adaptive strategy for the N-Player Public Goods Game that balances cooperation and defecting based on the number of cooperators in the previous round.
    Cooperates initially and continues if a threshold of cooperators is met; otherwise, mostly defects with a small chance to cooperate.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.k = game_description.k
        self.m = math.ceil(self.n / self.k)

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        t = state.round_number
        prev_my_action = history.my_actions[t - 1]
        opp_coop = history.opponent_actions[t - 1, :].sum()
        sum_prev_coop = int(opp_coop) + (1 if prev_my_action else 0)
        if sum_prev_coop >= self.m:
            return Action.C
        elif random.random() < 0.9:
            return Action.D
        else:
            return Action.C


# deepseek-r1-distill-llama-70b[exploitative]
class Strategy_EXPLOITATIVE_306(BaseStrategy):
    """
    An adaptive strategy that balances exploration and exploitation in an N-player public goods game.
    It starts by cooperating, periodically defects to test outcomes, and adapts based on success.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.k = game_description.k
        self.exploration_prob = 0.2
        self.S = 0
        self.F = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        if history is not None and state.round_number > 0:
            prev_round = state.round_number - 1
            if prev_round < len(history.my_actions):
                prev_action = history.my_actions[prev_round]
                if not prev_action:
                    sum_others_C = np.sum(history.opponent_actions[prev_round, :])
                    defect_payoff = history.my_payoffs[prev_round]
                    coop_payoff = self.k / self.n * (sum_others_C + 1)
                    if defect_payoff > coop_payoff:
                        self.S += 1
                    else:
                        self.F += 1
        if random.random() < self.exploration_prob:
            return Action.D
        elif self.S > self.F:
            return Action.D
        else:
            return Action.C


# gemini-2.5-flash[collective]
class Strategy_COLLECTIVE_100(BaseStrategy):
    """
    The Adaptive Public Goods Strategist (APGS) aims to maximize individual payoff
    by fostering cooperation when possible, punishing free-riding, and adapting
    to game parameters and observed player behavior.

    It initiates cooperation in Round 1. In intermediate rounds (2 to r-1),
    it dynamically decides to cooperate or defect based on a calculated threshold
    (T_coop = ceil(n/k)) against the total number of cooperators in the previous round.
    If collective cooperation meets or exceeds T_coop, the strategy cooperates; otherwise,
    it defects. In the final round (round r), it always defects due to backward induction.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.r = game_description.n_rounds
        self.k = game_description.k
        self.T_coop = math.ceil(self.n / self.k)

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round_1_indexed = state.round_number + 1
        if current_round_1_indexed == 1:
            return Action.C
        elif current_round_1_indexed == self.r:
            return Action.D
        else:
            m_prev = np.sum(history.opponent_actions[-1, :]) + history.my_actions[-1]
            if m_prev >= self.T_coop:
                return Action.C
            else:
                return Action.D


# gemini-2.5-flash[exploitative]
class Strategy_EXPLOITATIVE_242(BaseStrategy):
    """
    The Opportunistic Free-Rider strategy for the N-Player Public Goods Game.

    This strategy aims to maximize individual payoff by strategically inducing
    and then exploiting cooperation from others. It starts with an initial probe
    of cooperation, then adapts its behavior based on observed cooperation levels,
    prioritizing defection when cooperation is sufficiently high or to protect
    its endowment when cooperation is very low. It ruthlessly defects in the
    final rounds.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.r = game_description.n_rounds
        self.n_coop_threshold_low = max(1, math.floor(self.n / 5))
        self.n_coop_threshold_high = max(2, math.floor(self.n / 2))
        self.probe_probability = 0.15
        self.endgame_rounds = 1

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round = state.round_number
        if current_round == 0:
            return Action.C
        if current_round >= self.r - self.endgame_rounds:
            return Action.D
        my_prev_action_was_cooperate = history.my_actions[current_round - 1]
        opponents_prev_cooperators = np.sum(history.opponent_actions[current_round - 1, :])
        N_C_prev = int(my_prev_action_was_cooperate) + opponents_prev_cooperators
        if N_C_prev >= self.n_coop_threshold_high:
            return Action.D
        elif N_C_prev < self.n_coop_threshold_low:
            if random.random() < self.probe_probability:
                return Action.C
            else:
                return Action.D
        else:
            return Action.D


# gpt-5-mini[collective]
class Strategy_COLLECTIVE_494(BaseStrategy):
    """
    Adaptive Collective Conditional Cooperator (AC3)

    Summary:
    - Start by cooperating to signal willingness to form cooperation.
    - Always defect in the final round.
    - For intermediate rounds, compute the fraction f of cooperators in the previous round
      (including self) and compare to an adaptive threshold theta derived from productivity
      (k/n) and remaining horizon.
    - If f >= theta: cooperate if you cooperated last round (win-stay); if you defected last
      round, rejoin with probability recovery_prob.
    - If f < theta: enter a punishment phase (defect) for up to P rounds, but allow small
      exploration probability to probe for recovery. If punishment has exceeded P rounds,
      increase probability of cooperation to restart cooperation.
    - Deterministic except for small randomized probes for recovery/exploration.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = int(game_description.n_players)
        self.r = int(game_description.n_rounds)
        self.k = float(game_description.k)
        productivity_ratio = self.k / max(1.0, self.n)
        if productivity_ratio >= 0.5:
            self.threshold_base = 0.5
        else:
            self.threshold_base = 0.6
        self.P = max(1, math.floor(self.r / 5))
        self.exploration_prob_base = 0.15
        self.recovery_prob = 0.5

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        t = int(state.round_number)
        if t == 0 or history is None:
            return Action.C
        if t == self.r - 1:
            return Action.D
        rem = self.r - t
        theta = self.threshold_base + 0.2 * (1.0 - rem / self.r)
        theta = min(theta, 0.95)

        def cooperators_in_round(idx: int) -> int:
            my = int(bool(history.my_actions[idx]))
            opp_sum = int(np.sum(history.opponent_actions[idx, :])) if history.opponent_actions.size else 0
            return my + opp_sum
        last_idx = t - 1
        c_last = cooperators_in_round(last_idx)
        f = float(c_last) / float(self.n)
        my_last = bool(history.my_actions[last_idx])
        if f >= theta:
            if my_last:
                return Action.C
            else:
                if random.random() < self.recovery_prob:
                    return Action.C
                return Action.D
        consec_bad = 0
        for idx in range(last_idx, -1, -1):
            c_here = cooperators_in_round(idx)
            f_here = float(c_here) / float(self.n)
            if f_here < theta:
                consec_bad += 1
            else:
                break
        if consec_bad <= self.P:
            exploration_prob = self.exploration_prob_base * min(1.0, rem / self.r)
            if random.random() < exploration_prob:
                return Action.C
            return Action.D
        else:
            coop_prob = max(self.exploration_prob_base, 0.25)
            if random.random() < coop_prob:
                return Action.C
            return Action.D


# gpt-5-mini[exploitative]
class Strategy_EXPLOITATIVE_417(BaseStrategy):
    """
    Exploitative, data-driven public goods player.

    Defects by default, probes early with small probability to collect causal evidence,
    and only cooperates when empirical estimates show that cooperating now raises others'
    future cooperation enough to repay the immediate cost. Includes a sustain mode to
    partially cooperate with reciprocators and a permanent defection fallback if
    cooperation provokes fewer future contributions.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = int(game_description.n_players)
        self.r = int(game_description.n_rounds)
        self.k = float(game_description.k)
        self.W = min(10, max(0, self.r - 1))
        self.min_samples = min(6, max(0, self.r - 1))
        if self.r > 0:
            self.p_probe = max(0.05, min(0.25, 5.0 / float(self.r)))
        else:
            self.p_probe = 0.1
        self.p_sustain = 0.5
        self.epsilon = 0.02
        self.mode = 'normal'
        self.consec_above = 0
        self.consec_below = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        t = int(state.round_number)
        if t >= self.r - 1:
            return Action.D
        if history is None or t == 0:
            if random.random() < self.p_probe:
                return Action.C
            return Action.D
        if self.mode == 'permanent_defect':
            return Action.D
        rem_future = self.r - t - 1
        if rem_future <= 0:
            return Action.D
        my_actions = np.array(history.my_actions, dtype=bool)
        opp_actions = np.array(history.opponent_actions, dtype=bool)
        completed_rounds = my_actions.shape[0]
        num_transitions = max(0, completed_rounds - 1)
        window_m = min(self.W, num_transitions)
        if window_m <= 0:
            if random.random() < self.p_probe:
                return Action.C
            return Action.D
        start_s = num_transitions - window_m
        S_C_vals = []
        S_D_vals = []
        for s in range(start_s, start_s + window_m):
            if s + 1 >= opp_actions.shape[0]:
                continue
            frac_others_after = float(np.mean(opp_actions[s + 1, :])) if opp_actions.shape[1] > 0 else 0.0
            if my_actions[s]:
                S_C_vals.append(frac_others_after)
            else:
                S_D_vals.append(frac_others_after)
        sample_count = len(S_C_vals) + len(S_D_vals)
        if sample_count < self.min_samples:
            if random.random() < self.p_probe:
                return Action.C
            return Action.D
        mean_after_C = float(np.mean(S_C_vals)) if len(S_C_vals) > 0 else 0.0
        mean_after_D = float(np.mean(S_D_vals)) if len(S_D_vals) > 0 else 0.0
        delta_est = mean_after_C - mean_after_D
        threshold = (1.0 - self.k / float(self.n)) * float(self.n) / (self.k * float(rem_future))
        if delta_est >= threshold:
            self.consec_above += 1
            self.consec_below = 0
        else:
            if delta_est <= -self.epsilon:
                self.consec_below += 1
            else:
                self.consec_below = 0
            self.consec_above = 0
        if self.consec_above >= 3 and self.mode != 'sustain':
            self.mode = 'sustain'
        if self.consec_below >= 3 and delta_est <= -self.epsilon:
            self.mode = 'permanent_defect'
        if delta_est >= threshold:
            if self.mode == 'sustain':
                if random.random() < self.p_sustain:
                    return Action.C
                return Action.D
            return Action.C
        return Action.D


# llama3.1-70b[collective]
class Strategy_COLLECTIVE_469(BaseStrategy):
    """
    Adaptive Collective Optimism (ACO) strategy for N-Player Public Goods Game.
    
    This strategy adapts to various opponent behaviors and depends solely on game parameters and history.
    It aims to achieve a mutually beneficial outcome for all players involved by balancing individual self-interest with collective optimization.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return random.choice([Action.C, Action.D]) if random.random() < self.game_description.k / self.game_description.n_players else Action.D
        previous_round_payoff = np.mean(history.my_payoffs[-1:])
        if previous_round_payoff >= self.game_description.k:
            p_C = 0.7 + (previous_round_payoff - self.game_description.k) / (self.game_description.n_players * self.game_description.k)
            return Action.C if random.random() < p_C else Action.D
        else:
            return Action.D if random.random() > self.game_description.k / self.game_description.n_players else Action.C


# llama3.1-70b[exploitative]
class Strategy_EXPLOITATIVE_507(BaseStrategy):
    """
    An adaptive exploitative strategy for the N-Player Public Goods Game.
    It gathers information in initial rounds, adapts to opponents' behavior,
    exploits high cooperation rates, and punishes defectors.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.avg_coop_rate = 0.5
        self.punishment_rounds = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C if random.random() < 0.5 else Action.D
        if state.round_number <= 3:
            return Action.C if random.random() < 0.5 else Action.D
        recent_coop_rates = np.mean(history.opponent_actions[-2:, :], axis=0)
        self.avg_coop_rate = np.mean(recent_coop_rates)
        if self.avg_coop_rate > 0.5:
            return Action.D if random.random() < 0.7 else Action.C
        else:
            return Action.C if random.random() < 0.3 else Action.D
        opponent_coop_rates = np.mean(history.opponent_actions, axis=0)
        for i, rate in enumerate(opponent_coop_rates):
            if rate > 0.8:
                return Action.D
            elif history.opponent_actions[-1, i] == False and history.my_payoffs[-1] < self.game_description.k / self.game_description.n_players:
                self.punishment_rounds = 2
                break
        if self.punishment_rounds > 0:
            self.punishment_rounds -= 1
            return Action.D
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D


# mistral-7b[collective]
class Strategy_COLLECTIVE_345(BaseStrategy):
    """Adaptive Tit-for-Tat with Probability of Cooperation (ATFTP)"""

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.p_high = 0.8
        self.p_low = 0.5
        self.round_number = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if history is None:
            self.round_number += 1
            return Action.C
        else:
            self.round_number = state.round_number
            if history.opponent_actions[-1].all():
                p = self.p_high
            else:
                p = self.p_low
            random_choice = random.random()
            if random_choice < p:
                action = Action.C
            else:
                action = Action.D
        if self.round_number == self.game_description.n_rounds:
            action = Action.C
        return action


# mistral-7b[exploitative]
class Strategy_EXPLOITATIVE_593(BaseStrategy):
    """
    Tit-for-Tat with Adaptive Cooperation Rate (TFT-ACR) strategy for N-Player Public Goods Game.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.cooperation_rate = random.uniform(0, 1)
        self.a = 0.05
        self.b = 0.02

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C if random.random() <= self.cooperation_rate else Action.D
        cooperators = np.sum(history.opponent_actions[-1])
        self.cooperation_rate += (self.a - self.b) * (2 * cooperators / self.game_description.n_players - 1)
        self.cooperation_rate = max(min(self.cooperation_rate, 1), 0)
        return Action.C if random.random() <= self.cooperation_rate else Action.D
