# claude-haiku-4-5[collective]
class Strategy_COLLECTIVE_438(BaseStrategy):
    """
    Adaptive Threshold Cooperation (ATC) strategy for Collective Risk Dilemma.
    
    Balances individual rationality with collective welfare by:
    1. Recognizing the alignment problem between individual and collective interests
    2. Building conditional trust based on observed success rates
    3. Gracefully degrading cooperation only when evidence of failure accumulates
    4. Adapting cooperation probability based on whether threshold was historically met
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.successful_rounds = 0
        self.rounds_played = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            if random.random() < 0.65:
                return Action.C
            else:
                return Action.D
        self.successful_rounds = 0
        self.rounds_played = 0
        for round_idx in range(state.round_number):
            my_action = history.my_actions[round_idx]
            opponent_cooperators = np.sum(history.opponent_actions[round_idx, :])
            total_cooperators = int(my_action) + opponent_cooperators
            if total_cooperators >= self.game_description.m:
                self.successful_rounds += 1
            self.rounds_played += 1
        if self.rounds_played > 0:
            success_rate = self.successful_rounds / self.rounds_played
        else:
            success_rate = 0.5
        if success_rate >= 0.6:
            p_coop = 0.85
        elif success_rate >= 0.3:
            p_coop = 0.6
        else:
            p_coop = 0.4
        if state.round_number == self.game_description.n_rounds - 1:
            if success_rate >= 0.5:
                p_coop = 0.7
            else:
                p_coop = 0.3
        if random.random() < p_coop:
            return Action.C
        else:
            return Action.D


# claude-haiku-4-5[exploitative]
class Strategy_EXPLOITATIVE_66(BaseStrategy):
    """
    Adaptive Threshold Stalker: An exploitative strategy that systematically free-rides
    on others' cooperation while maintaining minimal credibility through stochastic noise.
    
    Core mechanics:
    - Round 1: Always defect (no history to exploit)
    - Threshold met (≥m cooperators): Defect (free-ride on +k without cost)
    - Marginal position (m-1 cooperators): Defect with probability 1-1/n, cooperate with 1/n
    - Below threshold: Defect (no payoff benefit from cooperation)
    - Final round: Always defect (no future reputation effects)
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.m_threshold = game_description.m
        self.k = game_description.k
        self.p_threshold = 1.0 / self.n_players if self.n_players > 0 else 0.0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round = state.round_number
        if current_round == 0:
            return Action.D
        last_round_idx = current_round - 1
        coop_count_last = int(sum(history.opponent_actions[last_round_idx, :]))
        if current_round == self.n_rounds - 1:
            return Action.D
        if coop_count_last >= self.m_threshold:
            return Action.D
        elif coop_count_last == self.m_threshold - 1:
            if random.random() < self.p_threshold:
                return Action.C
            else:
                return Action.D
        else:
            return Action.D


# deepseek-r1-distill-llama-70b[collective]
class Strategy_COLLECTIVE_370(BaseStrategy):
    """
    A strategy for the Collective Risk Dilemma game that promotes sustained cooperation through adaptive decisions.
    Players initially cooperate to establish trust. In subsequent rounds, cooperation continues if the threshold is met;
    otherwise, a deterministic method based on player IDs ensures a fair distribution of cooperative efforts.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.id = random.randint(1, game_description.n_players)

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        prev_round = state.round_number - 1
        c_prev = 0
        if history.my_actions[prev_round]:
            c_prev += 1
        c_prev += history.opponent_actions[prev_round].sum()
        n = self.game_description.n_players
        m = self.game_description.m
        if c_prev >= m:
            return Action.C
        else:
            s = n - c_prev + 1
            target = m - c_prev
            if self.id % s < target:
                return Action.C
            else:
                return Action.D


# deepseek-r1-distill-llama-70b[exploitative]
class Strategy_EXPLOITATIVE_306(BaseStrategy):
    """
    An adaptive strategy for the Collective Risk Dilemma game. It starts by cooperating,
    periodically defects to explore outcomes, and adapts based on the success of previous defections.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.S = 0
        self.F = 0
        self.exploration_prob = 0.2

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        if history is not None and len(history.my_actions) > 0:
            previous_round = len(history.my_actions) - 1
            my_prev_action = history.my_actions[previous_round]
            if my_prev_action == False:
                opponent_actions_prev = history.opponent_actions[previous_round, :]
                sum_coop = np.sum(opponent_actions_prev)
                if sum_coop >= self.game_description.m:
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
class Strategy_COLLECTIVE_168(BaseStrategy):
    """
    Adaptive Collective Responder (ACR) strategy for the Collective Risk Dilemma.
    It initiates cooperation, rewards collective success, shows resilience to near-failures,
    and self-protects against exploitation and widespread failure. Defects in the final round.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.last_action: Action | None = None
        self.consecutive_failures_as_c: int = 0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round_1_indexed = state.round_number + 1
        total_rounds = self.game_description.n_rounds
        m = self.game_description.m
        if state.round_number > 0:
            my_last_action_was_c = self.last_action == Action.C
            N_C_prev = np.sum(history.opponent_actions[-1, :]) + (1 if my_last_action_was_c else 0)
            if my_last_action_was_c and N_C_prev < m:
                self.consecutive_failures_as_c += 1
            else:
                self.consecutive_failures_as_c = 0
        else:
            self.consecutive_failures_as_c = 0
            self.last_action = None
        my_current_action: Action
        if current_round_1_indexed == total_rounds:
            my_current_action = Action.D
        elif current_round_1_indexed == 1:
            my_current_action = Action.C
        elif N_C_prev >= m:
            my_current_action = Action.C
        else:
            MAX_CONSECUTIVE_FAILURES_AS_C = 1
            if self.last_action == Action.C and self.consecutive_failures_as_c >= MAX_CONSECUTIVE_FAILURES_AS_C:
                my_current_action = Action.D
            else:
                HOPE_THRESHOLD = m - 1
                if N_C_prev >= HOPE_THRESHOLD:
                    my_current_action = Action.C
                else:
                    my_current_action = Action.D
        self.last_action = my_current_action
        return my_current_action


# gemini-2.5-flash[exploitative]
class Strategy_EXPLOITATIVE_447(BaseStrategy):
    """
    The Opportunistic Catalyst strategy defaults to defecting (free-riding) to maximize individual gain.
    It only acts as a temporary "catalyst" for cooperation when the collective project is on the
    verge of failure, but only under conditions where its cooperation is likely to be directly
    effective. Once the project is back on track, it immediately reverts to exploitation.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.rounds_of_committed_cooperation_remaining = 0
        self.consecutive_round_failures = 0
        self.FIX_COOPERATION_DURATION = 2
        self.FAILURE_STREAK_THRESHOLD = 1
        self.COOPERATION_IMPACT_WINDOW = 1

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round_num = state.round_number
        total_rounds = self.game_description.n_rounds
        min_cooperators_m = self.game_description.m
        if current_round_num == total_rounds - 1:
            return Action.D
        if current_round_num == 0:
            return Action.D
        num_cooperators_t_minus_1 = np.sum(history.opponent_actions[-1, :])
        total_cooperators_t_minus_1 = num_cooperators_t_minus_1 + (1 if history.my_actions[-1] else 0)
        if total_cooperators_t_minus_1 >= min_cooperators_m:
            self.consecutive_round_failures = 0
            self.rounds_of_committed_cooperation_remaining = 0
        else:
            self.consecutive_round_failures += 1
            if self.rounds_of_committed_cooperation_remaining > 0:
                self.rounds_of_committed_cooperation_remaining -= 1
            else:
                cooperators_needed = min_cooperators_m - total_cooperators_t_minus_1
                if self.consecutive_round_failures >= self.FAILURE_STREAK_THRESHOLD and cooperators_needed <= self.COOPERATION_IMPACT_WINDOW:
                    self.rounds_of_committed_cooperation_remaining = self.FIX_COOPERATION_DURATION
        if self.rounds_of_committed_cooperation_remaining > 0:
            return Action.C
        else:
            return Action.D


# gpt-5-mini[collective]
class Strategy_COLLECTIVE_152(BaseStrategy):
    """
    Bayesian Pivotal Conditional Cooperator (BPCC)

    - Treats each opponent as an independent Bernoulli cooperator with a recency-smoothed
      estimated probability p_j.
    - Computes how pivotal this agent's cooperation is (P_with - P_without) via a Bernoulli-sum DP.
    - Chooses C/D by comparing private expected payoffs plus a small collective tilt (gamma * externality),
      with anti-exploitation and exploration guards, special first/last-round behavior, and tie-breaking.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.alpha = 1.0
        self.base_gamma = 0.25
        self.max_recency = 5
        self.epsilon = max(0.01, 1.0 / max(1, self.game_description.n_rounds))
        self.sacrifice_threshold = max(0.2, 0.05 * max(1.0, self.game_description.k))
        self.tol = 1e-08

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        n = int(self.game_description.n_players)
        r = int(self.game_description.n_rounds)
        m = int(self.game_description.m)
        k = float(self.game_description.k)
        t = int(state.round_number) + 1
        if state.round_number == 0 or history is None:
            p_seed = 0.6 * (m / max(1, n)) + 0.2
            if p_seed < 0.2:
                p_seed = 0.2
            elif p_seed > 0.9:
                p_seed = 0.9
            if random.random() < p_seed:
                return Action.C
            return Action.D
        if random.random() < self.epsilon:
            return Action.C
        opp_count = max(0, history.opponent_actions.shape[1])
        trials = max(0, state.round_number)
        w = min(self.max_recency, trials) if trials > 0 else 0
        p_list = []
        if trials == 0 or w == 0:
            p_list = [0.5] * opp_count
        else:
            denom = self.alpha + float(w)
            recent = history.opponent_actions[-w:, :]
            recent_arr = np.array(recent, dtype=float)
            coop_counts = np.sum(recent_arr, axis=0) if opp_count > 0 else np.array([])
            for j in range(opp_count):
                num = float(self.alpha) + float(coop_counts[j])
                p_j = num / denom if denom > 0.0 else 0.5
                if p_j <= 0.0:
                    p_j = 1e-06
                elif p_j >= 1.0:
                    p_j = 1.0 - 1e-06
                p_list.append(p_j)
        pmf = [0.0] * (opp_count + 1)
        pmf[0] = 1.0
        for p in p_list:
            new_pmf = [0.0] * (opp_count + 1)
            for x in range(0, opp_count + 1):
                if pmf[x] == 0.0:
                    continue
                new_pmf[x] += pmf[x] * (1.0 - p)
                if x + 1 <= opp_count:
                    new_pmf[x + 1] += pmf[x] * p
            pmf = new_pmf

        def tail_prob(thresh: int) -> float:
            if thresh <= 0:
                return 1.0
            if thresh > opp_count:
                return 0.0
            s = 0.0
            for x in range(thresh, opp_count + 1):
                s += pmf[x]
            return max(0.0, min(1.0, s))
        P_without = tail_prob(m)
        P_with = tail_prob(m - 1)
        E_C = -1.0 + k * P_with
        E_D = 1.0 + k * P_without
        externality = float(n) * k * (P_with - P_without)
        scale = min(1.0, k / (k + 1.0)) * (1.0 + (r - t) / max(1.0, r)) / 2.0
        gamma = self.base_gamma * scale
        if t == r:
            gamma = gamma * 0.2
        U_C = E_C + gamma * externality
        U_D = E_D
        personal_loss_if_cooperate = E_D - (E_C + gamma * externality)
        if U_C >= U_D + self.tol and E_C + gamma * externality >= E_D - self.sacrifice_threshold:
            return Action.C
        if U_D > U_C + self.tol:
            if t == r and P_with - P_without >= 0.4 and (E_C + gamma * externality >= E_D - self.sacrifice_threshold):
                return Action.C
            return Action.D
        if abs(U_C - U_D) <= self.tol:
            if t <= math.ceil(r / 3.0):
                return Action.C
            if random.random() < 0.5:
                return Action.C
            return Action.D
        return Action.D


# gpt-5-mini[exploitative]
class Strategy_EXPLOITATIVE_44(BaseStrategy):
    """
    Exploitative pivotal cooperator strategy for the Collective Risk Dilemma.

    Summary:
    - Estimate each opponent's cooperation probability with Laplace smoothing (alpha=beta=1).
    - Compute the Poisson-binomial PMF for the number S of other cooperators.
    - Let P_pivotal = P(S == m-1). Cooperate iff k * P_pivotal > 1 (i.e., P_pivotal > 1/k),
      except always defect in the final round.
    - Apply a small, decaying exploration probability epsilon = min(0.05, 1/sqrt(1+T_obs))
      to invert the chosen action and probe opponents.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self._alpha = 1.0
        self._beta = 1.0

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        n_players = int(self.game_description.n_players)
        n_rounds = int(self.game_description.n_rounds)
        m = int(self.game_description.m)
        k = float(self.game_description.k)
        T_obs = int(state.round_number)
        rounds_remaining = n_rounds - T_obs
        if rounds_remaining <= 1:
            base_action = Action.D
            epsilon = min(0.05, 1.0 / math.sqrt(1.0 + T_obs))
            if random.random() < epsilon:
                return Action.C if base_action == Action.D else Action.D
            return base_action
        n_opponents = max(0, n_players - 1)
        if history is None or getattr(history, 'opponent_actions', None) is None or history.opponent_actions.size == 0:
            if n_opponents <= 0:
                p_list = []
            else:
                p_list = [(0.0 + self._alpha) / (float(T_obs) + self._alpha + self._beta)] * n_opponents
        else:
            opp_actions = history.opponent_actions
            if opp_actions.shape[0] == 0:
                coops = np.zeros(n_opponents, dtype=float)
            else:
                coops = np.sum(opp_actions.astype(float), axis=0)
            denom = float(T_obs) + self._alpha + self._beta
            p_list = []
            for j in range(n_opponents):
                coop_j = float(coops[j]) if j < coops.shape[0] else 0.0
                p_j = (coop_j + self._alpha) / denom
                if p_j < 0.0:
                    p_j = 0.0
                elif p_j > 1.0:
                    p_j = 1.0
                p_list.append(p_j)
        pmf = [0.0] * (n_opponents + 1)
        pmf[0] = 1.0
        for p in p_list:
            new_pmf = [0.0] * (n_opponents + 1)
            new_pmf[0] = pmf[0] * (1.0 - p)
            for s in range(1, n_opponents + 1):
                new_pmf[s] = pmf[s] * (1.0 - p) + pmf[s - 1] * p
            pmf = new_pmf
        pivotal_index = m - 1
        if 0 <= pivotal_index <= n_opponents:
            P_pivotal = pmf[pivotal_index]
        else:
            P_pivotal = 0.0
        if k * P_pivotal > 1.0:
            base_action = Action.C
        else:
            base_action = Action.D
        epsilon = min(0.05, 1.0 / math.sqrt(1.0 + T_obs))
        if random.random() < epsilon:
            return Action.C if base_action == Action.D else Action.D
        return base_action


# llama3.1-70b[collective]
class Strategy_COLLECTIVE_509(BaseStrategy):
    """
    A strategy that balances individual self-interest with collective well-being by 
    encouraging cooperation through reciprocal altruism, detecting and responding to 
    defection, exploring alternative strategies to adapt to changing opponent behaviors, 
    and learning from the collective behavior of others.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.p_init = 0.5
        self.p_recip = 0.8
        self.p_defect = 0.7
        self.p_explore = 0.1
        self.delta_p = 0.05

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C if random.random() < self.p_init else Action.D
        prev_round_coops = sum(history.opponent_actions[-1, :] + [history.my_actions[-1]])
        prev_round_payoff = history.my_payoffs[-1]
        avg_coops = np.mean(np.sum(history.opponent_actions, axis=1) + history.my_actions)
        coop_prob = self.p_init
        if prev_round_coops >= self.game_description.m and prev_round_payoff > 1:
            coop_prob = self.p_recip
        elif np.sum(history.opponent_actions[-1, :]) > self.game_description.n_players - self.game_description.m:
            coop_prob = 1 - self.p_defect
        if random.random() < self.p_explore:
            return Action.C if random.random() < 0.5 else Action.D
        else:
            action = Action.C if random.random() < coop_prob else Action.D
        prev_avg_coops = np.mean(np.sum(history.opponent_actions[:-1, :], axis=1) + history.my_actions[:-1])
        if avg_coops > prev_avg_coops and coop_prob < 1:
            coop_prob += self.delta_p
        elif avg_coops < prev_avg_coops and coop_prob > 0:
            coop_prob -= self.delta_p
        return action


# llama3.1-70b[exploitative]
class Strategy_EXPLOITATIVE_514(BaseStrategy):
    """
    Exploitative Strategy: "Adaptive Threshold Pursuer" (ATP)
    
    This strategy adapts to the number of cooperators in previous rounds, 
    aiming to encourage cooperation when the threshold is not met and exploit 
    cooperation when the threshold is met or exceeded.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        n_players = self.game_description.n_players
        m_threshold = self.game_description.m
        k_factor = self.game_description.k
        if state.round_number == 0 or history is None:
            return random.choice([Action.C] * (m_threshold // n_players + (1 if m_threshold % n_players != 0 else 0)) + [Action.D] * (n_players - (m_threshold // n_players + (1 if m_threshold % n_players != 0 else 0))))
        prev_cooperators = sum(history.opponent_actions[-1, :])
        if prev_cooperators < m_threshold:
            return Action.D if random.random() > (k_factor - 1) / (n_players - m_threshold + 1) else Action.C
        elif prev_cooperators == m_threshold - 1:
            return Action.C if random.random() < (k_factor - 1) / (k_factor + 1) else Action.D
        else:
            return Action.C if random.random() < (k_factor - 1) / k_factor else Action.D
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D


# mistral-7b[collective]
class Strategy_COLLECTIVE_167(BaseStrategy):
    """
    TFT-AC Strategy for Collective Risk Dilemma.
    This strategy follows Tit-for-Tat with adaptive cooperation based on the collective actions of opponents.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.propensity = 0.5
        self.cooperators_threshold = 0.6

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        cooperators = sum(history.opponent_actions[-1, :])
        total_players = len(history.opponent_actions[0, :])
        if cooperators >= self.game_description.m:
            cooperation_rate = cooperators / total_players
            if cooperation_rate > self.cooperators_threshold:
                self.propensity += 0.05
            elif cooperation_rate < self.cooperators_threshold - 0.1:
                self.propensity -= 0.05
        action = Action.D if random.random() > self.propensity else Action.C
        return action


# mistral-7b[exploitative]
class Strategy_EXPLOITATIVE_107(BaseStrategy):
    """
    Tit-for-Tat with Adaptive Cooperation Threshold (TFT-ACT) strategy in Collective Risk Dilemma game.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.lookback_window = game_description.n_players // 10
        self.min_coop_prop = game_description.m / game_description.n_players
        self.baseline_probability = 0.5
        self.current_q = self.baseline_probability
        self.w = self.lookback_window
        self.act_active = False

    def __call__(self, state: GameState, history: PlayerHistory) -> Action:
        if state.round_number == 0 or not history:
            return Action.C
        cooperators = np.sum(history.opponent_actions[-self.w:, :])
        coop_prop = cooperators / self.w
        if coop_prop >= self.min_coop_prop and (not self.act_active):
            self.current_q = 0.7
            self.act_active = True
        elif coop_prop < self.min_coop_prop and self.act_active:
            self.current_q = self.baseline_probability
            self.act_active = False
        opponent_actions = history.opponent_actions[-1, :] if state.round_number != 0 else np.zeros(self.game_description.n_players)
        cooperators = np.count_nonzero(opponent_actions)
        if random.random() < self.current_q:
            action = Action.C if cooperators >= self.game_description.m else Action.D
        else:
            action = Action.D if cooperators >= self.game_description.m else Action.C
        return action
