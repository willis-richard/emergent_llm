# n=4
# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_466]
class Strategy_EXPLOITATIVE_466(BaseStrategy):
    """
    Threshold Parasitism: An exploitative strategy for Collective Risk Dilemmas.
    
    Core approach:
    - Always defect in round 1 (no history to exploit)
    - Always defect in final two rounds (no future consequences)
    - In middle rounds, defect to free-ride on others' cooperation
    - Exploit the coordination problem by avoiding contribution costs
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.m = game_description.m
        self.k = game_description.k

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        round_num = state.round_number
        if round_num == 0:
            return Action.D
        if round_num >= self.n_rounds - 2:
            return Action.D
        if history is None or len(history.opponent_actions) == 0:
            coop_rate = 0.0
        else:
            total_cooperations = np.sum(history.opponent_actions)
            total_possible = self.n_players * (round_num + 1)
            if total_possible > 0:
                coop_rate = total_cooperations / total_possible
            else:
                coop_rate = 0.0
        threshold_likelihood = (self.m - 1) / self.n_players
        return Action.D


# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_225]
class Strategy_EXPLOITATIVE_225(BaseStrategy):
    """
    Conditional Parasite: Exploitative threshold-hunting strategy.
    
    Defects by default, cooperates only when necessary to secure the threshold
    and enable free-riding. Uses predictive modeling of opponent cooperation
    to identify tipping points where conditional cooperation maximizes payoff.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.m = game_description.m
        self.k = game_description.k
        self.k_window = min(5, max(1, self.n_rounds // 2))
        self.committed_defector_threshold = 0.1
        self.volatility_threshold = 0.4

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        round_num = state.round_number
        if round_num == 0:
            return self._decide_round_zero()
        if round_num == self.n_rounds - 1:
            return Action.D
        return self._decide_middle_round(state, history)

    def _decide_round_zero(self) -> Action:
        """
        Round 0 decision: estimate if threshold will be met with minimal cooperation.
        """
        p_cooperate_est = self.m / self.n_players
        expected_cooperators = (self.n_players - 1) * p_cooperate_est
        if expected_cooperators >= self.m:
            return Action.D
        else:
            return Action.C

    def _decide_middle_round(self, state: GameState, history: PlayerHistory) -> Action:
        """
        Middle rounds (1 to r-2): Use predictive model to identify tipping points.
        """
        round_num = state.round_number
        predicted_cooperators = self._predict_cooperators(history, round_num)
        if predicted_cooperators >= self.m:
            return Action.D
        elif predicted_cooperators == self.m - 1:
            return Action.C
        elif predicted_cooperators == self.m - 2:
            return Action.C
        else:
            return Action.D

    def _predict_cooperators(self, history: PlayerHistory, current_round: int) -> int:
        """
        Predict cooperation count in next round using recent history.
        """
        start_idx = max(0, current_round - self.k_window)
        recent_opponent_actions = history.opponent_actions[start_idx:current_round, :]
        predicted_count = 0
        for player_idx in range(self.n_players - 1):
            player_cooperations = recent_opponent_actions[:, player_idx]
            num_rounds_observed = len(player_cooperations)
            if num_rounds_observed == 0:
                predicted_count += self.m / self.n_players
                continue
            coop_count = np.sum(player_cooperations)
            coop_rate = coop_count / num_rounds_observed
            total_coop_rate = np.sum(history.opponent_actions[:current_round, player_idx]) / max(1, current_round)
            if total_coop_rate < self.committed_defector_threshold:
                predicted_count += 0.0
                continue
            volatility = self._calculate_volatility(player_cooperations)
            if volatility > self.volatility_threshold:
                predicted_count += 0.5
            else:
                predicted_count += coop_rate
        return int(math.floor(predicted_count + 0.5))

    def _calculate_volatility(self, actions: NDArray[np.bool_]) -> float:
        """
        Calculate volatility as the proportion of action switches.
        """
        if len(actions) < 2:
            return 0.0
        switches = 0
        for i in range(1, len(actions)):
            if actions[i] != actions[i - 1]:
                switches += 1
        volatility = switches / (len(actions) - 1)
        return volatility


# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_115]
class Strategy_EXPLOITATIVE_115(BaseStrategy):
    """
    Adaptive Threshold Parasitism: An exploitative strategy that identifies and rides on 
    others' cooperation while minimizing personal contribution. Defects strategically to 
    harvest rewards from reliable cooperators while ensuring the threshold is met.
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.m = game_description.m
        self.k = game_description.k
        self.opponent_cooperation_rates = np.zeros(self.n_players - 1)
        self.opponent_cooperation_counts = np.zeros(self.n_players - 1)

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round = state.round_number
        if current_round == 0:
            return Action.D
        if current_round == self.n_rounds - 1:
            return Action.D
        self._update_cooperation_statistics(history, current_round)
        cooperators_last_round = int(np.sum(history.opponent_actions[current_round - 1, :]))
        reliable_cooperators = int(np.sum(self.opponent_cooperation_rates > 0.6))
        if cooperators_last_round >= self.m:
            return Action.D
        elif reliable_cooperators >= self.m:
            return Action.D
        elif cooperators_last_round + reliable_cooperators >= self.m:
            if random.random() < 0.75:
                return Action.D
            else:
                return Action.C
        else:
            return Action.C

    def _update_cooperation_statistics(self, history: PlayerHistory, current_round: int) -> None:
        """
        Update cooperation rates for each opponent based on observed history.
        """
        for opponent_idx in range(self.n_players - 1):
            cooperations = int(np.sum(history.opponent_actions[:current_round, opponent_idx]))
            self.opponent_cooperation_counts[opponent_idx] = cooperations
            if current_round > 0:
                self.opponent_cooperation_rates[opponent_idx] = cooperations / current_round
            else:
                self.opponent_cooperation_rates[opponent_idx] = 0.0


# n=64
# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_411]
class Strategy_EXPLOITATIVE_411(BaseStrategy):
    """
    Adaptive Threshold Parasitism (ATP): A pure defection strategy that exploits
    the collective risk dilemma by free-riding on cooperators' contributions.
    
    Core principle: Always defect across all rounds. This maximizes payoff by:
    1. Avoiding the cooperation cost (c_i = 1)
    2. Harvesting the reward (k) when threshold m is reached by others
    3. Suffering no loss when cooperation fails
    4. Never exposing exploitable patterns
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        return Action.D


# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_365]
class Strategy_COLLECTIVE_365(BaseStrategy):
    """
    Adaptive Threshold Trust strategy for Collective Risk Dilemma.
    
    Maximizes collective welfare while maintaining individual resilience against exploitation.
    Operates on conditional cooperation with adaptive risk assessment:
    - Round 1: Cooperate (information gathering)
    - Rounds 2 to r-1: Cooperate if threshold was met last round, else defect
    - Round r: Defect (no future consequences)
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        n = self.game_description.n_players
        r = self.game_description.n_rounds
        m = self.game_description.m
        if state.round_number == 0:
            return Action.C
        if state.round_number == r - 1:
            return Action.D
        prev_round_index = state.round_number - 1
        opponent_cooperators = np.sum(history.opponent_actions[prev_round_index, :])
        own_prev_action = history.my_actions[prev_round_index]
        total_cooperators = opponent_cooperators + (1 if own_prev_action else 0)
        cooperation_rate = total_cooperators / n
        threshold_rate = m / n
        if cooperation_rate >= threshold_rate:
            return Action.C
        else:
            return Action.D


# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_373]
class Strategy_COLLECTIVE_373(BaseStrategy):
    """
    Adaptive Threshold Cooperation (ATC) Strategy for Collective Risk Dilemma.
    
    Balances individual rationality with collective welfare by:
    1. Seeding cooperation in round 1
    2. Cooperating when observed cooperation rate meets/exceeds threshold m/n
    3. Defecting when threshold is not met to avoid wasting endowment
    4. Maintaining consistency through end-game to support collective resilience
    """

    def __init__(self, game_description: CollectiveRiskDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.m = game_description.m
        self.k = game_description.k
        self.threshold_rate = self.m / self.n_players

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.C
        current_round = state.round_number
        previous_round_idx = current_round - 1
        previous_round_opponent_actions = history.opponent_actions[previous_round_idx, :]
        previous_round_my_action = history.my_actions[previous_round_idx]
        opponent_cooperators = np.sum(previous_round_opponent_actions)
        my_previous_action = int(previous_round_my_action)
        total_previous_cooperators = opponent_cooperators + my_previous_action
        cooperation_rate = total_previous_cooperators / self.n_players
        if cooperation_rate >= self.threshold_rate:
            return Action.C
        else:
            return Action.D
