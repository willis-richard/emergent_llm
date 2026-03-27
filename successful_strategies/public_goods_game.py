# n=4
# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_472]
class Strategy_EXPLOITATIVE_472(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Calculated Cooperation

    This strategy ruthlessly exploits cooperators by consistently defecting.
    It recognizes that defection is the dominant strategy in every round of the
    public goods game and maximizes payoff by parasitizing any cooperation while
    maintaining baseline payoff against other defectors.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.threshold = game_description.k / game_description.n_players

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.D
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D
        cooperators_last_round = sum(history.opponent_actions[-1, :])
        my_payoff_if_defected = 1 + self.game_description.k / self.game_description.n_players * cooperators_last_round
        cooperative_payoff = self.game_description.k / self.game_description.n_players * cooperators_last_round
        if cooperators_last_round > 0 and my_payoff_if_defected > cooperative_payoff:
            return Action.D
        return Action.D

# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_225]
class Strategy_EXPLOITATIVE_225(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Selective Parasitism

    This strategy implements pure defection as the dominant strategy in public goods games.
    It recognizes that defection is individually rational when 1 < k < n, and maintains
    defection across all game states to extract maximum value from cooperators while
    avoiding the cost of contribution.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.D
        n_players = self.game_description.n_players
        rounds_elapsed = state.round_number
        if history is not None and rounds_elapsed > 0:
            total_cooperators = int(np.sum(history.opponent_actions[:rounds_elapsed, :]))
            possible_observations = (n_players - 1) * rounds_elapsed
            cooperation_rate = total_cooperators / possible_observations if possible_observations > 0 else 0
        else:
            cooperation_rate = 0
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D
        if cooperation_rate > 0.7:
            return Action.D
        elif cooperation_rate > 0.3:
            return Action.D
        else:
            return Action.D
        return Action.D

# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_185]
class Strategy_EXPLOITATIVE_185(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Selective Parasitism

    Core approach: Always defect to maximize personal payoff by free-riding on others'
    contributions while avoiding the costs of cooperation. This pure defection strategy
    is individually rational regardless of opponent behavior.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.threshold_upper = 0.5
        self.threshold_lower = 0.2

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.D
        if state.round_number == self.game_description.n_rounds - 1:
            return Action.D
        prev_round_idx = state.round_number - 1
        cooperators_prev = np.sum(history.opponent_actions[prev_round_idx, :])
        cooperation_rate = cooperators_prev / self.game_description.n_players
        if cooperation_rate > self.threshold_lower:
            return Action.D
        else:
            return Action.D

# n=64
# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_170]
class Strategy_EXPLOITATIVE_170(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Selective Parasitism

    Defects by default, exploiting cooperators while matching defectors.
    Uses adaptive thresholds based on game parameters to decide when cooperation
    is profitable. Cooperates probabilistically in mid-game when cooperation rates
    are moderate, but always defects in round 1 and final round.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n = game_description.n_players
        self.r = game_description.n_rounds
        self.k = game_description.k
        self._calculate_thresholds()

    def _calculate_thresholds(self):
        """Calculate threshold_high, threshold_low, and p_strategic based on game parameters."""
        denominator = 1.0 - self.k / self.n
        if denominator > 0:
            self.threshold_high = self.k / self.n / denominator
        else:
            self.threshold_high = 1.0
        self.threshold_high = min(1.0, max(0.0, self.threshold_high))
        self.threshold_low = self.k / self.n * 0.3
        if self.n <= 3:
            self.threshold_low = self.k / self.n * 0.5
        self.p_strategic = min(0.15, self.k / self.n)

    def _get_weighted_cooperation_rate(self, history: PlayerHistory, current_round: int) -> float:
        """
        Calculate cooperation rate of opponents with memory decay.
        Recent behavior weighted more heavily than distant history.
        """
        if current_round < 1:
            return 0.0
        others_last_round = sum(history.opponent_actions[current_round - 1, :]) / (self.n - 1)
        if current_round > 1:
            earlier_rounds = history.opponent_actions[:current_round - 1, :]
            avg_earlier = np.mean(earlier_rounds)
            weighted_coop = 0.7 * others_last_round + 0.3 * avg_earlier
        else:
            weighted_coop = others_last_round
        return weighted_coop

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        current_round = state.round_number
        if current_round == 0:
            return Action.D
        if current_round == self.r - 1:
            return Action.D
        weighted_cooperation = self._get_weighted_cooperation_rate(history, current_round)
        if weighted_cooperation >= self.threshold_high:
            return Action.D
        elif weighted_cooperation >= self.threshold_low:
            if random.random() < self.p_strategic:
                return Action.C
            else:
                return Action.D
        else:
            return Action.D

# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_504]
class Strategy_EXPLOITATIVE_504(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Selective Exploitation

    This strategy exploits the fundamental asymmetry in the public goods game by:
    1. Always defecting to free-ride on others' contributions
    2. Detecting cooperation patterns and maintaining defection
    3. Adapting defection across all rounds to maximize personal payoff

    Core insight: Defection is strictly dominant (payoff difference = 1 > 0)
    regardless of others' cooperation rates, so we always defect.
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.cooperation_history = []

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        if state.round_number == 0:
            return Action.D
        if history is not None and len(history.opponent_actions) > 0:
            previous_round_idx = state.round_number - 1
            cooperators_in_previous = int(sum(history.opponent_actions[previous_round_idx, :]))
            self.cooperation_history.append(cooperators_in_previous)
        if len(self.cooperation_history) > 0:
            estimated_total_cooperators = sum(self.cooperation_history)
            rounds_observed = len(self.cooperation_history)
            estimated_cooperation_rate = estimated_total_cooperators / (self.game_description.n_players * rounds_observed)
        else:
            estimated_cooperation_rate = 0.0
        return Action.D

# claude-haiku-4-5[exploitative][Strategy_EXPLOITATIVE_394]
class Strategy_EXPLOITATIVE_394(BaseStrategy):
    """
    Exploitative Strategy: Adaptive Defection with Selective Parasitism

    This strategy always defects to maximize payoff by:
    1. Free-riding on any cooperators in the population
    2. Avoiding wasteful cooperation when others defect
    3. Establishing defection as the baseline from round 1

    Core insight: Defection is the dominant strategy in simultaneous-move
    public goods games when k < n. Even when opponents cooperate, defecting
    yields higher payoff (1 + share of contributions) than cooperating
    (share of contributions only).
    """

    def __init__(self, game_description: PublicGoodsDescription):
        self.game_description = game_description
        self.n_players = game_description.n_players
        self.n_rounds = game_description.n_rounds
        self.k = game_description.k

    def __call__(self, state: GameState, history: None | PlayerHistory) -> Action:
        """
        Decision rule: Always defect.

        Round 1 (history=None): Defect to probe and avoid exploitation
        Rounds 2 to r-1: Defect to exploit cooperators or match defectors
        Round r: Defect with no future punishment possible

        This is the dominant strategy regardless of opponent behavior.
        """
        return Action.D

